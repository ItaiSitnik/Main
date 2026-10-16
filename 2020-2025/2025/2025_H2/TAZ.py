import random

def calculate_check_digit(id_digits):
    weights = [1, 2] * 4  # [1, 2, 1, 2, 1, 2, 1, 2]
    total = 0
    for digit, weight in zip(id_digits, weights):
        product = digit * weight
        if product > 9:
            product = product // 10 + product % 10
        total += product
    check_digit = (10 - (total % 10)) % 10
    return check_digit

def generate_israeli_id():
    id_digits = [random.randint(0, 9) for _ in range(8)]
    id_digits = [2,0,7,4,3,2,9,4]
    check_digit = calculate_check_digit(id_digits)
    full_id = id_digits + [check_digit]
    return ''.join(map(str, full_id))

# דוגמה לשימוש
print(generate_israeli_id())
