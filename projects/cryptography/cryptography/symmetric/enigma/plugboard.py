from typing import Optional, List, Union, Tuple
import random

from cryptography.core.alphabet import Alphabet


class Plugboard(dict):

    def __new__(cls, alphabet: Union[List[str], List[Tuple[str, float]], Alphabet, None] = None, seed: Optional[int] = None):
        alphabet = Alphabet(alphabet)
        rng = random.Random(seed) if seed is not None else random.Random()
        p = rng.sample(population=alphabet.alphabet, k=6)
        substitution_mapping = {plaintext: plaintext for plaintext in alphabet.alphabet}
        for plaintext, ciphertext in list(zip(p[::2], p[1::2])):
            substitution_mapping[plaintext] = ciphertext
            substitution_mapping[ciphertext] = plaintext
        return substitution_mapping