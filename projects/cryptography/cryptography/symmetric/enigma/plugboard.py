from typing import Optional, List, Union, Tuple
import random

from cryptography.core.alphabet import Alphabet


class Plugboard(list):

    def __new__(cls, alphabet: Union[List[str], List[Tuple[str, float]], Alphabet, None] = None, seed: Optional[int] = None):
        alphabet = Alphabet(alphabet)
        rng = random.Random(seed) if seed is not None else random.Random()
        p = rng.sample(population=alphabet.alphabet, k=6)
        return list((p[2 * i], p[2 * i + 1]) for i in range(len(p) // 2))
