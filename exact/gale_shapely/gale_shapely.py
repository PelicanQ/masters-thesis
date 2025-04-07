import numpy as np
from numpy.typing import NDArray
import cupy
from exact.gale_shapely.loop_cython import cython_loop
import numba


@numba.jit
def jitted_loop(ranked_preference, number_of_states, preference):
    bare_to_dressed_index = number_of_states * [-1]
    dressed_assigned = number_of_states * [False]  # Initialize all states as unassigned.
    bare_assigned = number_of_states * [False]
    dressed_proposer = 0
    while dressed_proposer != -1:
        # Propose to bare states based on preference
        for bare_proposee in ranked_preference[:, dressed_proposer][::-1]:
            # If the bare proposee is unassigned -> assign
            if not bare_assigned[bare_proposee]:
                bare_assigned[bare_proposee] = True
                dressed_assigned[dressed_proposer] = True
                bare_to_dressed_index[bare_proposee] = dressed_proposer
                break
            # If the bare proposee is assigned -> check if proposee prefers proposer over currently assigned.
            else:
                dressed_current = bare_to_dressed_index[bare_proposee]
                if preference[bare_proposee, dressed_proposer] > preference[bare_proposee, dressed_current]:
                    # Unassign currently assigned dressed state.
                    dressed_assigned[dressed_current] = False

                    # Assign proposer and proposee.
                    dressed_assigned[dressed_proposer] = True
                    bare_to_dressed_index[bare_proposee] = dressed_proposer
                    break
        try:
            dressed_proposer = dressed_assigned.index(False)
        except:
            dressed_proposer = -1

    return bare_to_dressed_index


def state_assignment(eigen_states: NDArray) -> tuple[int]:
    number_of_states = eigen_states.shape[0]
    preference = np.abs(eigen_states)

    ranked_preference = cupy.asnumpy(cupy.argsort(cupy.asarray(preference), axis=0))
    # return cython_loop(ranked_preference, number_of_states, preference)
    return jitted_loop(ranked_preference, number_of_states, preference)


def state_assignment2(eigen_states: NDArray) -> tuple[tuple[int], tuple[int]]:
    """Computes a 1-to-1 assignment map between the dressed states (eigenstates) and bare states.
    The map is computed by reducing the assignment problem to a Stable Marriage Problem,
    which is solved by the Gale-Shapley algorithm. The Gale-Shapley algorithm is implemented
    with using the state overlap between the dressed and bare states as preference metric.

    Note, the computed map is the optimal map for the dressed states,
    meaning that every dressed state is stably assigned to their bare state with highest possible preference.
    To get the optimal map for the bare states, the inverse of 'eigen_states' should be given as argument.

    Args:
        eigen_states (NDArray): The eigenstates stored as column vectors expressed in the bare-state basis.

    Returns:
        bare_to_dressed_index (tuple): A map from the Hamiltonian indices of the bare states to the dressed states.
        dressed_to_bare_index (tuple): A map from the Hamiltonian indices of the dressed states to the bare states.
    """
    # Initialize requisites for the Gale-Shapley algorithm.
    number_of_states = eigen_states.shape[0]
    dressed_to_bare_index = number_of_states * [-1]
    bare_to_dressed_index = number_of_states * [-1]
    preference = np.abs(eigen_states)

    ranked_preference = cupy.asnumpy(
        cupy.argsort(cupy.asarray(preference), axis=0)
    )  # Eigenvectors are stored as column vectors.

    # The Gale-Shapley algorithm.
    # The dressed states (proposers) propose to the bare states (proposee),
    # to find matches until all states are assigned.
    dressed_assigned = number_of_states * [False]  # Initialize all states as unassigned.
    bare_assigned = number_of_states * [False]
    dressed_proposer = 0
    while dressed_proposer != -1:
        # Propose to bare states based on preference
        for bare_proposee in reversed(ranked_preference[:, dressed_proposer]):
            # If the bare proposee is unassigned -> assign
            if not bare_assigned[bare_proposee]:
                bare_assigned[bare_proposee] = True
                dressed_assigned[dressed_proposer] = True
                bare_to_dressed_index[bare_proposee] = dressed_proposer
                dressed_to_bare_index[dressed_proposer] = bare_proposee
                break
            # If the bare proposee is assigned -> check if proposee prefers proposer over currently assigned.
            else:
                dressed_current = bare_to_dressed_index[bare_proposee]
                if preference[bare_proposee, dressed_proposer] > preference[bare_proposee, dressed_current]:
                    # Unassign currently assigned dressed state.
                    dressed_assigned[dressed_current] = False
                    # dressed_to_bare_index[dressed_current] = -1

                    # Assign proposer and proposee.
                    dressed_assigned[dressed_proposer] = True
                    bare_to_dressed_index[bare_proposee] = dressed_proposer
                    dressed_to_bare_index[dressed_proposer] = bare_proposee
                    break
        try:
            dressed_proposer = dressed_assigned.index(False)
        except:
            dressed_proposer = -1

    return tuple(bare_to_dressed_index), tuple(dressed_to_bare_index)
