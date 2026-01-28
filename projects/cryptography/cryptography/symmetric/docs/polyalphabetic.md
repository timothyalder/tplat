# Polyalphabetic Substitution Cipher

A **polyalphabetic substitution cipher** uses multiple substitution alphabets during encryption.

* Letter mappings change throughout the message
* Reduces the effectiveness of frequency analysis
* Introduces periodic structure

---

## Vigenère Cipher

The **Vigenère cipher** was once called *le chiffre indéchiffrable* (“the indecipherable cipher”).

* Invented in 1467
* Popularized centuries later
* Uses a repeating keyword

---

### Encryption Process

1. Choose a keyword
2. Align keyword with plaintext
3. Apply Caesar shift per letter
4. Repeat keyword cyclically

---

### Cryptanalysis

* Claimed unbreakable for centuries
* Broken by **Charles Babbage** (unpublished)
* Publicly broken by **Friedrich Kasiski**

---

### Kasiski Examination

1. Identify repeated ciphertext sequences
2. Measure distances between repetitions
3. Compute common factors
4. Estimate keyword length
5. Split ciphertext by period
6. Apply frequency analysis to each slice
7. Reconstruct plaintext

---

### Notes

* Breaks polyalphabetic cipher into multiple monoalphabetic ones
* Periodicity is the core weakness
