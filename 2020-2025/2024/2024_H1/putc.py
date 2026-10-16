import random
import time

import pyautogui

pyautogui.click(x=750, y=980)

words = [
    "פוצי",
    "בובי",
    "אוהב אותך",
    "מותיק",
    "נשמה",
    "כוכבה",
    "אהובה שלי",
    "יפה שלי",
    "בייבי",
    "מאמי",
]


def hebrew_to_english(hebrew_text):
    # Define a dictionary mapping Hebrew characters to their QWERTY English counterparts
    hebrew_to_english_mapping = {
        "ק": "q",
        "ו": "w",
        "ר": "e",
        "ת": "r",
        "י": "t",
        "ן": "y",
        "ם": "u",
        "פ": "i",
        "ש": "o",
        "ד": "p",
        "ג": "a",
        "כ": "s",
        "ע": "d",
        "צ": "f",
        "ח": "g",
        "ל": "h",
        "ך": "j",
        "ף": "k",
        "ז": "l",
        "ס": "z",
        "ב": "x",
        "ה": "c",
        "נ": "v",
        "מ": "b",
        "צ": "n",
        "ת": "m",
        "ץ": ",",
    }

    # Convert Hebrew text to English using the mapping
    english_text = ""
    for char in hebrew_text:
        # If the character is in the mapping, use the corresponding English character, otherwise keep the character unchanged
        english_text += hebrew_to_english_mapping.get(char, char)

    return english_text


for i in range(1, 11):
    word = random.choice(words)
    print(word)
    word = hebrew_to_english(word)
    print(word)
    pyautogui.typewrite(word)
    pyautogui.press("enter")
    time.sleep(0.1)
