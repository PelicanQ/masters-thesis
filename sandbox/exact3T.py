# let's make a little tool to visualize bare transmon energies and exact as a function of Ej Eint sliders
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
from util import makeslid, make_axslid, makeline
from gale_shapley import state_assignment
from matplotlib.widgets import CheckButtons
from exact.three.hamil import eig_excitation_trunc
from exact.util import omega_alphas, exact_energy
import itertools


def sort_bare(Ej1, Ej2, Ej3):
    """For visualize only"""
    lis = []
    sortvals1 = np.array([exact_energy(i, 1, Ej1) for i in range(4)])
    sortvals2 = np.array([exact_energy(i, 1, Ej2) for i in range(4)])
    sortvals3 = np.array([exact_energy(i, 1, Ej3) for i in range(4)])
    sortvals1 = sortvals1 - sortvals1[0]
    sortvals2 = sortvals2 - sortvals2[0]
    sortvals3 = sortvals3 - sortvals3[0]
    for comb in itertools.product(range(4), repeat=3):
        n1 = comb[0]
        n2 = comb[1]
        n3 = comb[2]
        if sum(comb) < 4:
            lis.append(((n1, n2, n3), sortvals1[n1] + sortvals2[n2] + sortvals3[n3]))
    lis = sorted(lis, key=lambda item: item[1])
    states = np.array([x[0] for x in lis])
    levels = np.array([x[1] for x in lis])
    return levels, states


def sort_dressed(vals, vecs, idx_map):
    btd, dtb = state_assignment(vecs)
    lis = []

    for comb in itertools.product(range(4), repeat=3):
        lis.append((comb, vals[btd[idx_map[comb]]]))
    lis = sorted(lis, key=lambda x: x[1])
    states = np.array([x[0] for x in lis])
    return states


# Create figure and axis
fig = plt.figure(1)
plt.subplots_adjust(bottom=0.2)
fig2 = plt.figure(2)
ax = fig.subplots()
ax2 = fig2.subplots()
ax2.set_xlabel("o2prim")
ax2.set_ylabel("delta13")
(parampoint,) = ax2.plot(0, 0, marker="*")
ax2.set_ylim(-10, 10)
ax2.set_xlim(-10, 10)

ax.set_ylim([10, 80])
ax.set_title("3 transmon")

Ej1_init = 50
Ej2_init = 50
Ej3_init = 50

num_levels = 19


# we assume we start with 1 state lower than 2 state
lines = []
linesbare = []

for i in range(num_levels):
    (line,) = makeline(0, "gray", "XXX", ax=ax)
    (linebare,) = makeline(0, "gray", f"{i}", True, ax=ax)
    lines.append(line)
    linesbare.append(linebare)

ax.set_ylabel("Energy")
x1 = 0.6
x2 = 0.1
fontsize = 12
# Add Slider
ax_slid_Eint12 = make_axslid(x1, 0.05, fig)
ax_slid_Eint23 = make_axslid(x1, 0.1, fig)
ax_slid_Eint13 = make_axslid(x1, 0.15, fig)
ax_slidEj1 = make_axslid(x2, 0.05, fig)
ax_slidEj2 = make_axslid(x2, 0.1, fig)
ax_slidEj3 = make_axslid(x2, 0.15, fig)

slid_Eint12 = makeslid(ax_slid_Eint12, "Eint12", 0, 0.001, 0.15, 0)
slid_Eint23 = makeslid(ax_slid_Eint23, "Eint23", 0, 0.001, 0.15, 0)
slid_Eint13 = makeslid(ax_slid_Eint13, "Eint13", 0, 0.0001, 0.05, 0)
slidEj1 = makeslid(ax_slidEj1, "Ej1", 50, 1, 30, Ej1_init)
slidEj2 = makeslid(ax_slidEj2, "Ej2", 50, 1, 30, Ej2_init)
slidEj3 = makeslid(ax_slidEj3, "Ej3", 50, 1, 30, Ej3_init)

textbares = []
texts = []
dx = 0.1
for i in range(len(linesbare)):
    text = ax.text(-0.95 + i * dx, 0, f"{i}", fontsize=fontsize)
    textbares.append(text)
    text = ax.text(-0.90 + i * dx, 0, f"{i}")
    texts.append(text)

# text2 = ax.text(-0.9, w2_init, "2", fontsize=fontsize)
# text3 = ax.text(-0.85, w3_init, "3", fontsize=fontsize)
# textbare1 = ax.text(0, w1_init, "bare 1", fontsize=fontsize)
# textbare2 = ax.text(0, w2_init, "bare 2", fontsize=fontsize)
# textbare3 = ax.text(0, w3_init, "bare 3", fontsize=fontsize)

# texts = [text1, text2, text3]

# ax_checkbox = plt.axes([x1, 0.2, 0.2, 0.05])  # [left, bottom, width, height]
# checkbox = CheckButtons(ax_checkbox, ["Gale Shapely"], [False])  # Checked by default


galeshap = False


# Update function
def update(val):

    Ej1 = slidEj1.val
    Ej2 = slidEj2.val
    Ej3 = slidEj3.val
    Eint12 = slid_Eint12.val * 0
    Eint23 = slid_Eint23.val * 0
    Eint13 = slid_Eint13.val * 0
    dressed_levels, vecs, idx_map = eig_excitation_trunc(1, 1, Ej1, Ej2, Ej3, Eint12, Eint23, Eint13, k=7, M=15)

    bare_levels, bare_states = sort_bare(Ej1, Ej2, Ej3)
    dressed_states = sort_dressed(dressed_levels, vecs, idx_map)
    # ignore ground state
    bare_levels = bare_levels - bare_levels[0]
    dressed_levels = dressed_levels - dressed_levels[0]
    bare_states = bare_states[1:]
    bare_levels = bare_levels[1:]
    dressed_levels = dressed_levels[1:]
    dressed_states = dressed_states[1:]

    for i in range(len(linesbare)):
        linesbare[i].set_ydata([bare_levels[i], bare_levels[i]])
        # lines[i].set_ydata([dressed_levels[i], dressed_levels[i]])
        lines[i].set_ydata([0, 0])

        textbares[i].set_text("".join(map(str, bare_states[i])))
        textbares[i].set_y(bare_levels[i])
        # texts[i].set_y(dressed_levels[i])
        # texts[i].set_text("".join(map(str, dressed_states[i])))

    # param plot
    o1, _ = omega_alphas(1, Ej1, True)
    o2, _ = omega_alphas(1, Ej2, True)
    o3, _ = omega_alphas(1, Ej3, True)
    d13 = o1 - o3
    o2prim = o2 - (o3 + o1) / 2
    print(d13, o2prim)
    parampoint.set_data([o2prim, o2prim + 1e-6], [d13, d13])
    fig.canvas.draw_idle()
    ax.relim()
    ax.autoscale_view()

    fig2.canvas.draw_idle()
    ax2.relim()
    ax2.autoscale_view()


def toggle(val):
    global galeshap
    galeshap = not galeshap
    update(0)


# checkbox.on_clicked(toggle)  # Attach function to checkbox

for s in [slid_Eint12, slid_Eint23, slid_Eint13, slidEj1, slidEj2, slidEj3]:
    s.on_changed(update)


plt.show()
