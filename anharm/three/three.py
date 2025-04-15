# I want to see what coupling AH and RWA gives in the 2exc subspace of 3T on line

from anharm.Hamiltonian import Hamil

H = Hamil(3, 4, "line")
S = H.get_subspace(2)
print(S.basisnames)
# S.basisnames

print(S.statemat.loc["011", "020"])
