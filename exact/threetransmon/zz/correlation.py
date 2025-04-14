# Let's see if ZZZ correlates with the other 3 ZZ
from store.stores import Store_zz3t
import numpy as np
from matplotlib.widgets import Button
from matplotlib import pyplot as plt


vars, zz12, zz23, zz13, zzz = Store_zz3t.line(Ec2=1, Ec3=1, Ej2=50, Ej3=50, Eint12=0.1, Eint23=0.1, Eint13=0.1)
A = np.array([zz12, zz23, zz13, zzz])

fig = plt.figure()
origins = []
planes = []
index = 0


def proj2(A, plane: tuple | None = None):
    dim = A.shape[0]
    print(plane)
    if plane == None:
        # print("New")
        v1 = np.random.randn(dim)
        v1 /= np.linalg.norm(v1)
        v2 = np.random.randn(dim)
        v2 = v2 - np.dot(v1, v2) * v1
        v2 /= np.linalg.norm(v2)
        v1 = v1.reshape((dim, 1))
        v2 = v2.reshape((dim, 1))
    else:
        v1, v2 = plane
    e1 = np.array([[1, 0]]).T
    e2 = np.array([[0, 1]]).T
    P = e1 @ v1.T + e2 @ v2.T  # project onto 2D subspace
    R = P @ A
    return R, v1, v2


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


R, v1, v2 = proj2(A)
planes.append((v1, v2))
ax = fig.add_subplot(1, 1, 1)
plot = ax.scatter(R[0, :], R[1, :])
# else:
#     R = proj3(A)
#     ax = fig.add_subplot(1, 1, 1, projection="3d")
#     t = ax.scatter(R[0, :], R[1, :], R[2, :])


def on_next(val):
    global R, ax, index
    print(index)
    index += 1
    if index >= len(planes):
        R, v1, v2 = proj2(A)
        planes.append((v1, v2))
    else:
        v1, v2 = planes[index]
        R, _, _ = proj2(A, plane=(v1, v2))
    plot.set_offsets(np.c_[R[0, :], R[1, :]])

    # else:
    #     R = proj3(A)
    #     t.set_offsets(np.c_[R[0, :], R[1, :], R[2, :]])
    fig.canvas.draw_idle()


def on_prev(val):
    global R, ax, index
    if index == 0:
        return
    index -= 1
    v1, v2 = planes[index]
    R, _, _ = proj2(A, plane=(v1, v2))
    plot.set_offsets(np.c_[R[0, :], R[1, :]])
    # else:
    #     R = proj3(A)
    #     plot.set_offsets(np.c_[R[0, :], R[1, :], R[2, :]])
    fig.canvas.draw_idle()


nextax = plt.axes((0.7, 0.05, 0.1, 0.075))
prevax = plt.axes((0.6, 0.05, 0.1, 0.075))
nextbtn = Button(nextax, "Next")
prevbtn = Button(prevax, "Prev")
nextbtn.on_clicked(on_next)
prevbtn.on_clicked(on_prev)

fig.subplots_adjust(bottom=0.17)


plt.show()
