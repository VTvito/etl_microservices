import pyarrow as pa

def apply_transformations(arrow_table):
    """
    Cleans the data by dropping rows with null values.

    Args:
        arrow_table (pyarrow.Table): Input Arrow Table to be cleaned.

    Returns:
        pyarrow.Table: Cleaned Arrow Table with no null values.
    """
    try:
        # Convert to Pandas for easier manipulation
        df = arrow_table.to_pandas()

        # Drop rows with NaN values
        df_cleaned = df.dropna()

        # Convert back to Arrow Table
        cleaned_arrow_table = pa.Table.from_pandas(df_cleaned)
        return cleaned_arrow_table
    except Exception as e:
        raise ValueError(f"Failed to clean data: {e}")