from cryptography.symmetric.enigma.enigma import Enigma


def bruteforce(m: str):
    alphabet = ["A", "B", "C", "D", "E", "F", "G", "H", "I"]
    identity_substitution_mapping = {k: v for k, v in zip(alphabet, alphabet)}
    e = Enigma(alphabet=alphabet)

    # Create a reference for all possible initial settings
    chains = {}
    for s1_i in range(len(alphabet)):
        e.s1.substitution_mapping = identity_substitution_mapping
        e.s1.shift(s1_i)
        chains[s1_i] = {}
        for s2_i in range(len(alphabet)):
            e.s2.substitution_mapping = identity_substitution_mapping
            e.s2.shift(s2_i)
            chains[s1_i][s2_i] = {}
            for s3_i in range(len(alphabet)):
                chains[s1_i][s2_i][s3_i] = {}
                table = {}
                for plaintext in alphabet:
                    e.s3.substitution_mapping = identity_substitution_mapping
                    e.s3.shift(s3_i)
                    c = e(plaintext * 4)
                    table[c[0]] = c[
                        -1
                    ]  # Rejewski's solution hinged on the fact he knew the first and fourth letter of each message was the same
                print(f"{table=}")
                chain = []
                for start_chain in table.keys():
                    plaintext = start_chain
                    chain.append(plaintext)
                    while table[plaintext] != start_chain:
                        plaintext = table[plaintext]
                        chain.append(plaintext)
                chains[s1_i][s2_i][s3_i][plaintext] = chain
                print(f"{chain=}")
    print(f"{chains=}")

    # message_keys = ["".join(random.sample(alphabet, k=3)) for _ in range(100)]
    # m = [f"{message_key*2} {'abba ' * 10}" for message_key in message_keys]


if __name__ == "__main__":
    m = "abba"
    bruteforce(m=m)
