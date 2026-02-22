# Asymmetric Cryptography

Asymmetric cryptography relies on **one-way mathematical functions**.

---

## One-Way Functions

Regular arithmetic is reversible:
* If $3^x=81$, then $x=log_{3}(81)$.

Modular arithmetic is not:
* Solving $3^x \mod{7} = 1$ is non-trivial
* The discrete logarithm problem is hard

---

## Core Idea

* Encryption and decryption use different keys
* Encryption key is public
* Decryption key is private
* Eliminates the key distribution problem

---

## Public-Key Concept

Anyone can encrypt a message using the public key.  
Only the private key holder can decrypt it.

---

## Historical Development

* **Diffie–Hellman** introduced key exchange
* **Ellis** conceptualized public-key cryptography (classified)
* **Cocks** derived RSA internally at GCHQ
* **RSA** publicly introduced the first practical system

---

## RSA

* Based on integer factorization
* Security relies on computational hardness
* Initially limited to governments and industry

---

## Hybrid Cryptography

* RSA encrypts symmetric keys
* Symmetric cipher encrypts message
* Used in systems like **PGP**

---

### Summary

Asymmetric cryptography enables secure communication over open channels by exploiting mathematical asymmetry rather than secrecy.
