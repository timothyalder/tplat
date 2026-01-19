# Cryptography

**Cryptography** is the practice and study of techniques for securing communication in the presence of adversaries. The primary goal is to **conceal a message** so that only intended recipients can understand it.

## On Security

---

The **principles of information security** provide a framework for protecting data. **Confidentiality** ensures that information is only accessible to authorized users, for example, encrypting emails so only the intended recipient can read them. **Integrity** guarantees that data is accurate and unaltered, such as using a checksum to verify a downloaded file has not been tampered with. **Availability** ensures that information and systems are accessible when needed, like maintaining redundant servers so a website remains online during outages. **Authentication** confirms the identity of users or systems, for instance, requiring a username and password before accessing an account. **Non-repudiation** prevents parties from denying their actions, such as using digital signatures to prove the sender authored a document.

---

## Concealing a Message

There are three historically distinct approaches:

1. **Hiding the existence of the message**
2. **Obscuring the structure of the message**
3. **Transforming the message into an unreadable form**

---

## Steganography

**Steganography** is the practice of hiding a message so that its *existence* is concealed.

* The message is hidden within another medium (text, image, object).
* If discovered, the message may be readable immediately.
* Security relies on secrecy of the method, not strong mathematics.

**Historical examples:**

* Writing a message on a person’s shaved scalp and allowing hair to regrow over it (Herodotus).
* Scraping wax off wooden tablets, writing the message underneath, then recoating with wax.
* Invisible inks, microdots, digital image steganography.

**Key idea:** *The attacker should not even suspect a message exists.*

---

Here’s an expanded **Transposition** section including the **scytale example**:

---

## Transposition

A **transposition** cipher rearranges the characters of a message according to a fixed system.

* The letters themselves are unchanged.
* Only their positions are permuted.
* Common types include columnar transposition and route ciphers.

**Example 1: Columnar Transposition**

```
PLAINTEXT:  ATTACKATDAWN
TRANSPOSED: TTAWACDATKAN
```

**Example 2: Scytale (Ancient Greek military)**

* A scytale is a cylinder around which a strip of parchment is wound.
* The message is written along the length of the cylinder.
* When unwound, the letters appear scrambled. Only a cylinder of the same diameter can read it correctly.

```
PLAINTEXT:  ATTACKATDAWN
SCYTALE STRIP (scrambled when flat):
A C A
T K T
T A D
A W N
```

* Reading column-wise along the cylinder reconstructs the original message.

**Properties:**

* Preserves letter frequency.
* Vulnerable to statistical analysis if used alone.
* Often combined with substitution for added security.

---

## Encryption

**Encryption** is the process of transforming plaintext into ciphertext using an algorithm and a key.

* Comes from the Greek *kryptós* (hidden or secret).
* Assumes the attacker knows the algorithm but not the key (Kerckhoffs’s Principle).
* Modern cryptography relies on computational hardness, not obscurity.

---

## Cipher

A **cipher** is a specific algorithm for performing encryption or decryption.

* Operates at the level of **letters, bits, or symbols**
* Uses a key to control the transformation

Ciphers can be classified as:

* **Substitution ciphers** (replace symbols)
* **Transposition ciphers** (reorder symbols)
* **Product ciphers** (combine both)

---

## Code

A **code** replaces entire words or phrases with symbols or numbers.

* Operates at the *semantic* level (words/phrases), not letters.
* Requires a **codebook**.
* Example: “Attack at dawn” → “4729”

**Differences from ciphers:**

* Codes are language-dependent.
* Codebooks are bulky and hard to distribute securely.
* Historically used in diplomacy and military communication.

---

# Cryptanalysis

**Cryptanalysis** is the study of methods for breaking cryptographic systems—recovering the plaintext or key without authorization.

---

## Determining the Secret Key

The primary goal of cryptanalysis is to determine the **secret key** or otherwise recover plaintext.

Attack models include:

* Ciphertext-only attack
* Known-plaintext attack
* Chosen-plaintext attack
* Brute-force attack

---

## Decryption

**Decryption** is the process of converting ciphertext back into plaintext.

* From the Greek *kryptós* (hidden) + *lýein* (to loosen or release).
* Normally requires the secret key.
* Cryptanalysis seeks to decrypt *without* the key.

---

## Frequency Analysis

**Frequency analysis** exploits the statistical properties of language.

* Certain letters appear more often (e.g., E, T, A in English).
* In monoalphabetic ciphers, frequencies are preserved.

**Historical origin:**

* Developed by **Al-Kindi** in the 9th century.
* First systematic cryptanalytic technique.

**Process:**

1. Count letter frequencies in ciphertext
2. Compare with known language statistics
3. Guess substitutions and refine using patterns

**Effectiveness:**

* Extremely effective against monoalphabetic substitution
* Ineffective against strong modern ciphers

---

## References

Singh, S. (1999). *The Code Book: The Science of Secrecy from Ancient Egypt to Quantum Cryptography*. Doubleday.