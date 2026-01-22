from pathlib import Path
from typing import List, Optional, Tuple, Dict


def typical_reference_distribution(alphabet: List[str]) -> List[Tuple[str, float]]:
    # https://pi.math.cornell.edu/~mec/2003-2004/cryptography/subs/frequencies.html
    reference_distribution = [
        ("E", 12.02),
        ("T", 9.10),
        ("A", 8.12),
        ("O", 7.68),
        ("I", 7.31),
        ("N", 6.95),
        ("S", 6.28),
        ("R", 6.02),
        ("H", 5.92),
        ("D", 4.32),
        ("L", 3.98),
        ("U", 2.88),
        ("C", 2.71),
        ("M", 2.61),
        ("F", 2.30),
        ("Y", 2.11),
        ("W", 2.09),
        ("G", 2.03),
        ("P", 1.82),
        ("B", 1.49),
        ("V", 1.11),
        ("K", 0.69),
        ("X", 0.17),
        ("Q", 0.11),
        ("J", 0.10),
        ("Z", 0.07),
    ]
    reference_alphabet, _ = zip(*reference_distribution) 
    if any(plaintext not in reference_alphabet for plaintext in alphabet):
        raise ValueError("Error! Alphabet not supported by this reference distribution")
    return [(plaintext, frequency) for plaintext, frequency in reference_distribution if plaintext in alphabet]



def compile_reference_distribution(alphabet: List[str]) -> List[Tuple[str, float]]:
    docs = Path(__file__).parents[3].glob("**/*.md")
    text = ""
    for doc in docs:
        with open(doc, "r") as file:
            text += file.read()
    return frequency_distribution(m=text.upper(), alphabet=alphabet)


def frequency_distribution(m: str, alphabet: List[str]) -> List[Tuple[str, float]]:
    frequencies = [m.count(plaintext)/len(m) for plaintext in alphabet]
    return sorted(list(zip(alphabet, frequencies)), key=lambda x: x[1], reverse=True)
    

def frequency_analysis(c: str, alphabet: Optional[List[str]]=None, reference_distribution: Optional[List[Tuple[str, float]]]=None) -> Dict[str, str]:
    alphabet = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"] if alphabet is None else alphabet
    # reference_distribution = compile_reference_distribution(alphabet=alphabet) if reference_distribution is None else reference_distribution
    reference_distribution = typical_reference_distribution(alphabet=alphabet)
    ciphertext_distribution = frequency_distribution(m=c.upper(), alphabet=alphabet)
    referencetext_ordered, _ = map(list, zip(*reference_distribution))
    ciphertext_ordered, _ = map(list, zip(*ciphertext_distribution))
    substitution_mapping = {ciphertext: plaintext for ciphertext, plaintext in zip(ciphertext_ordered, referencetext_ordered)}
    return substitution_mapping


def swap_mapping(substitution_mapping: Dict[str, str], a: str, b: str) -> Dict[str, str]:
    swapped_substitution_mapping = {value: key for key, value in substitution_mapping.items()}
    a_key = swapped_substitution_mapping[a] 
    b_key = swapped_substitution_mapping[b]
    swapped_substitution_mapping[a] = b_key
    swapped_substitution_mapping[b] = a_key
    return {value: key for key, value in swapped_substitution_mapping.items()}
    
    
if __name__ == "__main__":
    c = "EVA KRC BEOA TRNZEVA CPR BWTFCOWV OB DK VW UREVB BW AOLLOGFTC EB KWF UONPC DR TRA CW OUENOVR LZWU CPR LOZBC PEBCK OVBXRGCOWV WL CPR GPEZEGCRZB CPRBR GPEZEGCRZB EB EVK WVR UONPC ZREAOTK NFRBB LWZU E GOXPRZ CPEC OB CW BEK CPRK GWVHRK E UREVOVN DFC CPRV LZWU IPEC OB SVWIV WL SOAA O GWFTA VWC BFXXWBR POU GEXEDTR WL GWVBCZFGCOVN EVK WL CPR UWZR EDBCZFBR GZKXCWNZEXPB O UEAR FX UK UOVA EC WVGR CPEC CPOB IEB WL E BOUXTR BXRGORB BFGP PWIRHRZ EB IWFTA EXXREZ CW CPR GZFAR OVCRTTRGC WL CPR BEOTWZ EDBWTFCRTK OVBWTFDTR IOCPWFC CPR SRK LZWU CPR NWTA DFN DK RANEZ ETTEV XWR"
    substitution_mapping = frequency_analysis(c=c)
    substitution_mapping[" "] = " "
    m = "".join([substitution_mapping[ciphertext] for ciphertext in c.upper()])
    print(m)
    # At this point, we can start to recognise some fragments of words which inform us of errors in our substitution mapping
    # It seems like the message is signed off "ECGAH ADDAR WOE" -> "EDGAR ALLAN POE"
    substitution_mapping = swap_mapping(substitution_mapping=substitution_mapping, a="C", b="D")
    substitution_mapping = swap_mapping(substitution_mapping=substitution_mapping, a="H", b="R")
    substitution_mapping = swap_mapping(substitution_mapping=substitution_mapping, a="R", b="N")
    substitution_mapping = swap_mapping(substitution_mapping=substitution_mapping, a="W", b="P")
    substitution_mapping = swap_mapping(substitution_mapping=substitution_mapping, a="N", b="R")
    substitution_mapping = swap_mapping(substitution_mapping=substitution_mapping, a="C", b="L")
    substitution_mapping = swap_mapping(substitution_mapping=substitution_mapping, a="H", b="N")
    m = "".join([substitution_mapping[ciphertext] for ciphertext in c.upper()])
    print(m)
    # We can now infer the remainder of the cipher
    substitution_mapping = swap_mapping(substitution_mapping=substitution_mapping, a="S", b="H")
    substitution_mapping = swap_mapping(substitution_mapping=substitution_mapping, a="B", b="W")
    substitution_mapping = swap_mapping(substitution_mapping=substitution_mapping, a="M", b="Y")
    substitution_mapping = swap_mapping(substitution_mapping=substitution_mapping, a="M", b="F")
    substitution_mapping = swap_mapping(substitution_mapping=substitution_mapping, a="V", b="K")
    substitution_mapping = swap_mapping(substitution_mapping=substitution_mapping, a="S", b="I")
    m = "".join([substitution_mapping[ciphertext] for ciphertext in c.upper()])
    print(m)
