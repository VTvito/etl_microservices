def apply_transformations(df):
    """
    Apply trasformation on data
    In this case we're going to delete null values and add new colums
    """
    
    df_clean = df.dropna()
    
    first_column = df_clean.columns[0]

    # create a new column (multiply * 2 the values )
    df_clean['new_column'] = df_clean[first_column] * 2  

    return df_clean