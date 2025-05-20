import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
from util import makeslid, make_axslid, makeline
from gale_shapley import state_assignment
from matplotlib.widgets import CheckButtons

# Create figure and axis
fig = plt.figure(1)
ax = fig.subplots()

plt.subplots_adjust(bottom=0.3)
ax.set_ylim([-3, 3])
ax.set_title("3 Level system")
w1_init = -1
w2_init = 0
w3_init = 1


def energies(w1, w2, w3, g12, g23, g13):
    A = np.array([[w1, g12, g13], [g12, w2, g23], [g13, g23, w3]])
    vals, vecs = np.linalg.eigh(A)
    # they come in acending order
    return vals, vecs


# we assume we start with 1 state lower than 2 state
(line1,) = makeline(w1_init, "r", "low")
(line2,) = makeline(w2_init, "g", "mid")
(line3,) = makeline(w3_init, "b", "high")
(line1bare,) = makeline(w1_init, "r", "bare low", True)
(line2bare,) = makeline(w2_init, "g", "bare mid", True)
(line3bare,) = makeline(w3_init, "b", "bare high", True)
ax.legend(loc="upper right")
ax.set_ylabel("Energy")
x1 = 0.6
x2 = 0.1
fontsize = 13
# Add Slider
ax_slid_g12 = make_axslid(x1, 0.05)
ax_slid_g23 = make_axslid(x1, 0.1)
ax_slid_g13 = make_axslid(x1, 0.15)
ax_slidw1 = make_axslid(x2, 0.05)
ax_slidw2 = make_axslid(x2, 0.1)
ax_slidw3 = make_axslid(x2, 0.15)

slid_g12 = makeslid(ax_slid_g12, "g12", 0, 0.01, 1)
slid_g23 = makeslid(ax_slid_g23, "g23", 0, 0.01, 1)
slid_g13 = makeslid(ax_slid_g13, "g13", 0, 0.01, 1)
slidw1 = makeslid(ax_slidw1, "w1", 0.1, 5, w1_init)
slidw2 = makeslid(ax_slidw2, "w2", 0.1, 5, w2_init)
slidw3 = makeslid(ax_slidw3, "w3", 0.1, 5, w3_init)

text1 = ax.text(-0.95, w1_init, "1", fontsize=fontsize)
text2 = ax.text(-0.9, w2_init, "2", fontsize=fontsize)
text3 = ax.text(-0.85, w3_init, "3", fontsize=fontsize)
textbare1 = ax.text(0, w1_init, "bare 1", fontsize=fontsize)
textbare2 = ax.text(0, w2_init, "bare 2", fontsize=fontsize)
textbare3 = ax.text(0, w3_init, "bare 3", fontsize=fontsize)

lines = [line1, line2, line3]
linesbare = [line1bare, line2bare, line3bare]
texts = [text1, text2, text3]

ax_checkbox = plt.axes([x1, 0.2, 0.2, 0.05])  # [left, bottom, width, height]
checkbox = CheckButtons(ax_checkbox, ["Gale Shapely"], [False])  # Checked by default

#
#
#

fig2 = plt.figure(2)
ax2 = fig2.add_subplot(111, projection="3d")
ax2.set_xlim([-1.2, 1.2])
ax2.set_ylim([-1.2, 1.2])

(vecline1bare,) = ax2.plot([-1, 1], [0, 0], [0, 0], label="bare low", linestyle=":", color="r")
(vecline2bare,) = ax2.plot([0, 0], [-1, 1], [0, 0], label="bare mid", linestyle=":", color="g")
(vecline3bare,) = ax2.plot([0, 0], [0, 0], [-1, 1], label="bare high", linestyle=":", color="b")
(vecline1,) = ax2.plot([-1, 1], [0, 0], [0, 0], label="low", color="r")
(vecline2,) = ax2.plot([0, 0], [-1, 1], [0, 0], label="mid", color="g")
(vecline3,) = ax2.plot([0, 0], [0, 0], [-1, 1], label="high", color="b")
# we assume 1 starts with lower energy than 2
vectext1 = ax2.text(1, 0, 0, "1", fontsize=fontsize)
vectext2 = ax2.text(0, 1, 0, "2", fontsize=fontsize)
vectext3 = ax2.text(0, 0, 1, "3", fontsize=fontsize)
vectexts = [vectext1, vectext2, vectext3]
veclines = [vecline1, vecline2, vecline3]
veclinesbare = [vecline1bare, vecline2bare, vecline3bare]
ax2.text(0.5, 0, 0, "bare 1")
ax2.text(0, 0.5, 0, "bare 2")
ax2.text(0, 0, 0.5, "bare 3")
ax2.legend()

galeshap = False


# Update function
def update(val):
    w1 = slidw1.val
    w2 = slidw2.val
    w3 = slidw3.val
    g12 = slid_g12.val
    g23 = slid_g23.val
    g13 = slid_g13.val
    vals, vecs = energies(w1, w2, w3, g12, g23, g13)
    bare_to_dressed_index, _ = state_assignment(vecs)
    line1bare.set_ydata([w1, w1])
    line2bare.set_ydata([w2, w2])
    line3bare.set_ydata([w3, w3])
    colors = np.array(["r", "g", "b"])[np.argsort([w1, w2, w3])]
    for i in range(3):
        linesbare[i].set_color(colors[i])
        veclinesbare[i].set_color(colors[i])
        lines[i].set_ydata([vals[i], vals[i]])
        veclines[i].set_data_3d([-vecs[0, i], vecs[0, i]], [-vecs[1, i], vecs[1, i]], [-vecs[2, i], vecs[2, i]])

    textbare1.set_y(w1)
    textbare2.set_y(w2)
    textbare3.set_y(w3)

    for i in range(3):
        text = texts[i]
        vectext = vectexts[i]
        line = lines[bare_to_dressed_index[i]] if galeshap else lines[i]
        vecline = veclines[bare_to_dressed_index[i]] if galeshap else veclines[i]
        ii = 0 if np.sign(vecline.get_data_3d()[0][0]) > 0 else 1
        vectext.set_x(vecline.get_data_3d()[0][ii])
        vectext.set_y(vecline.get_data_3d()[1][ii])
        vectext.set_z(vecline.get_data_3d()[2][ii])
        text.set_y(line.get_ydata()[1])

    fig2.canvas.draw_idle()
    fig.canvas.draw_idle()


def toggle(val):
    global galeshap
    galeshap = not galeshap
    update(0)


checkbox.on_clicked(toggle)  # Attach function to checkbox

for s in [slid_g12, slid_g23, slid_g13, slidw1, slidw2, slidw3]:
    s.on_changed(update)


plt.show()
