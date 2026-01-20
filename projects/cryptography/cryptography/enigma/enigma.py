from typing import Optional

from cryptography.enigma.scrambler import Scrambler
from cryptography.enigma.plugboard import Plugboard


class Enigma:
    
    def __init__(self, seed: Optional[int]=None):
        self.p = Plugboard(seed=seed)
        self.s1 = Scrambler(seed=seed)
        self.s2 = Scrambler(seed=seed)
        self.s3 = Scrambler(seed=seed)
    
    def __call__(self, m: str):
        m = m.replace(" ", "")
        for p_in, p_out in self.p:
            c0 = m.replace(p_in, p_out)
        c1 = self.s1(c0)
        c2 = self.s2(c1)
        c3 = self.s3(c2)
        return c3
    
if __name__ == "__main__":
    m = "Hello World"
    e = Enigma()
    c = e(m)
    print(c)