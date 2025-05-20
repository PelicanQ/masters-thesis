from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
import numpy as np
from store.stores3T import Store_zz3T


Ej3 = 50
Ej1s = np.arange(60, 70, 1)
Ej2s = np.arange(75, 140, 1)
Eint12 = 0.04
Eint23 = 0.04
Eint13 = 0.0013
zz12, zz23, zz13, zzz = Store_zz3T.plane(
    "Ej2", Ej2s, 1, "Ej1", Ej1s, 1, Ej3=Ej3, Eint12=Eint12, Eint23=Eint23, Eint13=Eint13, Ec2=1, Ec3=1
)
# vars, zz12, zz23, zz13, zzz = Store_zz3T.line(
#     Ej2=60, Ej3=Ej3, Eint12=Eint12, Eint23=Eint23, Eint13=Eint13, Ec2=1, Ec3=1
# )
zz12 = zz12.flatten()
zz23 = zz23.flatten()
zz13 = zz13.flatten()
zzz = zzz.flatten()
one = np.ones_like(zzz)


def linear():
    # recreate figure 6 in ZZ paper

    A = np.column_stack([zz12, zz23, zz13, one])
    print(A.shape)

    x, ssr, rank, s = np.linalg.lstsq(A, zzz)
    print("coeff", x)

    sst = np.sum((zzz - np.mean(zzz)) ** 2)  # Total sum of squares
    r_squared = 1 - (ssr / sst)
    print("R2", r_squared)


def sk_learn():
    # Example data
    X_input = np.column_stack((zz12, zz23, zz13))

    poly = PolynomialFeatures(degree=1, include_bias=True)
    X_poly = poly.fit_transform(X_input)  # Adds powers and interaction terms
    print(X_poly.shape)

    # Fit the linear regression model to the polynomial-transformed features
    model = LinearRegression()
    reg = model.fit(X_poly, zzz)

    print("R²:", reg.score(X_poly, zzz))
    print("Coefficients:", reg.coef_)


linear()
