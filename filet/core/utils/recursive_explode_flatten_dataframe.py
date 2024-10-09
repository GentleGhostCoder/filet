from typing import Optional

import pandas as pd


def recursive_explode_flatten_dataframe(df: pd.DataFrame, max_normalize_level: Optional[int] = None):
    """Explode and flatten a dataframe."""
    if any(
        list_cols := [
            all(col_not_na.apply(lambda x: isinstance(x, list))) if len(col_not_na := df[col].dropna()) else False
            for col in df.columns
        ]
    ):
        for col in df.columns[list_cols]:
            df = df.explode(col)
        df = df.reset_index(drop=True)
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
    return df.reset_index(drop=True)
