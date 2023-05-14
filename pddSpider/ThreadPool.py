import concurrent.futures
import time

class ThreadPool:
    _instance = None

    def __new__(cls, num_threads):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.executor = concurrent.futures.ThreadPoolExecutor(num_threads)
        return cls._instance

    def submit(self, func, *args, **kwargs):
        return self.executor.submit(func, *args, **kwargs)

def worker(name):
    print(f'Thread: {name} started')
    time.sleep(1)
    print(f'Thread: {name} finished')

pool = ThreadPool(2)

for i in range(5):
    pool.submit(worker, i)

pool.executor.shutdown()
