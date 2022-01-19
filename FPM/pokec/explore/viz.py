import matplotlib.pyplot as plt
import os
import numpy as np
from wordcloud import WordCloud

directory = os.path.abspath(os.path.join(os.path.dirname(__file__)))
plots_dir = f"{directory}/plots"
tables_dir = f"{directory}/tables"


class Viz:

    def __init__(self):
        if not os.path.exists(plots_dir):
            os.makedirs(plots_dir)
        if not os.path.exists(tables_dir):
            os.makedirs(tables_dir)

    @staticmethod
    def bar_plot(x, y, xlabel=None, ylabel=None, title=None, degrees=None, color='maroon'):
        plt.bar(x, y, color=color, width=0.4)
        if degrees:
            plt.xticks(rotation=degrees)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.title(f"{title}")
        plt.tight_layout()
        plt.savefig(f"{plots_dir}/{title}")
        plt.show()

    @staticmethod
    def line_plot(df, title):
        df.plot()
        plt.title(f"{title}")
        plt.tight_layout()
        plt.savefig(f"{plots_dir}/{title}")
        plt.show()

    @staticmethod
    def hist_plot(series, title, xlabel=None, ylabel=None):
        series.hist()
        plt.title(f"{title}")
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.tight_layout()
        plt.savefig(f"{plots_dir}/{title}")
        plt.show()

    @staticmethod
    def scatter_plot(x, y, title, c=None, xlabel=None, ylabel=None):
        plt.scatter(x, y, c=c)
        plt.title(f"{title}")
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.tight_layout()
        plt.savefig(f"{plots_dir}/{title}")
        plt.show()

    @staticmethod
    def sp_with_legend(x, y, cdict, classes, title, xlabel=None, ylabel=None):
        fig, ax = plt.subplots()
        for g in np.unique(classes):
            ix = np.where(classes == g)
            ax.scatter(x.iloc[ix], y.iloc[ix], c=cdict[g], label=g, s=100)
        ax.legend()
        plt.title(f"{title}")
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.tight_layout()
        plt.savefig(f"{plots_dir}/{title}")
        plt.show()

    @staticmethod
    def grouped_bar_plot(df, title, xlabel=None, ylabel=None):
        df.plot(kind='bar')
        plt.title(f"{title}")
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.tight_layout()
        plt.savefig(f"{plots_dir}/{title}")
        plt.show()

    @staticmethod
    def plot_wordcloud(items, title, color='salmon'):
        wc = WordCloud(width=3000,
                      height=2000,
                      random_state=1,
                      background_color=color,
                      colormap='Pastel1',
                      collocations=False).generate_from_frequencies(items)
        plt.figure(figsize=(40, 30))
        plt.title(title)
        plt.imshow(wc)
        plt.savefig(f"{plots_dir}/{title}")
        plt.show()

    @staticmethod
    def export_table_as_csv(df, filename):
        df.to_csv(f"{tables_dir}/{filename}.csv", index=False)
