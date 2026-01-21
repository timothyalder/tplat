# Monoalphabetic Substitution Cipher

A **monoalphabetic substitution cipher** replaces each plaintext letter with exactly one ciphertext letter.

* The mapping is fixed for the entire message.
* Caesar cipher is a special case.
* Example: A->Q, B->M, C->L, etc.

**Properties:**

* Preserves letter frequency distributions.
* Vulnerable to frequency analysis.
* Can be strengthened slightly with nulls or homophones.


## Caesar Cipher

The **Caesar cipher** is a simple substitution cipher.

* Each letter is shifted by a fixed number in the alphabet.
* Traditionally uses a shift of 3.

**Example (shift = 3):**

```
PLAINTEXT:  ATTACK
CIPHERTEXT: DWWDFN
```

**Properties:**

* Monoalphabetic substitution
* Very small key space (25 possible keys)
* Trivially broken with brute force or frequency analysis

---

## Keyword Cipher

A **keyword substitution cipher** is a type of monoalphabetic substitution cipher in which the substitution alphabet is constructed using a chosen keyword. Repeated letters in the keyword are removed, and the remaining letters of the alphabet are appended in order to form a keyed alphabet. Each plaintext letter is then replaced by the corresponding letter in this substitution alphabet. While stronger than a simple Caesar cipher, keyword substitution ciphers preserve letter frequency and are therefore vulnerable to frequency analysis.

---

## Nulls

**Nulls** are meaningless characters added to ciphertext to obscure patterns.

* Decryptor knows which characters to ignore.
* Used to defeat simple frequency or pattern matching.
* Common in classical hand ciphers.

**Example:**

```
CIPHERTEXT: XQDAZWWXDFNQZ
(remove X, Z, Q → DWWDFN)
```

**Note:** Nulls add confusion but *do not provide cryptographic security*.

---
