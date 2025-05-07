# Let's see if ZZZ correlates with the other 3 ZZ
from store.stores3T import Store_zz3T
import numpy as np
from matplotlib.widgets import Button
from matplotlib import pyplot as plt


vars, zz12, zz23, zz13, zzz = Store_zz3T.line(Ec2=1, Ec3=1, Ej2=50, Ej3=50, Eint12=0.1, Eint23=0.1, Eint13=0.01)
_, zz12_, zz23_, zz13_, zzz_ = Store_zz3T.line(Ec2=1, Ec3=1, Ej2=50, Ej3=50, Eint12=0.1, Eint23=0.1, Eint13=0.005)
zz12.extend(zz12_)
zz23.extend(zz23_)
zz13.extend(zz13_)
zzz.extend(zzz_)
A = np.array([zz12, zz23, zz13, zzz])

fig = plt.figure()
fig.suptitle("Projection of data in 4D space")
origins = []
planes = []
index = 0


def proj3(A):
    dim = A.shape[0]
    v1 = np.random.randn(dim)
    v1 /= np.linalg.norm(v1)

    v2 = np.random.randn(dim)
    v2 = v2 - np.dot(v1, v2) * v1
    v2 /= np.linalg.norm(v2)

    v3 = np.random.randn(dim)
    v3 = v3 - np.dot(v1, v3) * v1 - np.dot(v2, v3) * v2
    v3 /= np.linalg.norm(v3)

    v1 = v1.reshape((dim, 1))
    v2 = v2.reshape((dim, 1))
    v3 = v3.reshape((dim, 1))
    e1 = np.array([[1, 0, 0]]).T
    e2 = np.array([[0, 1, 0]]).T
    e3 = np.array([[0, 0, 1]]).T
    P = e1 @ v1.T + e2 @ v2.T + e3 @ v3.T

    R = P @ A
    return R, v1, v2, v3


R, v1, v2, v3 = proj3(A)
ax = fig.add_subplot(1, 1, 1, projection="3d")
plot = ax.scatter(R[0, :], R[1, :], R[2, :])


def on_next(val):
    global R, index
    print(index)
    index += 1
    if index >= len(planes):
        R, v1, v2, v3 = proj3(A)
        planes.append((v1, v2, v3))
    else:
        v1, v2, v3 = planes[index]
        R, _, _, _ = proj3(A, plane=(v1, v2, v3))
    x, y, z = (R[0, :], R[1, :], R[2, :])
    plot._offsets3d = (x, y, z)
    ax.set_xlim(np.min(x), np.max(x))
    ax.set_ylim(np.min(y), np.max(y))
    ax.set_zlim(np.min(z), np.max(z))
    fig.canvas.draw_idle()


def on_prev(val):
    global R, index
    if index == 0:
        return
    index -= 1
    v1, v2, v3 = planes[index]
    R, _, _, _ = proj3(A, plane=(v1, v2, v3))
    x, y, z = (R[0, :], R[1, :], R[2, :])
    plot._offsets3d = (x, y, z)
    ax.set_xlim(np.min(x), np.max(x))
    ax.set_ylim(np.min(y), np.max(y))
    ax.set_zlim(np.min(z), np.max(z))
    fig.canvas.draw_idle()


nextax = plt.axes((0.7, 0.05, 0.1, 0.075))
prevax = plt.axes((0.6, 0.05, 0.1, 0.075))
nextbtn = Button(nextax, "Next")
prevbtn = Button(prevax, "Prev")
nextbtn.on_clicked(on_next)
prevbtn.on_clicked(on_prev)

fig.subplots_adjust(bottom=0.17)


plt.show()
