import random
from typing import Optional, List
from collections import deque


class Scrambler:
    
    def __init__(self, mod: int=1, alphabet: Optional[List[str]]=None, seed: Optional[int]=None):
        rng = random.Random(seed) if seed is not None else random.Random()
        alphabet = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9"] if alphabet is None else alphabet
        shuffled = alphabet.copy()
        rng.shuffle(shuffled)
        self.substitution_mapping = {plaintext: ciphertext for plaintext, ciphertext in zip(alphabet, shuffled)} 
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
    
    def shift(self, i: int=1):
        keys = list(self.substitution_mapping.keys())
        values = deque(self.substitution_mapping.values())
        values.rotate(i)
        self.substitution_mapping = dict(zip(keys, values))
