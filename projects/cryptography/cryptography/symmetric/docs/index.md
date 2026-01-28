# Symmetric Cryptography

**Symmetric cryptography** is called “symmetric” because the same secret key is used for both encryption and decryption. Anyone who possesses the key can both encrypt and decrypt messages.

This category includes nearly all classical ciphers and many modern block and stream ciphers.

---

## Frequency Analysis

**Frequency analysis** exploits the statistical structure of natural language.

* Certain letters occur more frequently (e.g., E, T, A in English).
* In monoalphabetic substitution ciphers, these frequencies are preserved.
* Digraphs and trigraphs (e.g., TH, HE, ING) provide additional structure.

---

### Historical Origin

* Developed by **Al-Kindi** in the 9th century.
* First known systematic cryptanalytic technique.
* Documented in *A Manuscript on Deciphering Cryptographic Messages*.

---

### Method

1. Count letter frequencies in the ciphertext
2. Compare against known language distributions
3. Propose substitutions
4. Refine guesses using word patterns and context

---

### Effectiveness

* Extremely effective against monoalphabetic substitution
* Weak against polyalphabetic ciphers
* Ineffective against modern cryptographic systems

---
