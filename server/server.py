# This server should recieve batches of parameters, run eigensolver and return the batch

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
from exact.twotransmon.zz.sweep import single_zz
import time

app = FastAPI()


class Job(BaseModel):
    Ec2: float
    Ej1: float
    Ej2: float
    Eint: float


class Data(BaseModel):
    jobs: list[Job]
    k: int


class Result(BaseModel):
    Ec2: float
    Ej1: float
    Ej2: float
    Eint: float
    zz: float
    zzGS: float
@app.get("/")
def hello():
    return "Hello!"

@app.post("/2T", response_model=list[Result])
def route(data: Data):
    resp = []
    t1 = time.time()
    if data.k < 1:
        raise HTTPException("k parameter too small")
    print("Recieved jobs: ", len(data.jobs))
    for job in data.jobs:
        zz, zzGS = single_zz(
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
    uvicorn.run(app, port=82,host="0.0.0.0")
