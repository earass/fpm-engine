from mlxtend.frequent_patterns import apriori as ap
from mlxtend.frequent_patterns import association_rules as ar
from apyori import apriori
import pandas as pd
from pokec.utils import time_summary
from prefixspan import PrefixSpan
from pokec.cache import Cache
from pokec.engine.pcp_miner import CPMiner
import time
import logging


class FPM(Cache):

    def __init__(self, df):
        Cache.__init__(self)
        self.df = df
        self.sup_list = [0.004, 0.006, 0.008]
        self.data_lengths = [50000, 100000, 200000, 500000, 700000]

    @time_summary
    def ap_association_rules(self):
        all_df = pd.DataFrame()
        for sup in self.sup_list:
            for n in self.data_lengths:
                logging.info(f"Running association rules for min support: {str(sup)} and {str(n)} records")
                start = time.time()
                records = self.df.astype(str).values.tolist()

                association_rules = apriori(records, min_support=sup, min_confidence=0.2, min_lift=3, min_length=2,
                                            max_length=3)
                association_results = list(association_rules)
                f_items = pd.DataFrame(association_results)
                f_items['confidence'] = f_items['ordered_statistics'].apply(lambda x: x[0][2])
                f_items['lift'] = f_items['ordered_statistics'].apply(lambda x: x[0][3])
                f_items = f_items[['items', 'support', 'confidence', 'lift']]
                f_items['items'] = f_items['items'].apply(lambda x: list(x))
                end = time.time()
                time_taken = end - start
                f_items['time_taken'] = time_taken
                f_items['min_sup'] = sup
                f_items['data_length'] = n
                print(f_items)
                print(f_items.shape)
                all_df = pd.concat([all_df, f_items], ignore_index=True)
        self.save_df_as_parquet(all_df, 'ap_association_rules_output')

    @time_summary
    def sequential_patterns(self, min_len=2, max_len=3, freq=20000):
        all_df = pd.DataFrame()
        for sup in self.sup_list:
            for n in self.data_lengths:
                logging.info(f"Running Sequential Patterns for min support: {str(sup)} and {str(n)} records")
                start = time.time()
                data = self.df.iloc[:n].values.tolist()
                ps = PrefixSpan(data)
                ps.maxlen = max_len
                ps.minlen = min_len
                ps_df = pd.DataFrame(ps.frequent(freq*sup)).sort_values(0, ascending=False)
                ps_df.columns = [str(i) for i in ps_df.columns]
                end = time.time()
                time_taken = end - start
                ps_df['time_taken'] = time_taken
                ps_df['min_sup'] = sup
                ps_df['data_length'] = n
                print(ps_df)
                all_df = pd.concat([all_df, ps_df], ignore_index=True)
        self.save_df_as_parquet(all_df, 'sequential_patterns_output')

    @time_summary
    def colossal_miner(self):
        all_df = pd.DataFrame()
        for n in self.data_lengths:
            logging.info(f"Running Colossal Miner for {str(n)} records")
            df = self.df.iloc[:n]
            start = time.time()
            cp_miner = CPMiner(df)
            cp_miner.preprocess_1_itemset()
            cp_miner.assign_dbv()
            cp_miner.maketree(cp_miner.dbv)
            patterns = cp_miner.colossal_pattern
            cols = list(cp_miner.map_bits.keys())
            df = pd.DataFrame(patterns, columns=cols)
            print(df.head())
            print(df.shape)
            end = time.time()
            time_taken_cp = end - start

            for sup in self.sup_list:
                logging.info(f"CP Miner rules for min support: {str(sup)}")
                start = time.time()
                frequent_itemsets = ap(df, min_support=sup, use_colnames=True, max_len=3)
                rules = ar(frequent_itemsets, metric="lift", min_threshold=1)
                rules['antecedents'] = rules['antecedents'].apply(lambda x: list(x))
                rules['consequents'] = rules['consequents'].apply(lambda x: list(x))
                end = time.time()
                time_taken_rules = end - start
                rules['time_taken_cp'] = time_taken_cp
                rules['time_taken_rules'] = time_taken_rules
                rules['min_sup'] = sup
                rules['data_length'] = n
                print(rules.head())
                print(rules.shape)
                all_df = pd.concat([all_df, rules], ignore_index=True)
        self.save_df_as_parquet(all_df, 'colossal_mining_output')

    def run(self):
        self.ap_association_rules()
        self.sequential_patterns()
        self.colossal_miner()
