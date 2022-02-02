def fibonacci(n):
    res = [0, 1]
    for _ in range(n-1):
        res.append(res[-1] + res[-2])
    return res[1:n+1]