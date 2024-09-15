def apply_transformations(df):
    """
    Apply trasformation on data
    In this case we're going to delete null values and add new colums
    """
    
    df_clean = df.dropna()
    
    # df_clean['new_column'] = df_clean['existing_column']*2
    df.loc[:, 'new_column'] = df['existing_column'] * 2 # to avoid CopyWarning

    return df_clean