def apply_transformations(df):
    """
    Apply trasformation on data
    In this case we're going to delete null values
    """
    df_clean = df.dropna()
    return df_clean