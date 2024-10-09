from typing import Optional

import pandas as pd


def recursive_explode_flatten_dataframe(df: pd.DataFrame, max_normalize_level: Optional[int] = None):
    """Explode and flatten a dataframe, ensuring single-value lists are split into columns."""
    # Explode lists
    if any(
        list_cols := [
            all(col_not_na.apply(lambda x: isinstance(x, list))) if len(col_not_na := df[col].dropna()) else False
            for col in df.columns
        ]
    ):
        for col in df.columns[list_cols]:
            df = df.explode(col)
        df = df.reset_index(drop=True)

    # Normalize dictionaries
    if any(
        dict_cols := [
            all(col_not_na.apply(lambda x: isinstance(x, dict))) if len(col_not_na := df[col].dropna()) else False
            for col in df.columns
        ]
    ):
        for col in df.columns[dict_cols]:
            df = df.join(pd.json_normalize(df[col], max_level=max_normalize_level)).drop(columns=col)
        if max_normalize_level != 0:
            df = recursive_explode_flatten_dataframe(df, (max_normalize_level - 1) if max_normalize_level else None)

    if any(
        list_cols := [
            all(col_not_na.apply(lambda x: isinstance(x, list))) if len(col_not_na := df[col].dropna()) else False
            for col in df.columns
        ]
    ):
        for col in df.columns[list_cols]:
            # Determine the maximum list length in the column
            max_length = df[col].dropna().apply(len).max()
            # Create new columns for each index in the list
            for i in range(max_length):
                # Define new column name with _idx suffix
                new_col_name = f"{col}_{i}"
                # Extract the element at index i from each list (or None if the list is too short)
                df[new_col_name] = df[col].apply(lambda x: x[i] if i < len(x) else None)
            # Drop the original list columns
            df = df.drop(columns=[col])

    return df.reset_index(drop=True)
