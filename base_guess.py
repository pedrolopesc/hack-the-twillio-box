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

def max_letters(li_vowels: list[int]) -> int:
    return sum(li_vowels)

def create_dataset(dfin: pd.DataFrame) -> pd.DataFrame:
    df = dfin.copy()
    df['len'] = df['palavras'].apply(lambda x: len(x))
    df['acento'] = df['palavras'].apply(lambda x: x != unidecode(x))
    df['sigla'] = df['palavras'].apply(lambda x: x == x.upper())
    df['nome_capital'] = df['palavras'].apply(lambda x: x == x.lower())
    dfout = df[(df.len == 5) & (~df.acento) & (~df.sigla) & (df.nome_capital)].copy()
    dfout = dfout.pipe(has_wy)
    dfout['vec_palav'] = dfout['palavras'].apply(lambda x: list(x))
    dfout['vec_aeiou'] = dfout['palavras'].apply(count_vowels)
    dfout['vec_conso'] = dfout['palavras'].apply(count_consonants)

    dfout['count_vowels'] = dfout['vec_aeiou'].apply(max_letters)
    dfout['count_cons'] = dfout['vec_conso'].apply(max_letters)
    return dfout[['palavras', 'vec_palav', 'vec_aeiou', 'count_vowels', 'vec_conso', 'count_cons']]
