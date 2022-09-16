from unidecode import unidecode
import re
import pandas as pd

def read_database(addr: str='palavras.txt') -> pd.DataFrame:
    def words(text: str) -> str:
        return re.findall(r'\w+', text)
    li_pal = list(set(words(open(addr,encoding="utf8").read())))
    return pd.DataFrame({'palavras': li_pal})
