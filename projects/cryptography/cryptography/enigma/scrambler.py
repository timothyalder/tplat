import random
from typing import Optional, List

class Scrambler:
    
    def __init__(self, alphabet: Optional[List[str]]=None, seed: Optional[int]=None):
        rng = random.Random(seed) if seed is not None else random.Random()
        alphabet = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9"] if alphabet is None else alphabet
        shuffled = alphabet.copy()
        rng.shuffle(shuffled)
        self.substitution_mapping = {plaintext: ciphertext for plaintext, ciphertext in zip(alphabet, shuffled)}
        
    def __call__(self, m: str):
        c = "".join([self.substitution_mapping[plaintext] for plaintext in m.upper()])
        return c
