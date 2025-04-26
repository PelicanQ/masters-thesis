from analysis.plot import grid3d
from exact.twotransmon.hamil import eig_clever
import numpy as np
from store.stores import StoreLevels2T

# now we check the lowest levels for some Eint
k = 13
Ejs = np.arange(30, 90, 2)
Ecs = np.arange(0.2, 1.5, 0.1)
# Ejs = np.arange(30, 90, 2)
# Ecs = np.arange(0.2, 1.5, 0.1)
Ej2 = 50
Eint = 0.1
for j, Ej1 in enumerate(Ejs):
    for i, Ec2 in enumerate(Ecs):
        vals = eig_clever(Ej1=Ej1, Ej2=Ej2, Eint=Eint, Ec2=Ec2, k=k, only_energy=True)
        StoreLevels2T.insert(Ej1=Ej1, Ej2=Ej2, Eint=Eint, Ec2=Ec2, levels=vals[:8])
# grid3d(
#     xx=Eints,
#     collection=collection,
#     params=Ejs,
#     param_name="Ej",
#     suptitle=f"How do levels vary with Eint?, k={k}",
#     xlabel="Eint",
#     ylabel="En(k)-E0(k)",
#     labels=[f"E{l}" for l in level_select],
#     marker=None,
# )
