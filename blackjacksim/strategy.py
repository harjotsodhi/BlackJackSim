import pandas as pd


def read_strategy(csv_name="basic_strategy"):
    """
    Read in a BlackJack strategy stored within a csv
        and return it as three pandas dataframes,
        representing the hard, soft, and split strategy.

    Aces should be coded as "11"
    Face cards should be coded as "10"

    Parameters
    ----------
    csv_name: str, default="basic_strategy"
        name of the strategy contained in a csv in the
        "/strategy" subdirectory
    """
    name = f"blackjacksim/strategies/{csv_name}.csv"
    df=pd.read_csv(name, sep=',',header=0, index_col=0)
    df.index = df.index.astype(int)
    df.columns = df.columns.astype(int)
    hard = df.iloc[:17]
    soft = df.iloc[17:26]
    split = df.iloc[26:]
    return hard, soft, split
