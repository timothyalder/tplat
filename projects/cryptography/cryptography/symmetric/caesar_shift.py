from typing import List, Union, Tuple

from cryptography.core.alphabet import Alphabet


def caesar_shift(
    m: str,
    i: int,
    alphabet: Union[List[str], List[Tuple[str, float]], Alphabet, None] = None,
):
    alphabet = Alphabet(alphabet=alphabet).alphabet
    shifted = Alphabet(alphabet=alphabet)
    shifted.rotate(i)
    substitution_mapping = dict(zip(alphabet, shifted.alphabet))
    c = "".join([substitution_mapping[plaintext] for plaintext in m.upper()])
    return c
