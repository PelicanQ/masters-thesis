from store.models import ZZ3T

tol = 3e-2
q = ZZ3T.select().where(
    ZZ3T.zzGS12.between(-tol, tol)
    | ZZ3T.zzGS23.between(-tol, tol)
    | ZZ3T.zzGS13.between(-tol, tol)
    | ZZ3T.zzzGS.between(-tol, tol)
)
print(q)
for e in q:
    print(e.zzGS12)
