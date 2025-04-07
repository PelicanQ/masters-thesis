# This server should recieve batches of parameters, run eigensolver and return the batch

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
from exact.twotransmon.zz.zz import single_zz as zz2T
from exact.threetransmon.zz.zz import single_zz as zz3T
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
    Ej1: float
    Ej2: float
    Eint: float


class Data3T(BaseModel):
    jobs: list[Job3T]
    k: int


class Result3T(BaseModel):
    Ec2: float
    Ec3: float
    Ej1: float
    Ej2: float
    Ej3: float
    Eint12: float
    Eint23: float
    Eint13: float
    zz12: float
    zz23: float
    zz13: float
    zzz: float


@app.get("/")
def hello():
    return "Hello!"


@app.post("/3T", response_model=list[Result3T])
def three(data: Data3T):
    resp = []
    t1 = time.time()
    if data.k < 1:
        raise HTTPException("k parameter too small")
    print("Recieved jobs: ", len(data.jobs))
    for job in data.jobs:
        zz12,zz23,zz13, zzz = zz3T(
            Ej1=job.Ej1,
            Ej2=job.Ej2,
            Ej3=job.Ej3,
            Ec2=job.Ec2,
            Ec3=job.Ec3,
            Eint12=job.Eint12,
            Eint23=job.Eint23,
            Eint13=job.Eint13,
            k=data.k,
        )
        dic = job.model_dump()
        dic.update([("zzGS12", zz12), ("zzGS23", zz23),("zzGS13", zz13),("zzzGS", zzz)])
        resp.append(dic)
    print("Time taken:", time.time() - t1)
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
