import random
from typing import Optional, List
from collections import deque


class Scrambler:
    
    def __init__(self, divisor: int=1, alphabet: Optional[List[str]]=None, seed: Optional[int]=None):
        rng = random.Random(seed) if seed is not None else random.Random()
        alphabet = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9"] if alphabet is None else alphabet
        shuffled = alphabet.copy()
        rng.shuffle(shuffled)
        self.substitution_mapping = {plaintext: ciphertext for plaintext, ciphertext in zip(alphabet, shuffled)}
        self.divisor = divisor
        
    def __call__(self, m: str):
        c = ""
        for i, plaintext in enumerate(m.upper()):
            if i // self.divisor == 0:
                self.shift()
            c += self.substitution_mapping[plaintext]
        return c
    
    def shift(self):
        keys = list(self.substitution_mapping.keys())
        values = deque(self.substitution_mapping.values())
        values.rotate(1)
        self.substitution_mapping = dict(zip(keys, values))
