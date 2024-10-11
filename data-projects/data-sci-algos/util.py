import pandas as pd 
import numpy as np
import itertools

def is_one_hot_encoded(df):
    """
    This function checks to see if the csv is simply in this format:

    ** Obviously spaces omitted for true applications, spaces added here for readability **

    transactionID,item1,item2,item3,item4, ... ,itemX
    1            ,  0  ,  1  ,  0  ,  0  , ... ,  x
    2            ,  1  ,  0  ,  1  ,  1  , ... ,  x
    ...
    x            , x   ,  x  ,  x  ,  x  , ... ,  x

    """

    if 'transactionID' in df.columns:
        df = df.drop(columns=['transactionID'])
    
    return df.isin([0, 1]).all().all()

def calculate_support_one(df, column):
    """
    Calculate the support for a given item (column) in a one-hot encoded DataFrame.

    Args:
    - df: A Pandas DataFrame where each row represents a transaction and each column represents an item.
    - column: The name of the column (item) for which to calculate support.

    Returns:
    - Support: The proportion of transactions that contain the item.
    """
    if 'transactionID' in df.columns:
        df = df.drop(columns=['transactionID'])
    
    total_transactions = len(df)

    item_count = df[column].sum()
    
    # Calculate the support as the proportion of transactions containing the item
    support = item_count / total_transactions
    
    return support

def create_combo_one(df,k,):
    if(k == 1):
        return list(itertools.combinations(df.columns.drop('transactionID'), k))
    else:


def apriori(df, threshold, k):
    """ 
    This Algo is meant to take a pandas one-hot encoding of purchased itemsets and run apriori on them formatting should look as such

    ** Obviously spaces omitted for true applications, spaces added here for readability **

    transactionID,item1,item2,item3,item4, ... ,itemX
    1            ,  0  ,  1  ,  0  ,  0 , ... ,   x
    2            ,  1  ,  0  ,  1  ,  1 , ... ,   x
    ...
    x            ,  x  ,  x  ,  x  ,  x , ... ,   x

    This will run apriori and return a frequent itemset
    """

    if not isinstance(df, pd.DataFrame):
        print("DataFrame in Apriori function isn't a DataFrame")
        return 0

    if not is_one_hot_encoded(df):
        print ("DataFrame in Apriori function isn't one-hot encoded")
        return 0

    running_list = df.columns.drop('transactionID')
    
    # Remove one-itemsets that don't meet the threshold
    for item in running_list:
        support = calculate_support_one(df, item)
        print(support)
        print(threshold)
        if support < threshold:
            df = df.drop(columns=item)

    

if __name__ == "__main__":
    apriori(pd.read_csv("data-sci-algos/test_transactions.csv"), .6, 1)