from typing import List, Union, Tuple
from collections import deque

from cryptography.core.alphabet import Alphabet


def determine_i(m: str, c: str, alphabet: Union[List[str], List[Tuple[str,float]], Alphabet, None]=None):
    alphabet = Alphabet(alphabet=alphabet).alphabet
    assert all(char.upper() in alphabet for char in [m, c])
    return alphabet.index(m.upper()) - alphabet.index(c.upper())


def estimate_i_from_pdf(m: Alphabet, c: Alphabet):
    assert len(m) == len(c), "Error! Mismatch in reference and ciphertext distribution lengths."
    plaintext_pdf = m.probabilities
    ciphertext_pdf = deque(c.probabilities)
    # TODO: Refactor this to be a proper optimisation loop, rather than naive exhaustive search
    losses = []
    for idx in range(len(plaintext_pdf)):
        ciphertext_pdf.rotate(idx)
        loss = abs(sum([plaintext_prob - ciphertext_prob for plaintext_prob, ciphertext_prob in zip(plaintext_pdf, ciphertext_pdf)]))
        losses.append(loss)
    return losses.index(min(losses))


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
