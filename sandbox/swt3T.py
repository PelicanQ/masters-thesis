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


def sort_bare(o1, o2, o3):
    """For visualize only"""
    lis = []
    alpha = -1

    sortvals1 = np.array([0, o1, 2 * o1 + alpha, 3 * o1 + 3 * alpha])
    sortvals2 = np.array([0, o2, 2 * o2 + alpha, 3 * o2 + 3 * alpha])
    sortvals3 = np.array([0, o3, 2 * o3 + alpha, 3 * o3 + 3 * alpha])

    for comb in itertools.product(range(5), repeat=3):
        n1 = comb[0]
        n2 = comb[1]
        n3 = comb[2]
        if sum(comb) < 4:
            lis.append(((n1, n2, n3), sortvals1[n1] + sortvals2[n2] + sortvals3[n3]))
    lis = sorted(lis, key=lambda item: item[1])
    states = np.array([x[0] for x in lis])
    levels = np.array([x[1] for x in lis])
    return levels, states


# Create figure and axis
fig = plt.figure(1)
plt.subplots_adjust(bottom=0.2)
fig2 = plt.figure(2)
ax = fig.subplots()
ax2 = fig2.subplots()
ax2.set_xlabel("o2prim")
ax2.set_ylabel("delta13")
(parampoint,) = ax2.plot(0, 0, marker="*")
ax2.set_ylim(-6, 6)
ax2.set_xlim(-6, 6)
ax.set_ylim([10, 80])
ax.set_title("3T AHO")

o1_init = 25
o2_init = 25
o3_init = 25

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
ax_slid_o1 = make_axslid(x2, 0.05, fig)
ax_slid_o2 = make_axslid(x2, 0.1, fig)
ax_slid_o3 = make_axslid(x2, 0.15, fig)

slid_o1 = makeslid(ax_slid_o1, "o1", o1_init, 0.1, 10, o1_init)
slid_o2 = makeslid(ax_slid_o2, "o2", o2_init, 0.1, 10, o2_init)
slid_o3 = makeslid(ax_slid_o3, "o3", o3_init, 0.1, 10, o3_init)

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


# Update function
def update(val):

    o1 = slid_o1.val
    o2 = slid_o2.val
    o3 = slid_o3.val

    bare_levels, bare_states = sort_bare(o1, o2, o3)
    # ignore ground state
    bare_states = bare_states[1:]
    bare_levels = bare_levels[1:]

    for i in range(len(linesbare)):
        linesbare[i].set_ydata([bare_levels[i], bare_levels[i]])

        textbares[i].set_text("".join(map(str, bare_states[i])))
        textbares[i].set_y(bare_levels[i])

    # param plot
    d13 = o1 - o3
    o2prim = o2 - (o3 + o1) / 2
    parampoint.set_data([o2prim, o2prim], [d13, d13])
    # update
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

# for s in [slid_g12, slid_g23, slid_g13, slid_o1, slid_o2, slid_o3]:
for s in [slid_o1, slid_o2, slid_o3]:
    s.on_changed(update)


plt.show()
