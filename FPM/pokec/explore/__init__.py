from pokec.explore.viz import Viz
from pokec.cache import Cache
import numpy as np


def re_scale(items):
    range_value = max(items) - min(items)
    range_value = range_value + range_value / 50
    min_value = min(items) - range_value / 100

    for index, item in enumerate(items):
        items[index] = (item - min_value) / range_value
    return items


class Explore(Viz, Cache):

    def __init__(self):
        Viz.__init__(self)
        Cache.__init__(self)
        self.ap_out = self.read_parquet_df('ap_association_rules_output')
        self.seq_out = self.read_parquet_df('sequential_patterns_output')
        self.cp_out = self.read_parquet_df('colossal_mining_output')

    def plot_sup_vs_time(self):
        cond = self.ap_out['data_length'] == self.ap_out['data_length'].max()
        ap = self.ap_out.loc[cond, ['time_taken', 'min_sup']].drop_duplicates().rename(columns={
            'time_taken': 'Ap Association Rules', 'min_sup': 'Min Support'
        }).set_index('Min Support')

        cond = self.seq_out['data_length'] == self.seq_out['data_length'].max()
        seq = self.seq_out.loc[cond, ['time_taken', 'min_sup']].drop_duplicates().rename(columns={
            'time_taken': 'Sequential Patterns', 'min_sup': 'Min Support'
        }).set_index('Min Support')

        cond = self.cp_out['data_length'] == self.cp_out['data_length'].max()
        cp = self.cp_out.loc[cond, ['time_taken_rules', 'min_sup']].drop_duplicates().rename(columns={
            'time_taken_rules': 'Colossal Patterns', 'min_sup': 'Min Support'
        }).set_index('Min Support')
        st = ap.join(seq).join(cp)
        self.line_plot(st, 'Min Support Vs Time(s)')

    def plot_data_len_vs_time(self):
        cond = self.ap_out['min_sup'] == self.ap_out['min_sup'].max()
        ap = self.ap_out.loc[cond, ['time_taken', 'data_length']].drop_duplicates().rename(columns={
            'time_taken': 'Ap Association Rules', 'data_length': 'Records'
        }).set_index('Records')

        cond = self.seq_out['min_sup'] == self.seq_out['min_sup'].max()
        seq = self.seq_out.loc[cond, ['time_taken', 'data_length']].drop_duplicates().rename(columns={
            'time_taken': 'Sequential Patterns', 'data_length': 'Records'
        }).set_index('Records')

        cond = self.cp_out['min_sup'] == self.cp_out['min_sup'].max()
        cp = self.cp_out.loc[cond, ['time_taken_rules', 'data_length']].drop_duplicates().rename(columns={
            'time_taken_rules': 'Colossal Patterns', 'data_length': 'Records'
        }).set_index('Records')
        st = ap.join(seq).join(cp)
        self.line_plot(st, 'Number of Records Vs Time(s)')

    def confidence_vs_lift(self, df, method, n=100000):
        df = df.iloc[:n]
        cond = df['data_length'] == df['data_length'].max()
        df = df[cond]
        sup = "Min Support: " + df['min_sup'].round(3).astype(str)
        sup_col_map = {'Min Support: 0.004': 'blue', 'Min Support: 0.006': 'green', 'Min Support: 0.008': 'red'}
        self.sp_with_legend(df['confidence'], df['lift'], xlabel='Confidence', ylabel='Lift',
                            cdict=sup_col_map, classes=sup,
                            title=f'Confidence Vs Lift for {method}')

    def explore_ap(self):
        self.ap_out = self.ap_out.sort_values('support', ascending=False)
        self.ap_out['items'] = self.ap_out['items'].apply(lambda x: ', '.join(x))
        ap = self.ap_out.copy()

        self.confidence_vs_lift(ap, method='Ap Association Rules')

        freq_items = ap.groupby(['items'])['support'].max().reset_index().sort_values(
            'support', ascending=False).head(11).iloc[1:]
        freq_items['support_log10'] = freq_items['support'].apply(np.log10)
        freq_items_d = dict(zip(freq_items['items'], freq_items['support_log10']))

        self.plot_wordcloud(freq_items_d, title='Most Frequent item sets Ap Association Rules')

        self.bar_plot(freq_items['items'], freq_items['support'], xlabel='Frequent Items', ylabel='Support',
                      title='Top 10 Frequent Items with Support for Ap Association Rules', degrees=90)

        self.hist_plot(ap['support'], title='Support Histogram for Ap Association Rules',
                       xlabel='Support', ylabel='Frequency')

    def explore_seq(self):
        seq = self.seq_out
        seq['items'] = seq['1'].apply(lambda x: ', '.join(x))
        seq = seq.sort_values('0', ascending=False)

        freq_items = seq.groupby(['items'])['0'].max().reset_index().sort_values(
            '0', ascending=False).head(11).iloc[1:]
        freq_items['support_log10'] = freq_items['0'].apply(np.log10)
        freq_items_d = dict(zip(freq_items['items'], freq_items['support_log10']))
        self.plot_wordcloud(freq_items_d, title='Most Frequent item sets by Sequential Patterns')

        freq_items['Freq'] = re_scale(freq_items['0'].tolist())
        self.bar_plot(freq_items['items'], freq_items['Freq'], xlabel='Frequent Items', ylabel='Scaled Frequency',
                      title='Top 10 Frequent Items with Support for Sequential Patterns', degrees=90)

        t = seq[['time_taken', 'data_length']].drop_duplicates().rename(columns={
            'time_taken': 'Time', 'data_length': 'Records'
        }).set_index('Records')
        self.line_plot(t, 'Number of records vs Time by Sequential Patterns')

    def explore_cp(self):
        cp = self.cp_out.copy()
        cp = cp.sort_values('support', ascending=False)
        cp['items'] = cp['consequents'].apply(lambda x: ', '.join(x)) + ", " + cp['antecedents'].apply(lambda x: ', '.join(x))

        self.confidence_vs_lift(cp, method='Colossal Mining')

        freq_items = cp.groupby(['items'])['support'].max().reset_index().sort_values(
            'support', ascending=False).head(10)
        freq_items['support_log10'] = freq_items['support'].apply(np.log10)
        freq_items_d = dict(zip(freq_items['items'], freq_items['support_log10']))
        self.plot_wordcloud(freq_items_d, title='Most Frequent item sets for Colossal Mining')

        self.bar_plot(freq_items['items'], freq_items['support'], xlabel='Frequent Items', ylabel='Support',
                      title='Top 10 Frequent Items with Support for Colossal Mining', degrees=90)

    def run(self):
        self.plot_sup_vs_time()
        self.plot_data_len_vs_time()
        self.explore_ap()
        self.explore_seq()
        self.explore_cp()
