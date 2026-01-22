from typing import List
from collections import deque


def determine_i(m: str, c: str, alphabet: List[str]=None):
    alphabet = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"] if alphabet is None else alphabet
    assert all(char.upper() in alphabet for char in [m, c]) 
    return alphabet.index(m.upper()) - alphabet.index(c.upper())


def caesar_shift(m: str, i: int, alphabet: List[str]=None):
    alphabet = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"] if alphabet is None else alphabet
    shifted = deque(alphabet.copy())
    shifted.rotate(i)
    substitution_mapping = dict(zip(alphabet, shifted))
    c = "".join([substitution_mapping[plaintext] for plaintext in m.upper()])
    return c

if __name__ == "__main__":
    i = determine_i(m="I", c="O")
    print(i)
    m = "DAJSDA"
    c = caesar_shift(m=m, i=i)
