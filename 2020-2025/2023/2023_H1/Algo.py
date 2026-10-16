conversion_map = {
    1: 2, 2: 5, 3: 10, 4: 13,
    5: 35, 6: 51, 7: 101, 8: 103
}

result = {k: 0 for k in range(1, 9)}

Sum, n = 31081, 8
cache = [[-1 for _ in range(Sum + 1)] for _ in range(n + 1)]


def F(S, k):
    if S < 0:
        return float('inf')

    if cache[k][S] != -1:
        return cache[k][S]

    if S == 0:
        cache[k][S] = 0
        return 0

    if S > 0 and k == 0:
        cache[k][S] = float('inf')
        return float('inf')

    dont_use = F(S, k - 1)
    use = F(S - conversion_map[k], k) + 1

    cache[k][S] = min(use, dont_use)
    return min(use, dont_use)


def gen_result(S, k):
    if S == 0 or k == 0:
        return

    if F(S, k) == F(S, k - 1):
        gen_result(S, k - 1)
    else:
        result[k] += 1
        gen_result(S - conversion_map[k], k)


# calculate all cache
for x in range(0, Sum + 1):
    for y in range(0, n + 1):
        F(x, y)
print(f'number of coins needed: {cache[n][Sum]}')

# infer result
gen_result(Sum, n)
print('result: ')
for k, number in result.items():
    print(f'{k}. {number:3} of coins of type {k} '
          f'(with value {conversion_map[k]:3}) are needed')
