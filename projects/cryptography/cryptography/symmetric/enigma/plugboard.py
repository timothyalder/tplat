from typing import Optional, List
import random

class Plugboard(list):
    
    def __new__(cls, alphabet: Optional[List[str]]=None, seed: Optional[int]=None):
        rng = random.Random(seed) if seed is not None else random.Random()
        alphabet = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9"] if alphabet is None else alphabet
        p = rng.sample(population=alphabet, k=6)
        return list((p[2*i], p[2*i+1]) for i in range(len(p)//2))