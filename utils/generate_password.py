import string
import random

characterList = ""
characterList += string.digits
characterList += string.ascii_letters


def generate_password(length: int = 10):
    password = []
    for i in range(length):
        random_char = random.choice(characterList)
        password.append(random_char)
    return "".join(password)
