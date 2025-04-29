# This server should recieve batches of parameters, run eigensolver and return the batch

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
from exact.two.zz.zz import single_zz as zz2T
from exact.three.zz.zz import single_zz as zz3T
from exact.three.hamil import eig_excitation_trunc as eig3T
from exact.two.hamil import eig_clever as eig2T
import time

app = FastAPI()


class Job2T(BaseModel):
    k: int
    Ec2: float
    Ej1: float
    Ej2: float
    Eint: float


class Data2T(BaseModel):
    jobs: list[Job2T]


class Result2T(BaseModel):
    k: int
    Ec2: float
    Ej1: float
    Ej2: float
    Eint: float
    zz: float
    zzGS: float


class Job3T(BaseModel):
    k: int
    Ec2: float
    Ec3: float
    Ej1: float
    Ej2: float
    Ej3: float
    Eint12: float
    Eint23: float
    Eint13: float


class Data2TEnergy(BaseModel):
    jobs: list[Job2T]
    level_select: list[int]


class Data3TEnergy(BaseModel):
    jobs: list[Job3T]
    level_select: list[int]


class Data3T(BaseModel):
    jobs: list[Job3T]


class Result2TEnergy(BaseModel):
    k: int
    Ec2: float
    Ej1: float
    Ej2: float
    Eint: float
    levels: list[float]


class Result3TEnergy(BaseModel):
    k: int
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
    k: int
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
    total_t = time.perf_counter()
    print("Recieved jobs: ", len(data.jobs))
    for job in data.jobs:
        dic = job.model_dump()
        t1 = time.perf_counter()
        levels = eig3T(**dic, only_energy=True)
        print("Time job: ", time.perf_counter() - t1)
        dic.update([("levels", levels[data.level_select])])
        resp.append(dic)
    print("Total time:", time.perf_counter() - total_t)
    return resp


@app.post("/3T", response_model=list[Result3T])
def three(data: Data3T):
    resp = []
    total_t = time.perf_counter()
    print("Recieved jobs: ", len(data.jobs))
    for job in data.jobs:
        dic = job.model_dump()
        t1 = time.perf_counter()
        zz12, zz23, zz13, zzz = zz3T(**dic)
        dic.update([("zzGS12", zz12), ("zzGS23", zz23), ("zzGS13", zz13), ("zzzGS", zzz)])
        print("Job time: ", time.perf_counter() - t1)
        resp.append(dic)
    print("Total time:", time.perf_counter() - total_t)
    return resp


@app.post("/2T/energy", response_model=list[Result2TEnergy])
def two(data: Data2TEnergy):
    resp = []
    # total_t = time.perf_counter()
    # print("Recieved jobs: ", len(data.jobs))
    for job in data.jobs:
        dic = job.model_dump()
        # t1 = time.perf_counter()
        levels = eig2T(**dic, only_energy=True)
        # print("Time job: ", time.perf_counter() - t1)
        dic.update([("levels", levels[data.level_select])])
        resp.append(dic)
    # print("Total time:", time.perf_counter() - total_t)
    return resp


@app.post("/2T", response_model=list[Result2T])
def two(data: Data2T):
    resp = []
    t1 = time.time()
    print("Recieved jobs: ", len(data.jobs))
    for job in data.jobs:
        dic = job.model_dump()
        zz, zzGS = zz2T(**dic)
        dic.update([("zz", zz), ("zzGS", zzGS)])
        resp.append(dic)
    print("Time taken:", time.time() - t1)
    return resp


if __name__ == "__main__":
    uvicorn.run(app, port=81, host="0.0.0.0")
