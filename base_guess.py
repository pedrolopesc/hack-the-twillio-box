"""Code to play wordly game.
"""
from unidecode import unidecode
from typing import Any
import re
import pandas as pd

BASE = ['MUNDO', 'OUVIR', 'AMIGO', 'FELIZ', 'AJUDA', 'FONTE', 'MURAL', 'PAPEL', 'VENDA', 'OLHAR',
        'PORTA', 'RAMAL', 'ZELAR', 'VIDEO', 'RADAR', 'FALAR', 'ONDAS', 'LIVRE', 'NIVEL', 'CANAL',
        'MUDAR', 'LIGAR', 'BOTAO', 'PRATA', 'LEADS', 'PONTE', 'TOTAL', 'OLHOS', 'BOLHA', 'VALOR',
        'VISAO', 'ROLHA', 'IDEIA', 'UNICO', 'UNIAO', 'CRIAR', 'LIDER']

def read_database(addr: str='palavras.txt', flag_pre_base: bool=True) -> pd.DataFrame:
    """Load dataset.

    Args:
        addr (str, optional): File location with portuguses words. Defaults to 'palavras.txt'.
        flag_pre_base (bool, optional): Load words by BASE variable. Defaults to True.

    Returns:
        pd.DataFrame: DataFrame with single words column.
    """
    def words(text: str) -> str:
        return re.findall(r'\w+', text)
    if flag_pre_base:
        li_pal = [bas.lower() for bas in BASE]
    else:
        li_pal = list(set(words(open(addr,encoding="utf8").read())))
    return pd.DataFrame({'palavras': li_pal})

def count_vowels(palavra: str) -> list[int]:
    """Count each vowel occurring once.

    Args:
        palavra (str): word

    Returns:
        list[int]: boolean vector
    """
    li_pal = list(map(palavra.count, "aeiou"))
    return [int(bool(let)) for let in li_pal]

def count_consonants(palavra: str) -> list[int]:
    """Count each consoant occurring once.

    Args:
        palavra (str): word

    Returns:
        list[int]: boolean vector
    """
    li_pal = list(map(palavra.count, "bcdfghjklmnpqrstvxz"))
    return [int(bool(let)) for let in li_pal]

def has_wy(dfin: pd.DataFrame) -> pd.DataFrame:
    """Romove words with "y" or "w" from dataset

    In portuese there are no words with these letters

    Returns:
        pd.DataFrame: DataFrame with single words column filtered.
    """
    return dfin[~dfin['palavras'].str.contains('w|y')].copy()

def max_letters(li_bool_vec: list[int]) -> int:
    """Count distinct words.

    Args:
        li_vowels (list[int]): 0 or 1 vector

    Returns:
        int: Amount.
    """
    return sum(li_bool_vec)

def create_dataset() -> pd.DataFrame:
    """Create dataset DataFrame with columns to analyse words.

    Returns:
        pd.DataFrame: DataFrame with words and descriptive columns.
    """
    df = read_database()
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

def filter_words(word: str, li_guess: list[str]) -> bool:
    """True if has letter in correct position

    Args:
        word (_type_): word
        li_guess (_type_): vector with gueeses

    Returns:
        bool: True if word has letters
    """
    return all([((word[num]==li_guess[num]) | (li_guess[num] is None)) for num in range(5)])

def filter_df_green(dfin: pd.DataFrame, guess_green: list[str]) -> pd.DataFrame:
    """Select words by green color return

    Args:
        dfin (pd.DataFrame): dataset
        guess_green (list[str]): color vector

    Returns:
        pd.DataFrame: filtered dataset
    """
    return dfin[dfin.vec_palav.apply(lambda x: filter_words(x, guess_green))].copy()

def filter_df_yelw(dfin: pd.DataFrame, guess_yelw: list[str]) -> pd.DataFrame:
    """Select words by yellow color return

    Args:
        dfin (pd.DataFrame): dataset
        guess_green (list[str]): color vector

    Returns:
        pd.DataFrame: filtered dataset
    """
    dfout = dfin.copy()
    df_masks= [dfout.palavras.str.contains(g_y) for g_y in guess_yelw]
    return dfout[pd.concat(df_masks, axis=1).apply(lambda x: all(x), 1)]

def filter_df_not_cont(dfin: pd.DataFrame, guess_not: list[str]) -> pd.DataFrame:
    """Select words that doesn't has letters, black color
    Args:
        dfin (pd.DataFrame): dataset
        guess_green (list[str]): color vector

    Returns:
        pd.DataFrame: filtered dataset
    """
    dfout = dfin.copy()
    if 'g' in guess_not:
        df_masks= [~dfout.palavras.str.contains(g_y) for g_y in guess_not]
        dfout = dfout[pd.concat(df_masks, axis=1).apply(lambda x: all(x), 1)].copy()
    return dfout

def filter_df_not(dfin: pd.DataFrame, guess_green: list[str]) -> pd.DataFrame:
    """Select words by green color return

    Args:
        dfin (pd.DataFrame): dataset
        guess_green (list[str]): color vector

    Returns:
        pd.DataFrame: filtered dataset
    """
    return dfin[~dfin.vec_palav.apply(lambda x: filter_words(x, guess_green))].copy()

dfbase = create_dataset()

def step_guess(wordin: str,
               vec_color_return: list[str],
               dfbase: pd.DataFrame=dfbase) -> pd.DataFrame:
    """Return DataFrame with avaiable word options.

    Args:
        wordin (str): Word to insert
        vec_color_return (list[str]): Returned vector color from game
        dfbase (pd.DataFrame, optional): Avaiable words when it begins. Defaults to dfbase.

    Returns:
        pd.DataFrame: DataFrame with avaiable word options after guess.
    """
    dfin = dfbase.copy()
    guess_g = [w if v == 'g' else None for w, v in zip(list(wordin), vec_color_return)]
    guess_y = [w if v == 'y' else None for w, v in zip(list(wordin), vec_color_return)]
    guess_not_cont = [w for w, v in zip(list(wordin), vec_color_return) if v is None]
    guess_yel = list(set(guess_y) - {None})
    dfgreen = filter_df_green(dfin, guess_g)
    dfgreen_not = filter_df_not_cont(dfgreen, guess_not_cont)
    if guess_yel:
        dfyello = filter_df_yelw(dfgreen_not, guess_yel)
        dfnotco = filter_df_not(dfyello, guess_y)
    else:
        dfnotco = dfgreen_not
    return dfnotco.sort_values(by=['count_vowels', 'count_cons'], ascending=[False, False])
