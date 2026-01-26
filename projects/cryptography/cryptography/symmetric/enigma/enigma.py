from typing import Optional, List

from cryptography.symmetric.enigma.scrambler import Scrambler
from cryptography.symmetric.enigma.plugboard import Plugboard


class Enigma:

    def __init__(
        self, alphabet: Optional[List[str]] = None, seed: Optional[int] = None
    ):
        alphabet = (
            [
                "A",
                "B",
                "C",
                "D",
                "E",
                "F",
                "G",
                "H",
                "I",
                "J",
                "K",
                "L",
                "M",
                "N",
                "O",
                "P",
                "Q",
                "R",
                "S",
                "T",
                "U",
                "V",
                "W",
                "X",
                "Y",
                "Z",
                "0",
                "1",
                "2",
                "3",
                "4",
                "5",
                "6",
                "7",
                "8",
                "9",
            ]
            if alphabet is None
            else alphabet
        )
        self.p = Plugboard(alphabet=alphabet, seed=seed)
        self.s1 = Scrambler(mod=1, alphabet=alphabet, seed=seed)
        self.s2 = Scrambler(mod=len(alphabet), alphabet=alphabet, seed=seed)
        self.s3 = Scrambler(mod=len(alphabet) ** 2, alphabet=alphabet, seed=seed)

    def __call__(self, m: str):
        m = m.replace(" ", "")
        for p_in, p_out in self.p:  # Fix this
            c0 = m.replace(p_in, p_out)
        c1 = self.s1(c0)
        c2 = self.s2(c1)
        c3 = self.s3(c2)
        return c3


if __name__ == "__main__":
    m = "Hello World"
    seed = 42
    e = Enigma(seed=seed)
    c = e(m)
    print(c)
