from .hamil import calc_eigs, plt
import numpy as np

# Now we look at fixed En

kk = np.concatenate(
    [np.arange(start=6, stop=20, step=1), np.arange(start=22, stop=60, step=4)]
)
n = 10  # which energy level to look at


Ejs = [1, 5, 10, 100, 400, 1000]
E = np.zeros(shape=(len(Ejs), len(kk)))

for j, Ej in enumerate(Ejs):
    for i, k in enumerate(kk):
        vals = calc_eigs(Ej, ng=0, k=k)
        val = vals[n] - vals[0]
        E[j, i] = val

low_cut = 15  # lower cut for std
stds = []

plt.figure(figsize=(12, 6))
# now make a subplot for each Ej
for j, Ej in enumerate(Ejs):

    energy = E[j, :]
    std = np.std(energy[low_cut:])
    stds.append(std)

    plt.subplot(2, 3, j + 1)
    plt.plot(kk, energy, marker=".")

    plt.axvline(x=kk[low_cut], color="r", linestyle="--")
    plt.title(f"Ej={Ej}, std=10^{np.log10(std):.0f}", fontsize=8)

    plt.xlabel("k")
    plt.ylabel(f"E{n}(k)-E0(k)")
    plt.tight_layout(pad=0.7)  # Adjust the padding between plots

plt.subplots_adjust(top=0.85)  # Adjust the top to make space for suptitle
plt.suptitle(f"Convergence of energy level {n} for different Ej")


plt.show()
