# Asymmetric

Regular arithmetic is two-way

$3^x$ is easily reversible. If I told you $3^x=81$, you could solve this algebraically using $log_{3}(81)$. You could even guess $3^5$ which would give $243$, meaning you would then know to guess a smaller exponent, leading you to the correct answer.

mod arithmetic is an example of one-way function. For example $3^x mod(7)=1$ is not trivial to solve. In this case, you might try $3^5 mod(7)$ but that equals $5$. You may think this means you should try a smaller exponent, but that would lead you in the wrong direction. The actual answer is $3^6 mod(7)=1$. As you can imagine, for large numbers, this problem becomes drastically more difficult. For example, I can very quickly calculate $2^{143} mod(2167)=1306$, but it would take you much longer to determine the exponent given $2^x mod(2167)=1306$.

Unlike symmetric encryption, which uses the same key and function for encryption and decryption, an asymmetric encryption function is one-way. Knowing the encryption function is not enough to perform decryption. In fact, the whole purpose of asymmetric encryption was for everyone to know a users encryption function, thereby avoiding the problem of key sharing.

Alice Bob and Eve. Alice wants to send a personal message to Bob, which Eve is trying to read. 

Alice can send a locked message to Bob. Bob can add his own lock and send the message back to Alice. Alice can remove her lock and send the message back to Bob. Bob can then remove his lock and read the message. In digital cryptography, this doesn't work because the order of operations of the encryption function is of great importance. Last in, first out.

Alice gives every post office a copy of her lock. Everyone can lock a message and send it to her. Only she has the key to unlock

Diffie-Hellman pionered this idea.

RSA then published the first paper with a mathematical impl. of the idea.

It turns out that Ellis actually had this idea several years earlier, but was bound to secrecy by GCHQ. Ellis drew inspiration from a different idea whereby the receiver artificially adds noise to a communications channel. To an outside listener, any information on the channel is obscured by the noise. But the receiver, who knows the profile of the noise is able to decode any transmitted signals. The parallel here is that the receiver plays a role in the encryption process, not just the decryption (as is the case with symmetric encryption).

For several years, GCHQ cryptographers struggled to come up with a mathematical implementation of the concept, but failed. Cocks, a graduate trained in number theory and recently hired at GCHQ, came up with the idea "in about 30 minutes" work.

Impl. of RSA was limited by the current technology. Only industry and government had access to the computational resources required for practical use-cases of RSA - it was not publicly accessible.

Zimmerman came up with pretty good privacy (PGP), which was symmetric encryption with RSA used to encrypt the key.