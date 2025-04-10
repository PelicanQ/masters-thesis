# let's make a little tool to visualize bare transmon energies and exact as a function of Ej Eint sliders
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
from util import makeslid, make_axslid, makeline
from gale_shapley import state_assignment
from matplotlib.widgets import CheckButtons
from exact.threetransmon.hamil import eig_clever_vis
import cupy as cp

# Create figure and axis
fig = plt.figure(1)
ax = fig.subplots()

plt.subplots_adjust(bottom=0.2)
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
    (line,) = makeline(0, "gray", "XXX")
    (linebare,) = makeline(0, "gray", f"{i}", True)
    lines.append(line)
    linesbare.append(linebare)

# ax.legend(loc="upper right")
ax.set_ylabel("Energy")
x1 = 0.6
x2 = 0.1
fontsize = 12
# Add Slider
ax_slid_Eint12 = make_axslid(x1, 0.05)
ax_slid_Eint23 = make_axslid(x1, 0.1)
ax_slid_Eint13 = make_axslid(x1, 0.15)
ax_slidEj1 = make_axslid(x2, 0.05)
ax_slidEj2 = make_axslid(x2, 0.1)
ax_slidEj3 = make_axslid(x2, 0.15)

slid_Eint12 = makeslid(ax_slid_Eint12, "Eint12", 0.5, 0.01, 0.5)
slid_Eint23 = makeslid(ax_slid_Eint23, "Eint23", 0.5, 0.01, 0.5)
slid_Eint13 = makeslid(ax_slid_Eint13, "Eint13", 0.5, 0.01, 0.5)
slidEj1 = makeslid(ax_slidEj1, "Ej1", Ej1_init, 0.1, 20)
slidEj2 = makeslid(ax_slidEj2, "Ej2", Ej2_init, 0.1, 20)
slidEj3 = makeslid(ax_slidEj3, "Ej3", Ej3_init, 0.1, 20)

textbares = []
dx = 0.1
for i in range(len(linesbare)):
    text = ax.text(-0.95 + i * dx, 0, f"{i}", fontsize=fontsize)
    textbares.append(text)
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
    Eint12 = slid_Eint12.val
    Eint23 = slid_Eint23.val
    Eint13 = slid_Eint13.val
    levels, sortedbare = eig_clever_vis(1, 1, Ej1, Ej2, Ej3, Eint12, Eint23, Eint13, only_energy=True, k=7, M=20)
    # ignore ground state
    levels = levels - levels[0]
    levels = levels[1:]
    states = [item[0] for item in sortedbare][1:]
    bare_levels = [item[1] for item in sortedbare][1:]

    for i in range(len(linesbare)):
        bareE = bare_levels[i]
        E = levels[i]
        linesbare[i].set_ydata([bareE, bareE])
        lines[i].set_ydata([E, E])
    # colors = np.array(["r", "g", "b"])[np.argsort([w1, w2, w3])]
    # for i in range(3):
    #     linesbare[i].set_color(colors[i])
    #     lines[i].set_ydata([vals[i], vals[i]])
    for i in range(len(textbares)):
        textbares[i].set_text("".join(map(str, states[i])))
        textbares[i].set_y(bare_levels[i])

    # for i in range(3):
    #     text = texts[i]
    #     line = lines[bare_to_dressed_index[i]] if galeshap else lines[i]
    #     text.set_y(line.get_ydata()[1])
    fig.canvas.draw_idle()
    ax.relim()
    ax.autoscale_view()


def toggle(val):
    global galeshap
    galeshap = not galeshap
    update(0)


# checkbox.on_clicked(toggle)  # Attach function to checkbox

for s in [slid_Eint12, slid_Eint23, slid_Eint13, slidEj1, slidEj2, slidEj3]:
    s.on_changed(update)


plt.show()
