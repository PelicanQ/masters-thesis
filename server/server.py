# This server should recieve batches of parameters, run eigensolver and return the batch

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
from exact.twotransmon.zz.zz import single_zz as zz2T
from exact.threetransmon.zz.zz import single_zz as zz3T, single_zz_energy as zz3T_energy
import time

app = FastAPI()


class Job2T(BaseModel):
    Ec2: float
    Ej1: float
    Ej2: float
    Eint: float


class Data2T(BaseModel):
    jobs: list[Job2T]
    k: int


class Result2T(BaseModel):
    Ec2: float
    Ej1: float
    Ej2: float
    Eint: float
    zz: float
    zzGS: float


class Job3T(BaseModel):
    Ec2: float
    Ec3: float
    Ej1: float
    Ej2: float
    Ej3: float
    Eint12: float
    Eint23: float
    Eint13: float
    k: int


class Data3TEnergy(BaseModel):
    jobs: list[Job3T]
    level_select: list[int]


class Data3T(BaseModel):
    jobs: list[Job3T]


class Result3TEnergy(BaseModel):
    Ec2: float
    Ec3: float
    Ej1: float
    Ej2: float
    Ej3: float
    Eint12: float
    Eint23: float
    Eint13: float
    levels: list[float]


class Result3T(BaseModel):
    Ec2: float
    Ec3: float
    Ej1: float
    Ej2: float
    Ej3: float
    Eint12: float
    Eint23: float
    Eint13: float
    zzGS12: float
    zzGS23: float
    zzGS13: float
    zzzGS: float


@app.get("/")
def hello():
    return "Hello!"


@app.post("/3T/energy", response_model=list[Result3TEnergy])
def three(data: Data3TEnergy):
    resp = []
    t1 = time.perf_counter()
    print("Recieved jobs: ", len(data.jobs))
    for job in data.jobs:
        dic = job.model_dump()
        levels = zz3T_energy(**dic)
        dic.update([("levels", levels[data.level_select])])
        resp.append(dic)
    print("Time taken:", time.perf_counter() - t1)
    return resp


@app.post("/3T", response_model=list[Result3T])
def three(data: Data3T):
    resp = []
    t1 = time.perf_counter()
    if data.k < 1:
        raise HTTPException("k parameter too small")
    print("Recieved jobs: ", len(data.jobs))
    for job in data.jobs:
        dic = job.model_dump()
        zz12, zz23, zz13, zzz = zz3T(**dic)
        dic.update([("zzGS12", zz12), ("zzGS23", zz23), ("zzGS13", zz13), ("zzzGS", zzz)])
        resp.append(dic)
    print("Time taken:", time.perf_counter() - t1)
    return resp


@app.post("/2T", response_model=list[Result2T])
def two(data: Data2T):
    resp = []
    t1 = time.time()
    if data.k < 1:
        raise HTTPException("k parameter too small")
    print("Recieved jobs: ", len(data.jobs))
    for job in data.jobs:
        zz, zzGS = zz2T(
            Ej1=job.Ej1,
            Ej2=job.Ej2,
            Ec2=job.Ec2,
            Eint=job.Eint,
            k=data.k,
        )
        dic = job.model_dump()
        dic.update([("zz", zz), ("zzGS", zzGS)])
        resp.append(dic)
    print("Time taken:", time.time() - t1)
    return resp


if __name__ == "__main__":
    uvicorn.run(app, port=81, host="0.0.0.0")
