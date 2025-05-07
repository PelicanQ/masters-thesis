# Here we manage numeric jobs
from exact.two.zz.zz import single_zz as zz2T
from exact.three.zz.zz import single_zz as zz3T
from exact.four.zz.zz import single_zz as zz4T
from exact.two.hamil import eig_clever as energy2T
from exact.three.hamil import eig_excitation_trunc as energy3T
from store.stores4T import Store_zz4T
import aiohttp
import asyncio
import timeit
from abc import abstractmethod


class HandlerBase:
    task: asyncio.Task

    def __init__(self, url):
        self.url = url

    @abstractmethod
    def local_run(self, job: dict) -> dict:
        pass

    def schedule(self, jobs):
        self.task = asyncio.create_task(self.run_batch_remote(jobs))

    async def submit(self, jobs: list[dict], batch_size: int):
        # testtime = timeit.timeit(lambda: self.local_run(jobs[0]), number=1)
        progress = 0  # index of next job to be run
        numjobs = len(jobs)
        # print(f"Num jobs: {numjobs}. Est time: {round(numjobs*testtime)} s")

        results = []
        if numjobs > batch_size:
            self.schedule(jobs[progress : progress + batch_size])
            progress += batch_size
            await asyncio.sleep(0)
        else:
            print("Running all locally")
            return [self.local_run(j) for j in jobs]

        while progress < numjobs:
            res = await asyncio.to_thread(lambda: self.local_run(jobs[progress]))
            results.append(res)
            progress += 1
            print(f"local done. Progress: {progress}/{numjobs}")
            if progress >= numjobs:
                break
            await asyncio.sleep(0)
            if self.task.done():
                try:
                    res = self.task.result()
                    results.extend(res)
                except Exception as e:
                    print("Remote batch failed!", e)  # accept missing data and continue
                self.schedule(jobs[progress : progress + batch_size])
                progress += batch_size
                await asyncio.sleep(0)

        res = await self.task
        results.extend(res)
        print(f"All done. Num results: {len(results)}/{numjobs}")
        return results

    async def run_batch_remote(self, jobs: list[dict]):
        # send a batch of jobs to remote server, await, then return results
        # this method should include retries
        json = {"jobs": jobs}
        if hasattr(self, "level_select"):
            json["level_select"] = self.level_select
        async with aiohttp.ClientSession() as session:
            print(json)
            post = session.post(self.url, json=json)
            async with post as response:
                response = await response.json()
                return response


class Handler2T(HandlerBase):
    def local_run(self, job: dict):
        current = job.copy()
        zz, zzGS = zz2T(**current)
        current.update([("zz", zz), ("zzGS", zzGS)])
        return current


class Handler2TEnergy(HandlerBase):
    def __init__(self, url, level_select):
        super().__init__(url)
        self.level_select = level_select

    def local_run(self, job: dict):
        current = job.copy()
        levels = energy2T(**current, only_energy=True)
        current.update([("levels", levels[self.level_select].tolist())])
        return current


class Handler3TEnergy(HandlerBase):
    def __init__(self, url, level_select):
        super().__init__(url)
        self.level_select = level_select

    def local_run(self, job: dict):
        current = job.copy()
        levels = energy3T(**current, only_energy=True)
        current.update([("levels", levels[self.level_select].tolist())])
        return current


class Handler3T(HandlerBase):
    async def test_remote(self):
        print("Testing remote")
        res = await self.run_batch_remote(
            [{"k": 2, "Ec2": 1, "Ec3": 1, "Ej1": 50, "Ej2": 50, "Ej3": 50, "Eint12": 0.1, "Eint23": 0.1, "Eint13": 0.1}]
        )
        print("Remote done")
        return res

    def local_run(self, job: dict):
        current = job.copy()
        zz12, zz23, zz13, zzz = zz3T(**current)
        current.update([("zzGS12", zz12), ("zzGS23", zz23), ("zzGS13", zz13), ("zzzGS", zzz)])
        return current


class Handler4T(HandlerBase):
    def local_run(self, job: dict):
        current = job.copy()
        results = zz4T(**current)
        current.update([(val, results[val]) for val in Store_zz4T.all_vals])
        return current


if __name__ == "__main__":
    h = Handler4T("http://127.0.0.1:81/4T")
    d1 = {"Ej1": 1, "Ej2": 1, "Ec2": 1, "Eint": 1, "k": 10}
    asyncio.run(h.submit([d1 for _ in range(20)]))
