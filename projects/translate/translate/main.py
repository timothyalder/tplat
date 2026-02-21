import sys
from pathlib import Path
from typing import Optional, List
from tqdm import tqdm
from deep_translator import GoogleTranslator


def translate_srt(input_path: str, output_path: Optional[str] = None) -> List[str]:
    # Validate inputs
    assert Path(input_path).suffix==".srt"
    if output_path is None:
        output_path = input_path.replace(".srt", "-english.srt")
        
    # Read in data
    with open(input_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Translate
    translated_lines = []
    for line in tqdm(lines, desc=f"Translating {Path(input_path).name}"):
        if line.strip() and not line.strip().isdigit() and '-->' not in line:
            translated = GoogleTranslator(source='de', target='en').translate(line)
            translated_lines.append(translated + '\n')
        else:
            translated_lines.append(line)

    # Write out
    with open(output_path, 'w', encoding='utf-8') as f:
        f.writelines(translated_lines)
        
    return translated_lines


if __name__ == "__main__":    
    input_path = sys.argv[1] if len(sys.argv)>1 else "/Users/timothyalder/Downloads/Love Sucks/S1E03/Love_Sucks-Jäger_und_Gejagte-0776117932.srt"
    output_path = sys.argv[2] if len(sys.argv)>2 else None
    translate_srt(input_path=input_path, output_path=output_path)
