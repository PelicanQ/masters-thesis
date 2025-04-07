import numpy as np
cimport numpy as np

def cython_loop(np.ndarray[np.int64_t, ndim=2] ranked_preference, int number_of_states, np.ndarray[np.float64_t, ndim=2] preference):
    # Initialize arrays
    cdef np.ndarray[np.int32_t, ndim=1] bare_to_dressed_index = np.full(number_of_states, -1, dtype=np.int32)
    cdef np.ndarray[np.npy_bool, ndim=1] dressed_assigned = np.zeros(number_of_states, dtype=np.bool_)
    cdef np.ndarray[np.npy_bool, ndim=1] bare_assigned = np.zeros(number_of_states, dtype=np.bool_)

    # Start with the first dressed proposer
    cdef Py_ssize_t dressed_proposer = 0

    while dressed_proposer != -1:
        # Propose to bare states based on preference
        for bare_proposee in ranked_preference[:, dressed_proposer][::-1]:
            # If the bare proposee is unassigned -> assign
            if not bare_assigned[bare_proposee]:
                bare_assigned[bare_proposee] = True
                dressed_assigned[dressed_proposer] = True
                bare_to_dressed_index[bare_proposee] = dressed_proposer
                break
            # If the bare proposee is assigned -> check if proposee prefers proposer over currently assigned
            else:
                dressed_current = bare_to_dressed_index[bare_proposee]
                if preference[bare_proposee, dressed_proposer] > preference[bare_proposee, dressed_current]:
                    # Unassign currently assigned dressed state
                    dressed_assigned[dressed_current] = False

                    # Assign proposer and proposee
                    dressed_assigned[dressed_proposer] = True
                    bare_to_dressed_index[bare_proposee] = dressed_proposer
                    break

        # Find the next unassigned dressed state
        dressed_proposer = -1
        for i in range(number_of_states):
            if not dressed_assigned[i]:
                dressed_proposer = i
                break

    return bare_to_dressed_index
