# Polyalphabetic Substitution Cipher

## Vignere Cipher

Broken by polymath 

## Enigma Machine

Used by the Germans in World War One.

Consisted of a keyboard, a scrambler unit, and a lampboard.


Two copper discs with each letter written around circumference of disc's. One disc slightly smaller than other, positioned inside other. The relative offset between the two wheels defines a Caeser shift cipher. This is a mechanical implementation of a *monoalphabetical substitution cipher*. Next, assume that for each keystroke of the input message, the disc rotates, obtaining a polyalphabetical substitution cipher. However, every 26 presses the cipher alphabet repeats. Repetition is the enemy is cryptography. And we already know such ciphers can be broken. To increase complexity, add additional discs to the scrambler. Discs are connected in series, with one full rotation of the preceding disc triggering a one-character turn of the next disc. Now have polyalphabetical substitution cipher with $26^3=17576$ possible keys to try for each message. However, this can still conceivably be bruteforced in a day by a team of cryptanalysts. In addition, make the scramblers interchangable; there are $3!=6$ combinations of the scramblers, leading to $17576\times6=105456$ possible keys. Finally, added a 6-lead plugboard that can be used to swap a pair of letters. For example, a wire connected the *a* and *b* sockets would make it such that the electrical signal for *a* would follow the path through the scambler previously reserved for *b*, and vice versa. Each swap uses 2 letters, so 6 swaps is 12 letters. There are $\binom{26}{12}=9657700$ possible ways to choose 12 letters from 26. There are $\frac{12!}{2^6\times6!}=10395$. This gives $9657700\times10395=100391791500$ ways to pair those 12 letters into 6 unordered pairs.
When a keystroke is performed, an electrical impulse travels from the key through the scrambler unit and into the reflector. The reflector reflects this electrical impulse back through

The *key* is the initial settings of the machine

By wiring multiple of these **scramblers** in series, you obtain a polyalphabetical substiution cipher 