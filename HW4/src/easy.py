from functools import wraps
from multiprocessing import Process
from threading import Thread
from time import time


def timing(f):
    @wraps(f)
    def wrap(*args, **kw):
        ts = time()
        res = f(*args, **kw)
        te = time()
        return res, te - ts

    return wrap


@timing
def run_workers(function, args, workers_num, worker):
    workers = [worker(target=function, args=(args,)) for _ in range(workers_num)]
    for w in workers:
        w.start()
    for w in workers:
        w.join()


@timing
def run_sync(function, args, threads_num):
    for _ in range(threads_num):
        function(args)


def fibonacci(n):
    cur, prv = 1, 0
    fib_seq = [1]
    for _ in range(n - 1):
        cur, prv = cur + prv, cur
        fib_seq.append(cur)
    return fib_seq


def main():
    workers_num = 10
    n = 10 ** 5

    sync_time = run_sync(fibonacci, n, workers_num)[1]
    threads_time = run_workers(fibonacci, n, workers_num, Thread)[1]
    process_time = run_workers(fibonacci, n, workers_num, Process)[1]
    with open('../artifacts/easy_statistics.txt', 'w') as f:
        f.write(f'Test get the first {n} Fibonacci numbers {workers_num} times\n')
        f.write(f'Sync time: {sync_time} sec\n')
        f.write(f'Threads time: {threads_time} sec\n')
        f.write(f'Process time: {process_time} sec\n')


if __name__ == '__main__':
    main()
