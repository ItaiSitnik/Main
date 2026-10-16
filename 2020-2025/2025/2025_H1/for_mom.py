total = 40004
values = {
    1: 12254,
    2: 6609,
    3: 5091,
    4: 4012,
    5: 3356,
    6: 3502,
    7: 2579,
    8: 2601,
}

assert sum(values.values()) == total, "Sum mismatch!"

for k in sorted(values):
    value = values[k]
    percent = value / total * 100
    print(f"{k:<1} {value:<5} {percent:>4.3f}%")
