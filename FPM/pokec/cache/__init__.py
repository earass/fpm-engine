import pandas as pd
import os
import logging

directory = os.path.abspath(os.path.join(os.path.dirname(__file__), 'files'))


class Cache:

    def __init__(self):
        pass

    @staticmethod
    def save_df_as_parquet(df, file_name):
        path = f'{directory}/{file_name}.parquet'
        df.to_parquet(path)

    @staticmethod
    def read_parquet_df(filename, columns=None):
        df = pd.read_parquet(f'{directory}/{filename}.parquet', "pyarrow", columns=columns)
        return df

    @staticmethod
    def export_df_as_csv(df, file_name):
        file_path = f'{directory}/{file_name}.csv'
        df.to_csv(file_path, index=False)
        logging.info(f"File saved on path: {file_path}")
