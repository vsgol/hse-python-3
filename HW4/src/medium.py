import math
import multiprocessing as mp
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from time import time

from easy import timing


def integrate(f, a, b, n_iter=1000):
    start_time = time()
    acc = 0
    step = (b - a) / n_iter
    for i in range(n_iter):
        acc += f(a + i * step)
    acc *= step
    end_time = time()
    return acc, start_time, end_time, a, b


@timing
def integrate_parallel(f, a, b, n_iter, n_jobs, pool, logs_file):
    logs_file.write(f'Integrate with {n_jobs} workers:\n')
    tasks = []
    step = (b - a) / n_jobs
    with pool(max_workers=n_jobs) as executor:
        res = 0
        for i in range(n_jobs):
            tasks.append(executor.submit(integrate,
                                         f, a + i * step, a + (i + 1) * step, n_iter // n_jobs))
        for t in tasks:
            acc, start_time, end_time, a_, b_ = t.result()
            res += acc
            logs_file.write(
                f'\tIntegrating from {start_time} to {end_time}, computing time {end_time - start_time}\n'
                f'\t            part from {a_} to {b_}, {n_iter // n_jobs} iterations\n'
            )
    logs_file.write(f'Result: {res}\n')
    return res


def run_integration(function, a, b, n_iter, pool, pool_name, file, logs_file):
    file.write(f'{pool_name} time:\n')
    for n_jobs in range(1, 2 * mp.cpu_count() + 1):
        file.write(f'Number of workers {n_jobs}\n')
        res, work_time = integrate_parallel(function, a, b, n_iter, n_jobs, pool, logs_file)
        file.write(f'Result {res}\n')
        file.write(f'Time {work_time}\n\n')
        logs_file.write(f'Time {work_time}\n\n')


def main():
    n_iter = 10 ** 7
    with open('../artifacts/medium_logs.txt', "w") as logs_file, \
            open('../artifacts/medium_statistics.txt', "w") as file:
        run_integration(math.cos, 0, math.pi / 2, n_iter, ProcessPoolExecutor, 'Processes', file, logs_file)
        run_integration(math.cos, 0, math.pi / 2, n_iter, ThreadPoolExecutor, 'Threads', file, logs_file)


if __name__ == '__main__':
    main()
