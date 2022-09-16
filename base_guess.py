from unidecode import unidecode
import re
import pandas as pd

def read_database(addr: str='palavras.txt') -> pd.DataFrame:
    def words(text: str) -> str:
        return re.findall(r'\w+', text)
    li_pal = list(set(words(open(addr,encoding="utf8").read())))
    return pd.DataFrame({'palavras': li_pal})

def count_vowels(palavra: str) -> list[int]:
    li_pal = list(map(palavra.count, "aeiou"))
    return [int(bool(let)) for let in li_pal]

def count_consonants(palavra: str) -> list[int]:
    li_pal = list(map(palavra.count, "bcdfghjklmnpqrstvxz"))
    return [int(bool(let)) for let in li_pal]

def has_wy(dfin: pd.DataFrame) -> pd.DataFrame:
    dfout = dfin[~dfin['palavras'].str.contains('w|y')].copy()
    return dfout
