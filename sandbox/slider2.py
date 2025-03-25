import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
from util import makeslid, make_axslid, makeline
from gale_shapley import state_assignment
from matplotlib.widgets import CheckButtons

# Create figure and axis
fig = plt.figure(1)
ax = fig.subplots()

plt.subplots_adjust(bottom=0.2)
ax.set_ylim([-2, 2])
ax.set_title("2 Level system")
w1_init = 0
w2_init = 1


def energies(w1, w2, g):
    A = np.array([[w1, g], [g, w2]])
    vals, vecs = np.linalg.eigh(A)
    # they come in acending order
    return vals, vecs


# we assume we start with 1 state lower than 2 state
(line1,) = makeline(w1_init, "r", "low")
(line2,) = makeline(w2_init, "g", "high")
(line1bare,) = makeline(w1_init, "r", "bare low", True)
(line2bare,) = makeline(w2_init, "g", "bare high", True)
ax.legend()

x1 = 0.6
x2 = 0.1
fontsize = 13
# Add Slider
ax_slid1 = make_axslid(x1, 0.05)
ax_slidw1 = make_axslid(x2, 0.05)
ax_slidw2 = make_axslid(x2, 0.1)

slid_g12 = makeslid(ax_slid1, "g12", 0)
slidw1 = makeslid(ax_slidw1, "w1", w1_init)
slidw2 = makeslid(ax_slidw2, "w2", w2_init)
text1 = ax.text(-0.9, w1_init, "1", fontsize=fontsize)
text2 = ax.text(-0.9, w2_init, "2", fontsize=fontsize)
textbare1 = ax.text(0, w1_init, "bare 1", fontsize=fontsize)
textbare2 = ax.text(0, w2_init, "bare 2", fontsize=fontsize)

lines = [line1, line2]
texts = [text1, text2]

ax_checkbox = plt.axes([x1, 0.1, 0.2, 0.05])  # [left, bottom, width, height]
checkbox = CheckButtons(ax_checkbox, ["Gale Shapely"], [False])  # Checked by default

#
#
#

fig2 = plt.figure(2)
ax2 = fig2.add_subplot(111)
ax2.set_xlim([-1.2, 1.2])
ax2.set_ylim([-1.2, 1.2])

(vecline1bare,) = ax2.plot([-1, 1], [0, 0], label="bare low", linestyle=":", color="r")
(vecline2bare,) = ax2.plot([0, 0], [-1, 1], label="bare high", linestyle=":", color="g")
(vecline1,) = ax2.plot([-1, 1], [0, 0], label="low", color="r")
(vecline2,) = ax2.plot([0, 0], [-1, 1], label="high", color="g")
# we assume 1 starts with lower energy than 2
vectext1 = ax2.text(1, 0, "1", fontsize=fontsize)
vectext2 = ax2.text(0, 1, "2", fontsize=fontsize)
vectexts = [vectext1, vectext2]
veclines = [vecline1, vecline2]
ax2.text(0.5, 0, "bare 1")
ax2.text(0, 0.5, "bare 2")
ax2.legend()

galeshap = False


# Update function
def update(val):
    w1 = slidw1.val
    w2 = slidw2.val
    vals, vecs = energies(w1, w2, slid_g12.val)
    bare_to_dressed_index, _ = state_assignment(vecs)
    line1bare.set_ydata([w1, w1])
    line2bare.set_ydata([w2, w2])

    line1bare.set_color("r" if w2 > w1 else "g")
    line2bare.set_color("r" if w2 <= w1 else "g")
    vecline1bare.set_color("r" if w2 > w1 else "g")
    vecline2bare.set_color("r" if w2 <= w1 else "g")

    line1.set_ydata([vals[0], vals[0]])
    line2.set_ydata([vals[1], vals[1]])

    vecline1.set_xdata([-vecs[0, 0], vecs[0, 0]])
    vecline1.set_ydata([-vecs[1, 0], vecs[1, 0]])
    vecline2.set_xdata([-vecs[0, 1], vecs[0, 1]])
    vecline2.set_ydata([-vecs[1, 1], vecs[1, 1]])
    textbare1.set_y(slidw1.val)
    textbare2.set_y(slidw2.val)

    for i in range(2):
        text = texts[i]
        vectext = vectexts[i]
        line = lines[bare_to_dressed_index[i]] if galeshap else lines[i]
        vecline = veclines[bare_to_dressed_index[i]] if galeshap else veclines[i]

        vectext.set_x(vecline.get_xdata()[1])
        vectext.set_y(vecline.get_ydata()[1])
        text.set_y(line.get_ydata()[1])

    fig2.canvas.draw_idle()
    fig.canvas.draw_idle()


def toggle(val):
    global galeshap
    galeshap = not galeshap
    update(0)


checkbox.on_clicked(toggle)  # Attach function to checkbox

for s in [slid_g12, slidw1, slidw2]:
    s.on_changed(update)


plt.show()
