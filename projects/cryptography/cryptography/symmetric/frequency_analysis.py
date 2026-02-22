from pathlib import Path
from typing import List, Tuple, Dict, Union

from cryptography.core.alphabet import Alphabet


def compile_reference_distribution(
    alphabet: Union[List[str], List[Tuple[str, float]], Alphabet, None] = None,
) -> Alphabet:
    docs = Path(__file__).parents[3].glob("**/*.md")
    text = ""
    for doc in docs:
        with open(doc, "r") as file:
            text += file.read()
    alphabet = Alphabet(alphabet=alphabet)
    alphabet.calculate_distribution(m=text)
    return alphabet


def swap_mapping(
    substitution_mapping: Dict[str, str], a: str, b: str
) -> Dict[str, str]:
    swapped_substitution_mapping = {
        value: key for key, value in substitution_mapping.items()
    }
    a_key = swapped_substitution_mapping[a]
    b_key = swapped_substitution_mapping[b]
    swapped_substitution_mapping[a] = b_key
    swapped_substitution_mapping[b] = a_key
    return {value: key for key, value in swapped_substitution_mapping.items()}
