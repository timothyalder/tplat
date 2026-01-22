from pathlib import Path
from typing import List, Optional, Tuple, Dict


def compile_frequency_distribution(alphabet: List[str]) -> List[Tuple[str, float]]:
    docs = Path(__file__).parents[3].glob("**/*.md")
    text = ""
    for doc in docs:
        with open(doc, "r") as file:
            text += file.read()
    return frequency_distribution(m=text.upper(), alphabet=alphabet)


def frequency_distribution(m: str, alphabet: List[str]) -> List[Tuple[str, float]]:
    frequencies = [m.count(plaintext)/len(m) for plaintext in alphabet]
    return sorted(list(zip(alphabet, frequencies)), key=lambda x: x[1])
    

def frequency_analysis(c: str, alphabet: Optional[List[str]]=None, reference_distribution: Optional[List[Tuple[str, float]]]=None) -> Dict[str, str]:
    alphabet = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"] if alphabet is None else alphabet
    reference_distribution = compile_frequency_distribution(alphabet=alphabet) if reference_distribution is None else reference_distribution
    print(reference_distribution)
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
    # Correct: E, A
    # To swap: S -> H, O -> I
    substitution_mapping = swap_mapping(substitution_mapping=substitution_mapping, a="S", b="H")
    substitution_mapping = swap_mapping(substitution_mapping=substitution_mapping, a="O", b="I")
    m = "".join([substitution_mapping[ciphertext] for ciphertext in c.upper()])
    # print(m)
    # Correct: E, A, T, H, A, I
    # To swap: S -> U, P -> Y
    substitution_mapping = swap_mapping(substitution_mapping=substitution_mapping, a="S", b="U")
    substitution_mapping = swap_mapping(substitution_mapping=substitution_mapping, a="P", b="Y")
    m = "".join([substitution_mapping[ciphertext] for ciphertext in c.upper()])
    # print(m)
    # Mostly there
    # To swap: P -> B, N -> S
    substitution_mapping = swap_mapping(substitution_mapping=substitution_mapping, a="P", b="B")
    substitution_mapping = swap_mapping(substitution_mapping=substitution_mapping, a="N", b="S")
    substitution_mapping = swap_mapping(substitution_mapping=substitution_mapping, a="P", b="F")
    substitution_mapping = swap_mapping(substitution_mapping=substitution_mapping, a="M", b="D")
    substitution_mapping = swap_mapping(substitution_mapping=substitution_mapping, a="R", b="N")
    substitution_mapping = swap_mapping(substitution_mapping=substitution_mapping, a="R", b="M")
    substitution_mapping = swap_mapping(substitution_mapping=substitution_mapping, a="G", b="P")
    substitution_mapping = swap_mapping(substitution_mapping=substitution_mapping, a="R", b="C")
    m = "".join([substitution_mapping[ciphertext] for ciphertext in c.upper()])
    print(m)
    
    "C U D R Y H S O D B O D G R Z A F D N R F C R Q T EL C T H N V X S O H S G N N B Z N S R R Q H V R O O C L N T W H R E L H H P E L N G I O E W H R P O Q H R A F O Z S U G H R U H W N V T U H S B Q O S E E A M A Z L N O D B O D G R D W R D L G K Y Y R N Q R N O D N X H R U H A C S L V H D U L S T H N V X S G R M N Q Y C U O O O  E Z V H V V I A Y E A W I B Q S V Q C Y X D R W H R V P R H D B P E G H R N Q D G KEPRWPDTPKEE"