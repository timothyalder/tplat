import math
import random
from typing import List, Tuple

from sympy import isprime, mod_inverse

from cryptography.utils import vectorise


def iscoprime(a, b) -> bool:
    return math.gcd(a, b) == 1

def encrypt(m: str, p: int, q: int) -> Tuple[List[int], int]:
    random.seed(42)
    assert isprime(p) and isprime(q), "Error! Arguments p, and q must be prime numbers."
    
    # The encryption key is the pair of integers (e, n)
    n = p*q
    phi = (p-1)*(q-1) # Phi(n) is the length of the set of coprimes defined below 
    # coprimes = [x for x in range(n) if iscoprime(x, n)]
    # assert phi == len(coprimes), f"Error! Number phi {phi} != len(coprimes) {len(coprimes)}"
    while True:
        d = random.randrange(2, phi)
        if math.gcd(d, phi) == 1:
            break
    e = pow(base=d, exp=-1, mod=phi)
    
    c = [pow(m_int, e, n) for m_int in vectorise(m=m, n=n)]
    
    return c, d
    
def decrypt(c: List[int], p: int, q: int, d: int):
    assert isprime(p) and isprime(q), "Error! Arguments p, and q must be prime numbers."

    n = p*q
    m = [pow(base=c_int, exp=d, mod=n) for c_int in c]
    b = b"".join(
        block.to_bytes((block.bit_length() + 7) // 8, "big")
        for block in m
    )
    
    return b.decode("utf-8")

def bruteforce(c: List[int], d: int, max_prime: int=100):
    candidates = []
    num_candidates = 0
    primes = [p for p in range(2, max_prime) if isprime(p)]
    
    for i, p in enumerate(primes):
        for q in primes[i:]:
            phi = (p-1)*(q-1)
            # Check if d has an inverse mod phi(n) (i.e., is valid)
            if math.gcd(d, phi) != 1:
                continue
            try:
                e = mod_inverse(d, phi)
            except ValueError:
                continue
            num_candidates += 1
            try:
                plaintext = decrypt(c=c, p=p, q=q, d=d)
                candidates.append(plaintext)
            # Incorrect combos of p,q will mostly give invalid utf-8
            except UnicodeDecodeError:
                continue    
    return candidates, num_candidates


if __name__ == "__main__":
    m = "Hello World"
    p = 61
    q = 53
    print(f"Encryption message, '{m}' with prime numbers p={p} and q={q}")
    c, d = encrypt(m=m, p=p, q=q)
    print(f"Ciphertext: '{c}'")
    m = decrypt(c=c, p=p, q=q, d=d)
    print(f"Decrypted message: '{m}'")
    possible_m, _ = bruteforce(c=c, d=d)
    for m in possible_m:
        print(m)
        
    import matplotlib.pyplot as plt
    from pathlib import Path
    from tqdm import tqdm
    m = "Hi"
    primes = [p for p in range(17, 100) if isprime(p)]
    num_candidates = []
    ns = []
    
    for i, p in tqdm(enumerate(primes), desc="Generating plot", total=len(primes)):
        for q in primes[i:]:
            n = p*q
            ns.append(n)
            c, d = encrypt(m=m, p=p, q=q)
            num_candidates.append(bruteforce(c=c, d=d)[1])
    
    # Plot
    plt.figure(figsize=(10,6))
    plt.scatter(ns, num_candidates)
    plt.xlabel("RSA modulus n = p * q")
    plt.ylabel("Number of possible decryption candidates")
    plt.title("Number of possible RSA decryption candidates vs n (primes 2-100)")
    plt.grid(True)
    plt.savefig(Path(__file__).parent/"complexity.png")
