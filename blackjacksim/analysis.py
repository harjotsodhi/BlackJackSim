import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings("ignore")


def sim_stats(arr):
    """
    Descriptive statistics of simulation results.

    Parameters
    ----------
    arr: np.array
        Array of BlackJack simulation results.
    """
    print(f"Count : {arr.shape[0]}")
    print(f"Mean  : ${round(arr.mean(),3)}")
    print(f"Std   : ${round(np.std(arr),3)}")
    print(f"Max   : ${arr.max()}")
    print(f"Min   : ${arr.min()}")


def plot_hist(arr):
    """
    Plot a histogram of the winnings over n games.
        Overlay a kernel density estimate (KDE) plot.

    Save the figure in the current directory.
        Does not print output.

    Parameters
    ----------
    arr: np.array
        Array of BlackJack simulation results.
    """
    fig, ax1 = plt.subplots()
    ax2 = ax1.twinx() # twin axis sharing the x-axis
    sns.distplot(arr, kde=False, ax=ax1)
    sns.distplot(arr, hist=False, ax=ax2, kde_kws={'bw_method':1})
    ax1.set_title(f"Results of {arr.shape[0]} games of BlackJack")
    ax1.set_xlabel("Winnings")
    ax1.set_ylabel("Number of games")
    ax2.set(yticklabels=[])
    ax2.set(ylabel=None)
    fig.savefig('figure1.png')
    plt.close(fig)
