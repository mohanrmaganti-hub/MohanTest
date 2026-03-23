import pandas as pd


def transform_records(records, mapping):
    """Simple transformation: select mapping keys and ensure consistent columns"""
    df = pd.DataFrame(records)
    if df.empty:
        return df
    # rename columns according to mapping
    df = df.rename(columns=mapping)
    # keep only the mapped columns
    df = df[list(mapping.values())]
    return df
