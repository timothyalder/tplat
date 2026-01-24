from typing import List, Tuple, Union
from collections import deque

import matplotlib.pyplot as plt
from matplotlib.figure import Figure


class Alphabet:

    def __new__(
        cls, alphabet: Union["Alphabet", List[str], List[Tuple[str, float]], None] = None
    ):
        if isinstance(alphabet, Alphabet):
            return alphabet
        return super().__new__(cls)

    def __init__(self, alphabet: Union[List[str], List[Tuple[str]], None] = None) -> None:
        if isinstance(alphabet, Alphabet):
            return
        # https://pi.math.cornell.edu/~mec/2003-2004/cryptography/subs/frequencies.html
        self.canonical_alphabet, self.canonical_probabilities = map(list, zip(*[
            ("A", 8.12),
            ("B", 1.49),
            ("C", 2.71),
            ("D", 4.32),
            ("E", 12.02),
            ("F", 2.30),
            ("G", 2.03),
            ("H", 5.92),
            ("I", 7.31),
            ("J", 0.10),
            ("K", 0.69),
            ("L", 3.98),
            ("M", 2.61),
            ("N", 6.95),
            ("O", 7.68),
            ("P", 1.82),
            ("Q", 0.11),
            ("R", 6.02),
            ("S", 6.28),
            ("T", 9.10),
            ("U", 2.88),
            ("V", 1.11),
            ("W", 2.09),
            ("X", 0.17),
            ("Y", 2.11),
            ("Z", 0.07),
        ]))
        self.canonical_index = {
            plaintext: idx for idx, plaintext in enumerate(self.canonical_alphabet)
        }
        if alphabet is None:
            self.alphabet = self.canonical_alphabet
            self.probabilities = [prob/100 for prob in self.canonical_probabilities]
        elif isinstance(alphabet[0], tuple):
            self.alphabet, self.propabilities = map(list, zip(*alphabet))
        else:
            self.alphabet = alphabet
            self.probabilities = [self.canonical_probabilities[self.canonical_index[plaintext]] for plaintext in alphabet]
            
    def __len__(self) -> int:
        return len(self.alphabet)
            
    def __str__(self) -> str:
        return str(list(zip(self.alphabet, self.probabilities)))
    
    def __getitem__(self, i: int):
        return (self.alphabet[i], self.probabilities[i])
    
    def index(self, *args, **kwargs):
        return self.alphabet.index(*args, **kwargs)
        
    def rotate(self, i: int):
        for attr in ["alphabet", "probabilities"]:
            shifted = deque(self.__getattribute__(attr).copy())
            shifted.rotate(i)
            self.__setattr__(attr, list(shifted))

    def calculate_distribution(self, m: str) -> None:
        frequencies = [m.count(plaintext)/len(m) for plaintext in self.alphabet]
        self.alphabet, self.probabilities = map(list, zip(*sorted(list(zip(self.alphabet, frequencies)), key=lambda x: x[1], reverse=True)))

    def canonical_sort(self) -> None:
        def sort_key(item):
            ch = item[0]
            if ch in self.canonical_index:
                return (0, self.canonical_index[ch])
            else:
                return (1, ch)

        self.alphabet, self.probabilities = map(
            list, zip(*sorted(zip(self.alphabet, self.probabilities), key=sort_key))
        )

    def frequency_sort(self) -> None:
        self.alphabet, self.probabilities = map(
            list,
            zip(
                *sorted(
                    list(zip(self.alphabet, self.probabilities)),
                    key=lambda x: x[1],
                    reverse=True,
                )
            ),
        )

    def plot_distribution(self) -> Figure:
        fig, ax = plt.subplots()
        ax.plot(range(len(self.alphabet)), self.probabilities)
        ax.set_xticks(range(len(self.alphabet)))
        ax.set_xticklabels(self.alphabet)
        ax.set_xlabel("Alphabet")
        ax.set_ylabel("Frequency")
        ax.grid(True)
        plt.close(fig)
        return fig
    
    def plot_distributions(self, alphabets: Union["Alphabet", List["Alphabet"]]) -> Figure:
        if isinstance(alphabets, Alphabet):
            alphabets = [alphabets]
        alphabets.insert(0, self)
            
        fig, ax = plt.subplots()
        for idx, alphabet in enumerate(alphabets): 
            ax.plot(range(len(alphabet.alphabet)), alphabet.probabilities, label=f"{alphabet.__class__.__name__} ({idx})") 
        ax.set_xticks(range(len(self.alphabet)))
        ax.set_xticklabels(self.alphabet)
        ax.set_xlabel("Alphabet")
        ax.set_ylabel("Frequency")
        ax.legend()
        ax.grid(True)
        plt.close(fig)
        return fig