def fibonacci(n):
    fib_seq = [0, 1]
    for _ in range(n - 1):
        prev = fib_seq[-1]
        prev2 = fib_seq[-2]
        fib_seq.append(prev + prev2)
    return fib_seq[1:n + 1]
