# RSA

## Overview

**RSA** is a public-key (asymmetric) cryptosystem based on the computational difficulty of integer factorisation. It was publicly introduced in 1977 by **Rivest, Shamir, and Adleman**, following earlier classified work at **GCHQ** by **James Ellis**, **Clifford Cocks**, and **Malcolm Williamson**.

RSA provides:

* **Confidentiality** via public-key encryption
* **Authentication and non-repudiation** via digital signatures

It is a canonical example of a **trapdoor one-way function** (see [Asymmetric Cryptography](../index.md)).

---

## Cryptographic Model

Let:

* $M$ be the set of all possible plaintext messages, with $m \in M$
* $K$ be the set of all keys, with $k \in K$

For each $k \in K$, there exist two efficiently computable functions:

* **Encryption:** $E_k : M \rightarrow M$
* **Decryption:** $D_k : M \rightarrow M$

A **public-key cryptosystem** satisfies the following properties:

1. **Correctness**
   For all $m \in M$ and $k \in K$:
   $$
   D_k(E_k(m)) = m
   $$

2. **Efficiency**
   Both $E_k(m)$ and $D_k(m)$ are computationally feasible to compute.

3. **One-wayness**
   Given only $E_k$, it is computationally infeasible to derive $D_k$.

4. **Key derivability**
   Given $k$, it is easy to compute both $E_k$ and $D_k$.

If these conditions are met, $E_k$ is called a **trapdoor one-way permutation**: easy to compute in one direction, but infeasible to invert without secret information (the *trapdoor*).

In RSA:

* The **encryption key** is made public.
* The **decryption key** is kept private by the recipient.

This asymmetry eliminates the key-sharing problem inherent to **symmetric cryptography** (see [Symmetric Encryption](../../../symmetric/docs/index.md)).

---

## Mathematical Foundation

RSA relies on the fact that:

* **Integer multiplication** is computationally easy
* **Integer factorisation** is computationally hard for sufficiently large numbers

### Primes

> **Prime number**
> An integer $p$ is *prime* if $p \neq \pm 1$ and its only divisors are $\pm 1$ and $\pm p$.
> Integers that are not prime are called *composite*.

---

## Key Generation

1. Choose two large distinct prime numbers $p$ and $q$
   (typically hundreds or thousands of bits each)

> **Note:**
>
> In 1977, Martin Gardner published a column in Scientific America with a message encrypted using RSA-129 (129 indicating 129-bits). The purpose of the message was to highlight the security of the RSA encryption method. 17 years later, the message was finally decoded. The factorisation was performed over 6 months by a team of 600 volunteer researchers using approximately 1600 computers.
>
> ```RSA-129 = 114381625757888867669235779976146612010218296721242362562561842935706935245733897830597123563958705058989075147599290026879543541
> RSA-129 = 3490529510847650949147849619903898133417764638493387843990820577 * 32769132993266709549961988190834461413177642967992942539798288533
> ```
>
> When decrypted using the factorization the message was revealed to be *"The Magic Words are Squeamish Ossifrage"*.
>
> In 2015, RSA-129 was factored in about one day, with the CADO-NFS open source implementation of number field sieve, using a commercial cloud computing service for about $30.[12]
>
> Present implementations of RSA use 1024-2048 bits. This would take millions of years to break (many orders of magnitude longer than the age of the universe). [This 3Blue1Brown video](https://www.youtube.com/watch?v=S9JGmA5_unY) gives a helpful intuitive explanation of just how large this is.

2. Compute:
   $$
   n = pq
   $$

3. Compute Euler’s totient:
   $$
   \varphi(n) = (p-1)(q-1)
   $$

4. Choose an integer $e$ such that:
   $$
   1 < e < \varphi(n), \quad \gcd(e, \varphi(n)) = 1
   $$

5. Compute $d$ such that:
   $$
   ed \equiv 1 \pmod{\varphi(n)}
   $$

---

## Encryption and Decryption

* **Public key:** $(e, n)$
* **Private key:** $(d, n)$

### Encryption

To encrypt a message $m$:

1. Encode $m$ as an integer such that $0 \le m < n$
2. Compute the ciphertext:
   $$
   c \equiv m^e \pmod{n}
   $$

### Decryption

To decrypt a ciphertext $c$:

$$
m \equiv c^d \pmod{n}
$$

Correctness follows from Euler’s theorem and the construction of $e$ and $d$.

---

## Security Properties

* RSA security depends on the difficulty of factoring $n$ into $p$ and $q$
* Knowledge of $\varphi(n)$ allows recovery of $d$
* Factoring $n$ efficiently breaks RSA

> **Important:**
> RSA is deterministic and insecure without padding. Practical implementations use schemes such as **OAEP** for encryption and **PSS** for signatures.

---

## Historical Context

* Conceptual foundations developed at **GCHQ** in the early 1970s
* First public description by **Rivest, Shamir, and Adleman** (1977)
* Early deployment limited to governments and large institutions
* Popularised via **PGP**, which uses RSA to encrypt symmetric session keys
