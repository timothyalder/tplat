from typing import Union, List, Tuple
from itertools import zip_longest

from cryptography.core.alphabet import Alphabet
from cryptography.symmetric.monoalphabetic.caesar_shift import caesar_shift


def find_repetitions(c: str, min_length: int = 3, max_length: int = 10):
    c = c.replace(" ", "")
    repetitions = {}
    for l in range(min_length, max_length):
        for i in range(len(c) - l):
            if c.count(c[i : i + l]) > 1 and c[i : i + l] not in repetitions.keys():
                repetitions[c[i : i + l]] = c.count(c[i : i + l])
    return repetitions


def find_distance_between_repititions(c: str, repitition: str) -> int:
    c = c.replace(" ", "")
    idxs = []
    for idx, _ in enumerate(c):
        if c[idx : idx + len(repitition)] == repitition:
            idxs.append(idx)
    distances = [idxs[i + 1] - idxs[i] for i in range(len(idxs) - 1)]
    return min(distances)


def vigenere(
    m: str,
    key: str,
    alphabet: Union[List[str], List[Tuple[str, float]], Alphabet, None] = None,
) -> str:
    alphabet = Alphabet(alphabet=alphabet)
    m = m.replace(" ", "").upper()
    key = key.replace(" ", "").upper()
    c = ""
    for idx, plaintext in enumerate(m):
        i = alphabet.index(key[idx % len(key)])
        c += caesar_shift(m=plaintext, i=i, alphabet=alphabet)
    return c


def kasiski(
    c: str,
    key_length: int,
    alphabet: Union[List[str], List[Tuple[str, float]], Alphabet, None] = None,
) -> Tuple[str, str]:
    reference_distribution = Alphabet(alphabet=alphabet)
    reference_distribution.canonical_sort()
    c = c.replace(" ", "").upper()
    plaintext_columns = []
    monoalphabetic_ciphertexts = [c[i::key_length] for i in range(key_length)]
    alphabets = []
    predicted_key = ""
    for monoalphabetic_ciphertext in monoalphabetic_ciphertexts:
        ciphertext_distribution = Alphabet(alphabet=reference_distribution.alphabet)
        ciphertext_distribution.calculate_distribution(m=monoalphabetic_ciphertext)
        ciphertext_distribution.canonical_sort()
        i = ciphertext_distribution.estimate_i_from_pdf(c=reference_distribution)
        ciphertext_distribution.rotate(i)
        predicted_key += reference_distribution[i - 1][0]
        alphabets += [ciphertext_distribution]

        plaintext = caesar_shift(
            m=monoalphabetic_ciphertext, i=i, alphabet=ciphertext_distribution
        )
        plaintext_columns.append(plaintext)

    m = "".join(
        ch for row in zip_longest(*plaintext_columns) for ch in row if ch is not None
    )

    return m, predicted_key
