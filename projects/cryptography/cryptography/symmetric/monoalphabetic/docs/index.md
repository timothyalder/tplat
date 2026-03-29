# Monoalphabetic Substitution Cipher

A **monoalphabetic substitution cipher** replaces each plaintext character with exactly one ciphertext character.

* The mapping remains fixed for the entire message.
* The cipher alphabet is a permutation of the plaintext alphabet.
* The Caesar cipher is a special case.

**Example mapping:**
A → Q, B → M, C → L, ...

---

## Properties

* Preserves letter frequency distributions
* Vulnerable to frequency analysis
* Can be marginally strengthened using nulls or homophones

---

## Caesar Cipher

The **Caesar cipher** is the simplest substitution cipher.

* Each letter is shifted by a fixed offset.
* Traditionally uses a shift of 3.

**Example (shift = 3):**

```
PLAINTEXT: ATTACK
CIPHERTEXT: DWWDFN
```

---

### Properties

* Monoalphabetic substitution
* Key space of size 25
* Trivially broken by brute force or frequency analysis

---

## Keyword Cipher

A **keyword cipher** constructs the substitution alphabet using a keyword.

**Construction:**

1. Choose a keyword
2. Remove repeated letters
3. Append remaining alphabet characters

**Example:**

```
Keyword: CIPHER
Substitution alphabet: C I P H E R A B D F G ...
```

---

### Notes

* Stronger than Caesar
* Still preserves frequency
* Vulnerable to frequency analysis

---

## Nulls

**Nulls** are meaningless characters inserted into the ciphertext.

* Known to the intended recipient
* Obscure patterns and frequencies
* Historically common in hand ciphers

**Example:**

```
CIPHERTEXT: XQDAZWWXDFNQZ
(remove X, Z, Q → DWWDFN)
```

> **Note:**
>
> Nulls increase confusion but do not provide cryptographic security.
