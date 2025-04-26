from onetransmon.hamil import plt, ngs, ng_sweep, N, calc_eigs

# here we just line up all eigenvalues in increasing order


for idx, Ej in enumerate([0, 1, 1e2, 1e3, 1e4, 1e5]):
    plt.subplot(2, 3, idx + 1)
    vals = calc_eigs(Ej, 0, k=100)
    vals = vals - vals[0]
    plt.plot(vals, marker=".", linewidth=0)
    plt.ylabel("En")
    plt.xlabel("n")
    plt.title(f"Ej={Ej:.2E}", fontsize=9)
plt.suptitle("All eigenenergies, varying Ej, k=100")
plt.show()
