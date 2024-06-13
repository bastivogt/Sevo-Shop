from random import choice
from string import digits, ascii_letters

def create_token(length=27):
    s = ''
    for i in range(length):
        s += choice(digits + ascii_letters)
    return s