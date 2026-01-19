# RSA

## Background

Created by

## Context

Let $M$ be the set of all possible messages and K be the set of all "keys." For each $k\element K$, there exists both a decryption function $D_k M -> M$ and an ecryption function $E_k: M -> M$. 

* $M$: the set of all possible messages. It is the set of individual messages, $m$ — i.e., $m \element M$
* $K$: The set of all keys — i.e., $k \element K$
* $D_k$: For each $k \element K$, there exists a decryption function mapping $D_k: M -> M$
* $E_k: M -> M$: For the same $k$, there exists an ecryption function $E_k: M -> M$.

A public key cryptosystem obeys the following conditions:
1. For every $m \element M$ and every $k \element K$, $E_k(D_k(m)) = m$ and $D_k(E_k(m)) = m$.
2. For every $m \element M$ and every $k \element K$, the values of $E_k(m)$ and $D_k(m)$ are not difficult to compute.
3. For almost every $k \element K$, if somebody knows only the function $E_k$, it is computationally infeasible to compute $D_k$.
4. Given $k \element K$, it is easy to find the functions $E_k$ and $D_k$.

If the above conditions are met, $E_k$ is a *trap-door one-way permutation*. The function is one way because 

The encryption function, $E_k$, is made publicly accessible; anyone can use the public key to send an encrypted message. But $D_k$ is kept private, with only the recipient being able to decrypt the encrypted message. 

## Theory

How is this accomplished? The core concept is that although multiplying two numbers is trivial, factoring the product back into the original two numbers is much more difficult to do computationally (for large numbers).

Consider two **large** prime numbers $p$ and $q$ (usually ~50 digits each).

> **Prime:**
>
> An integer $p$ is $prime$ if $p!=\pm 1$ and it's only divisors are $\pm 1$ and $\pm p$. An integer that does not satify this property is called $composite$.

First, define $n = p * q$. 

The encryption is the pair of integers $(e, n)$ 

The decryption key is the pair $(d, n)$. 

Given a message $m$, in order to encrypt it we would:
1. Represent it as an integer between $0$ and $n-1$.
2. $E(m) \equivalent m^e \equivalent c (mod n)$ — i.e., the encrypted message is $m$ raised to the $e^{th}$ power modulo $n$ resulting in the ciphertext $c$
3. $D(c) \equivalent c^d \equivalent m (mod n)$ — i.e., the decrypted message is $c$ raised to the to the $d^{th}$ power modulo $n$.

The integers $e$ and $d$ are closely related to $p$ and $q$:

$d=(p-1)(q-1)$
$e=1/d modulo (d)$

The encryption key, $(e,n)$ is publicly accessible, but the decryption key $(d,n)$ is private.