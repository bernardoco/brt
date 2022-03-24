__all__ = [
    "fetch_json_data",
    "save_to_csv"
]

import requests
import pandas as pd


def fetch_json_data(url: str):
    res = requests.get(url)
    return res.json()['veiculos']


def save_to_csv(df: pd.DataFrame, filename: str):
    df = pd.DataFrame.from_dict(eval(df))
    if not filename.endswith('.csv'):
        filename += '.csv'

    return df.to_csv(filename, index=False)