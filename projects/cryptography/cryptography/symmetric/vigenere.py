from typing import Optional, List
import math
from itertools import zip_longest

from cryptography.symmetric.caesar_shift import caesar_shift
from cryptography.symmetric.frequency_analysis import frequency_analysis


def find_repetitions(c: str, min_length: int=3, max_length: int=10):
    c = c.replace(" ", "")
    repetitions = {}
    for l in range(min_length, max_length):
        for i in range(len(c)-l):
            if c.count(c[i:i+l])>1 and c[i:i+l] not in repetitions.keys():
                repetitions[c[i:i+l]] = c.count(c[i:i+l])
    return repetitions


def find_distance_between_repititions(c: str, repitition: str) -> int:
    c = c.replace(" ", "")
    idxs = []
    for idx, _ in enumerate(c):
        if c[idx:idx+len(repitition)] == repitition:
            idxs.append(idx)
    distances = [idxs[i+1] - idxs[i] for i in range(len(idxs)-1)]
    return min(distances)
    
        
def common_factors(x, y):
    common_divisor = math.gcd(x, y)
    common_factors = []
    for i in range(1, common_divisor + 1):
        if common_divisor % i == 0:
            common_factors.append(i)
    return common_factors


def vigenere(m: str, key: str, alphabet: Optional[List[str]]=None) -> str:
    alphabet = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"] if alphabet is None else alphabet
    m = m.replace(" ", "").upper()
    key = key.replace(" ", "").upper()
    c = ""
    for idx, plaintext in enumerate(m):
        i = alphabet.index(key[idx%len(key)])
        c += caesar_shift(m=plaintext, i=i, alphabet=alphabet)
    return c


def kasiski(c: str, key_length: int):
    c = c.replace(" ", "").upper()
    plaintext_columns = []
    monoalphabetic_ciphertexts = [c[i::key_length] for i in range(key_length)]
    for monoalphabetic_ciphertext in monoalphabetic_ciphertexts:
        substitution_mapping = frequency_analysis(c=monoalphabetic_ciphertext)
        plaintext_columns.append([substitution_mapping[ciphertext] for ciphertext in monoalphabetic_ciphertext])
         
    m = "".join(
        ch
        for row in zip_longest(*plaintext_columns)
        for ch in row
        if ch is not None
    )
    
    return m
        

if __name__ == "__main__":
    c = "C U D R Y H S O D B O D G R Z A F D N R F C R Q T EL C T H N V X S O H S G N N B Z N S R R Q H V R O O C L N T W H R E L H H P E L N G I O E W H R P O Q H R A F O Z S U G H R U H W N V T U H S B Q O S E E A M A Z L N O D B O D G R D W R D L G K Y Y R N Q R N O D N X H R U H A C S L V H D U L S T H N V X S G R M N Q Y C U O O O  E Z V H V V I A Y E A W I B Q S V Q C Y X D R W H R V P R H D B P E G H R N Q D G KEPRWPDTPKEE"
    repetitions = find_repetitions(c=c, min_length=6)
    print(repetitions) # ODBODGR and THNVXS appear twice in the ciphertext
    distance = find_distance_between_repititions(c=c, repitition = "ODBODGR")
    print(distance) # ODBODGR appears 102 characters apart
    distance = find_distance_between_repititions(c=c, repitition = "THNVXS")
    print(distance) # THNVXS appears 120 characters apart
    # Common factors
    candidates = common_factors(102, 120)
    print(candidates) # The keyword is likely 1, 2, 3, or 6 characters long
    # 1, 2, and 3 are all suspiciously small. 6 seems like the most likely candidate
    # Let's now try and apply frequency analysis assuming a key length of 6
    m = kasiski(c=c, key_length=6)
    print(m)
    # Let's test some 6-letter keys: "cipher"
    # m = vigenere(m=c, key="cipher")
    # print(m)
