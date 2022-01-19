import pandas as pd
import os
import logging
from pokec.utils import time_summary
from pokec.cache import Cache

pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

dir_path = os.path.abspath(os.path.join(os.path.dirname(__file__)))


class DataInterface(Cache):

    def __init__(self):
        super().__init__()
        self.data_file = 'Cleaned_pokec_dataset'
        self.sample_data_file = 'Cleaned_sample'

    @time_summary
    def read(self, read_sample):
        logging.info("Reading Data")
        file = self.data_file
        if read_sample:
            file = self.sample_data_file
        try:
            df = self.read_parquet_df(file)
            logging.info(f"Raw data shape: {df.shape}")
            return df
        except OSError:
            raise Exception(f"Please add file {file} in the directory: {dir_path}")
