# Let's see if ZZZ correlates with the other 3 ZZ
from store.stores import Store_zz3t
import numpy as np
from matplotlib import pyplot as plt
vars, zz12, zz23, zz13, zzz = Store_zz3t.line(Ec2=1, Ec3=1, Ej2=50, Ej3=50,Eint12=0.1, Eint23=0.1, Eint13=0.1)
A = np.array([zz12,zz23,zz13,zzz])


def proj2(A):
    dim = A.shape[0]
    v1 = np.random.randn(dim)
    v1 /=np.linalg.norm(v1)
    v2 = np.random.randn(dim)
    v2 = v2 - np.dot(v1,v2) * v1
    v2 /=np.linalg.norm(v2)
    v1 = v1.reshape((dim,1))
    v2 = v2.reshape((dim,1))
    e1 = np.array([[1,0]]).T
    e2 = np.array([[0,1]]).T
    
    P = e1 @ v1.T + e2 @ v2.T # project onto 2D subspace
    R = P @ A
    return R

def proj3(A):
    dim = A.shape[0]
    v1 = np.random.randn(dim)
    v1 /=np.linalg.norm(v1)

    v2 = np.random.randn(dim)
    v2 = v2 - np.dot(v1,v2) * v1
    v2 /=np.linalg.norm(v2)

    v3 = np.random.randn(dim)
    v3 = v3 - np.dot(v1,v3) * v1 - np.dot(v2,v3) * v2
    v3 /=np.linalg.norm(v3)

    v1 = v1.reshape((dim,1))
    v2 = v2.reshape((dim,1))
    v3 = v3.reshape((dim,1))
    e1 = np.array([[1,0,0]]).T
    e2 = np.array([[0,1,0]]).T
    e3 = np.array([[0,0,1]]).T
    P = e1 @ v1.T + e2 @ v2.T + e3 @ v3.T

    R = P@A
    return R

# print(R)
R = proj3(A)
# plt.scatter(R[0,:],R[1,:])

ax = plt.subplot(1,1,1,projection='3d')
ax.scatter(R[0,:],R[1,:],R[2,:])
plt.show()