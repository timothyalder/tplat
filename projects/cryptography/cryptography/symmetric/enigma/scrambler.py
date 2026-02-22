import random
from typing import Optional, List, Union, Tuple
from collections import deque

from cryptography.core.alphabet import Alphabet


class Scrambler:

    def __init__(
        self,
        mod: int = 1,
        alphabet: Union[List[str], List[Tuple[str, float]], Alphabet, None] = None,
        seed: Optional[int] = None,
    ):
        rng = random.Random(seed) if seed is not None else random.Random()
        alphabet = Alphabet(alphabet)
        shuffled = Alphabet(alphabet.alphabet)
        rng.shuffle(shuffled.alphabet)
        self.substitution_mapping = {
            plaintext: ciphertext for plaintext, ciphertext in zip(alphabet.alphabet, shuffled.alphabet)
        }
        self.mod = mod

    def __call__(self, m: str):
        # Record initial state
        initial_substitution_mapping = self.substitution_mapping.copy()
        # Perform the encryption, shifting the cipher every mod characters
        c = ""
        for i, plaintext in enumerate(m.upper()):
            if i % self.mod == 0:
                self.shift(i=1)
            c += self.substitution_mapping[plaintext]
        # Make sure to reset the initial state after performing the encryption
        self.substitution_mapping = initial_substitution_mapping
        return c

    def shift(self, i: int = 1):
        keys = list(self.substitution_mapping.keys())
        values = deque(self.substitution_mapping.values())
        values.rotate(i)
        self.substitution_mapping = dict(zip(keys, values))
