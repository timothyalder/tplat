from typing import Union, List, Tuple
import math
from itertools import zip_longest

from cryptography.core.alphabet import Alphabet
from cryptography.symmetric.caesar_shift import caesar_shift, determine_i, estimate_i_from_pdf
from cryptography.symmetric.frequency_analysis import frequency_distribution


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


def vigenere(m: str, key: str, alphabet: Union[List[str], List[Tuple[str,float]], Alphabet, None]=None) -> str:
    alphabet = Alphabet(alphabet=alphabet)
    m = m.replace(" ", "").upper()
    key = key.replace(" ", "").upper()
    c = ""
    for idx, plaintext in enumerate(m):
        i = alphabet.index(key[idx%len(key)])
        c += caesar_shift(m=plaintext, i=i, alphabet=alphabet)
    return c


def kasiski(c: str, key_length: int, alphabet: Union[List[str], List[Tuple[str,float]], Alphabet, None]=None):
    alphabet = Alphabet(alphabet=alphabet)
    reference_distribution = Alphabet()
    reference_distribution.canonical_sort()
    c = c.replace(" ", "").upper()
    plaintext_columns = []
    monoalphabetic_ciphertexts = [c[i::key_length] for i in range(key_length)]
    alphabets = []
    for idx, monoalphabetic_ciphertext in enumerate(monoalphabetic_ciphertexts):
        ciphertext_distribution = frequency_distribution(m=monoalphabetic_ciphertext, alphabet=alphabet.alphabet)
        # ciphertext_distribution.frequency_sort()
        # reference_distribution.frequency_sort()
        # naive_i = determine_i(m=ciphertext_distribution[0][0], c=reference_distribution[0][0])
        # reference_distribution.canonical_sort()
        ciphertext_distribution.canonical_sort()
        i = estimate_i_from_pdf(m=reference_distribution, c=ciphertext_distribution)
        print(i)
        if idx == 0:
            i = 1 # Not so confident - lots of X's
        if idx == 1:
            i = -13 # Pretty confident
        if idx == 2:
            i = -3 # Pretty confident
        if idx == 3:
            i = -10 # -9, -10, -11 # Not very confident
        if idx == 4:
            i = -10 # Not so confident - lots of K; Q looks good though
        if idx == 5:
            i = -3 # Very confident
        ciphertext_distribution.rotate(i)
        
        alphabets += [ciphertext_distribution]
        # print(f"i from pdf: {i}, i from max freq {naive_i}")
        
        plaintext = caesar_shift(m=monoalphabetic_ciphertext, i=i, alphabet=alphabet)
        plaintext_columns.append(plaintext)
    distributions_fig = reference_distribution.plot_distributions(alphabets=alphabets[4:5])
    distributions_fig.savefig("distributions.png")
         
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
    distance = find_distance_between_repititions(c=c, repitition = "ODBODGR") # ODBODGR appears 102 characters apart
    distance = find_distance_between_repititions(c=c, repitition = "THNVXS") # THNVXS appears 120 characters apart
    candidates = common_factors(102, 120)
    print(candidates) # The keyword is likely 1, 2, 3, or 6 characters long
    # 1, 2, and 3 are all suspiciously small. 6 seems like the most likely candidate
    # Let's now try and apply frequency analysis assuming a key length of 6
    m = kasiski(c=c, key_length=6)
    print(m)
