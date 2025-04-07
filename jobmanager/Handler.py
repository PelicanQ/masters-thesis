# Here we manage numeric jobs
from exact.twotransmon.zz.sweep import single_zz
import aiohttp
import asyncio
import timeit


class Handler:
    task: asyncio.Task

    def __init__(self, url, k):
        self.url = url
        self.k = k

    def local_run(self, job: dict):
        current = job.copy()
        zz, zzGS = single_zz(**current, k=self.k)
        current.update([("zz", zz), ("zzGS", zzGS)])
        return current

    def schedule(self, jobs):
        self.task = asyncio.create_task(self.run_batch_remote(jobs))

    async def submit(self, jobs: list[dict], batch_size: int):
        testtime = timeit.timeit(lambda: self.local_run(jobs[0]), number=1)
        progress = 0  # index of next job to be run
        numjobs = len(jobs)
        print(f"Num jobs: {numjobs}. Est time: {round(numjobs*testtime)} s")

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
                    print("Remote batch failed!")
                    print(e)  # accept missing data and continue
                self.schedule(jobs[progress : progress + batch_size])
                progress += batch_size
                await asyncio.sleep(0)

        res = await self.task
        print("residual task done")
        results.extend(res)
        print(f"All done. Num results: {len(results)}/{numjobs}")
        return results

    async def run_batch_remote(self, jobs: list[dict]):
        # send a batch of jobs to remote server, await, then return results
        # this method should include retries
        async with aiohttp.ClientSession() as session:
            post = session.post(self.url, json={"jobs": jobs, "k": self.k})
            async with post as response:
                response = await response.json()
                return response
            # try:
            # except aiohttp.ClientError as e:
            #     print("Client error: ", e)
            # except asyncio.TimeoutError as e:
            #     print("Timeout error", e)
            # except Exception as e:
            #     print("Unknown error", e)


if __name__ == "__main__":
    h = Handler("http://127.0.0.1:81/2T")
    d1 = {"Ej1": 1, "Ej2": 1, "Ec2": 1, "Eint": 1}
    asyncio.run(h.submit([d1 for _ in range(20)], 4, 13))
