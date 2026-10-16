import json
import random


# Function to convert numbers to their English words (1 to 100)
def num_to_english(n):
    num_dict = {1: 'one', 2: 'two', 3: 'three', 4: 'four', 5: 'five', 6: 'six', 7: 'seven', 8: 'eight', 9: 'nine', 10: 'ten',
                11: 'eleven', 12: 'twelve', 13: 'thirteen', 14: 'fourteen', 15: 'fifteen', 16: 'sixteen', 17: 'seventeen', 18: 'eighteen', 19: 'nineteen',
                20: 'twenty', 30: 'thirty', 40: 'forty', 50: 'fifty', 60: 'sixty', 70: 'seventy', 80: 'eighty', 90: 'ninety'}

    if n <= 20:
        return num_dict[n]
    elif n < 100:
        tens, ones = divmod(n, 10)
        return num_dict[tens * 10] + ('' if ones == 0 else '-' + num_dict[ones])
    elif n == 100:
        return 'one-hundred'

# Generate random values for each key


def random_value():
    return random.choice([random.randint(0, 100), random.uniform(0, 100), ''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=5))])


# Create the JSON data
data = {}
for i in range(1, 101):
    key = num_to_english(i)
    data[key] = random_value()

# Save to a JSON file
file_path = '/mnt/data/random_data.json'
with open(file_path, 'w') as json_file:
    json.dump(data, json_file)

file_path
