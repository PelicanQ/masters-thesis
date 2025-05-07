# What sweeps do I have in my DB?

List of some sweeps that have been done. It's possible that resolution or bounds are slighlty off.

## 3T

### 1D

### 2D

Ejs = np.arange(30, 80, 0.2)
Eints = np.arange(0, 0.5, 0.01)
Ec2=1, Ec3=1, Ej1=Ejs, Ej2=50, Ej3=50, Eint12=Eints, Eint23=0.2, Eint13=0
Ec2=1, Ec3=1, Ej1=Ejs, Ej2=50, Ej3=60, Eint12=Eints, Eint23=0.2, Eint13=0

Ej1s = np.arange(30, 80, 0.2)
Ej2s = np.arange(30, 80, 0.2)
Ej2=Ej2s, Ej1=Ej1s, Ej3=50, Eint12=0.1, Eint23=0.1, Eint13=0, Ec2=1, Ec3=1

jobs = collect_jobs(Ec2=1, Ec3=1, Ej1=Ejs, Ej2=Ejs, Ej3=50, Eint12=0.105, Eint23=0.105, Eint13=-0.002, k=7)

## 2T

### 1D

### 2D
