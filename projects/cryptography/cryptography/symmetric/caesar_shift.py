from typing import List, Union, Tuple
from collections import deque

from cryptography.core.alphabet import Alphabet


def determine_i(m: str, c: str, alphabet: Union[List[str], List[Tuple[str,float]], Alphabet, None]=None):
    alphabet = Alphabet(alphabet=alphabet).alphabet
    assert all(char.upper() in alphabet for char in [m, c]) 
    return alphabet.index(m.upper()) - alphabet.index(c.upper())


def caesar_shift(m: str, i: int, alphabet: Union[List[str], List[Tuple[str,float]], Alphabet, None]=None):
    alphabet = Alphabet(alphabet=alphabet).alphabet
    shifted = Alphabet(alphabet=alphabet)
    shifted.rotate(i)
    substitution_mapping = dict(zip(alphabet, shifted.alphabet))
    c = "".join([substitution_mapping[plaintext] for plaintext in m.upper()])
    return c

if __name__ == "__main__":
    i = determine_i(m="I", c="O")
    print(i)
    m = "DAJSDA"
    c = caesar_shift(m=m, i=i)
    print(c)
