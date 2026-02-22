import pytest
from cryptography.symmetric.polyalphabetic.vigenere import (
    vigenere,
    kasiski,
    find_distance_between_repititions,
    find_repetitions,
)


def test_cryptogram_three():
    from cryptography.core.alphabet import Alphabet
    from cryptography.symmetric.frequency_analysis import swap_mapping

    c = (
        "EVA KRC BEOA TRNZEVA CPR BWTFCOWV OB DK VW UREVB BW AOLLOGFTC EB "
        "KWF UONPC DR TRA CW OUENOVR LZWU CPR LOZBC PEBCK OVBXRGCOWV WL CPR "
        "GPEZEGCRZB CPRBR GPEZEGCRZB EB EVK WVR UONPC ZREAOTK NFRBB LWZU E GOXPRZ "
        "CPEC OB CW BEK CPRK GWVHRK E UREVOVN DFC CPRV LZWU IPEC OB SVWIV WL SOAA O "
        "GWFTA VWC BFXXWBR POU GEXEDTR WL GWVBCZFGCOVN EVK WL CPR UWZR EDBCZFBR "
        "GZKXCWNZEXPB O UEAR FX UK UOVA EC WVGR CPEC CPOB IEB WL E BOUXTR BXRGORB "
        "BFGP PWIRHRZ EB IWFTA EXXREZ CW CPR GZFAR OVCRTTRGC WL CPR BEOTWZ EDBWTFCRTK "
        "OVBWTFDTR IOCPWFC CPR SRK LZWU CPR NWTA DFN DK RANEZ ETTEV XWR"
    )
    ciphertext_distribution = Alphabet()
    plaintext_distribution = Alphabet()
    ciphertext_distribution.calculate_distribution(m=c)
    plaintext_distribution.frequency_sort()
    substitution_mapping = {
        ciphertext: referencetext
        for ciphertext, referencetext in zip(
            ciphertext_distribution.alphabet, plaintext_distribution.alphabet
        )
    }
    substitution_mapping[" "] = " "
    m = "".join([substitution_mapping[ciphertext] for ciphertext in c.upper()])
    # print(m)
    # At this point, we can start to recognise some fragments of words which inform us of errors in our substitution mapping
    # It seems like the message is signed off "ECGAH ADDAR WOE" -> "EDGAR ALLAN POE"
    substitution_mapping = swap_mapping(
        substitution_mapping=substitution_mapping, a="C", b="D"
    )
    substitution_mapping = swap_mapping(
        substitution_mapping=substitution_mapping, a="H", b="R"
    )
    substitution_mapping = swap_mapping(
        substitution_mapping=substitution_mapping, a="R", b="N"
    )
    substitution_mapping = swap_mapping(
        substitution_mapping=substitution_mapping, a="W", b="P"
    )
    substitution_mapping = swap_mapping(
        substitution_mapping=substitution_mapping, a="N", b="R"
    )
    substitution_mapping = swap_mapping(
        substitution_mapping=substitution_mapping, a="C", b="L"
    )
    substitution_mapping = swap_mapping(
        substitution_mapping=substitution_mapping, a="H", b="N"
    )
    m = "".join([substitution_mapping[ciphertext] for ciphertext in c.upper()])
    assert m == (
        "AND MET IAHD LEGRAND TSE IOLUTHON HI WM NO FEANI IO DHYYHCULT AI "
        "MOU FHGST WE LED TO HFAGHNE YROF TSE YHRIT SAITM HNIPECTHON OY TSE "
        "CSARACTERI TSEIE CSARACTERI AI ANM ONE FHGST READHLM GUEII YORF A CHPSER "
        "TSAT HI TO IAM TSEM CONKEM A FEANHNG WUT TSEN YROF BSAT HI VNOBN OY VHDD H "
        "COULD NOT IUPPOIE SHF CAPAWLE OY CONITRUCTHNG ANM OY TSE FORE AWITRUIE "
        "CRMPTOGRAPSI H FADE UP FM FHND AT ONCE TSAT TSHI BAI OY A IHFPLE IPECHEI "
        "IUCS SOBEKER AI BOULD APPEAR TO TSE CRUDE HNTELLECT OY TSE IAHLOR AWIOLUTELM "
        "HNIOLUWLE BHTSOUT TSE VEM YROF TSE GOLD WUG WM EDGAR ALLAN POE"
    )
    # We can now infer the remainder of the cipher
    substitution_mapping = swap_mapping(
        substitution_mapping=substitution_mapping, a="S", b="H"
    )
    substitution_mapping = swap_mapping(
        substitution_mapping=substitution_mapping, a="B", b="W"
    )
    substitution_mapping = swap_mapping(
        substitution_mapping=substitution_mapping, a="M", b="Y"
    )
    substitution_mapping = swap_mapping(
        substitution_mapping=substitution_mapping, a="M", b="F"
    )
    substitution_mapping = swap_mapping(
        substitution_mapping=substitution_mapping, a="V", b="K"
    )
    substitution_mapping = swap_mapping(
        substitution_mapping=substitution_mapping, a="S", b="I"
    )
    m = "".join([substitution_mapping[ciphertext] for ciphertext in c.upper()])
    assert m == (
        "AND YET SAID LEGRAND THE SOLUTION IS BY NO MEANS SO DIFFICULT AS "
        "YOU MIGHT BE LED TO IMAGINE FROM THE FIRST HASTY INSPECTION OF THE "
        "CHARACTERS THESE CHARACTERS AS ANY ONE MIGHT READILY GUESS FORM A CIPHER "
        "THAT IS TO SAY THEY CONVEY A MEANING BUT THEN FROM WHAT IS KNOWN OF KIDD I "
        "COULD NOT SUPPOSE HIM CAPABLE OF CONSTRUCTING ANY OF THE MORE ABSTRUSE "
        "CRYPTOGRAPHS I MADE UP MY MIND AT ONCE THAT THIS WAS OF A SIMPLE SPECIES "
        "SUCH HOWEVER AS WOULD APPEAR TO THE CRUDE INTELLECT OF THE SAILOR ABSOLUTELY "
        "INSOLUBLE WITHOUT THE KEY FROM THE GOLD BUG BY EDGAR ALLAN POE"
    )


def test_cryptogram_four():
    from cryptography.core.math import common_factors

    c = (
        "C U D R Y H S O D B O D G R Z A F D N R F C R Q T E L "
        "C T H N V X S O H S G N N B Z N S R R Q H V R O O "
        "C L N T W H R E L H H P E L N G I O E W H R P O Q "
        "H R A F O Z S U G H R U H W N V T U H S B Q O S E E "
        "A M A Z L N O D B O D G R D W R D L G K Y Y R N "
        "Q R N O D N X H R U H A C S L V H D U L S T H N V "
        "X S G R M N Q Y C U O O O E Z V H V V I A Y E A W I B "
        "Q S V Q C Y X D R W H R V P R H D B P E G H R N Q D G "
        "KEPRWPDTPKEE"
    )
    repetitions = find_repetitions(c=c, min_length=6)
    assert all(
        seq in repetitions for seq in ["ODBODGR", "THNVXS"]
    )  # ODBODGR and THNVXS appear twice in the ciphertext
    assert (
        find_distance_between_repititions(c=c, repitition="ODBODGR") == 102
    )  # ODBODGR appears 102 characters apart
    assert (
        find_distance_between_repititions(c=c, repitition="THNVXS") == 120
    )  # THNVXS appears 120 characters apart
    candidates = common_factors(102, 120)
    assert candidates == [1, 2, 3, 6]
    m, predicted_key = kasiski(c=c, key_length=3)
    assert m == (
        "CHARLESBABBAGEWASANECCENTRICGENIUSBESTKNOWNFORDEVELOPINGTHEBLUEPRINTFORTHE"
        "MODERNCOMPUTERHEWASTHESONOFBENJAMINBABBAGEAWEALTHYLONDONBANKERHEAPPLIEDHISGENIUSTO"
        "MANYPROBLEMSHISINVENTIONSINCLUDETHESPEEDOMETERANDTHECOWCATCHER"
    ) and (predicted_key == "ZMW")
    # We can now see THNVXS -> GENIUS
    # ODBODGR -> BABBAGE


def test_vigenere():
    c = vigenere(m="AbCd", key="aBc")
    assert c == "ACED"


if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__, "-s"]))
