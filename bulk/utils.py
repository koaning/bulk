import random
from typing import List

import matplotlib.colors as mcolors
import pandas as pd


def add_color_mapping(df: pd.DataFrame) -> pd.DataFrame:
    """Creates a label -> css4 color mapping"""
    all_labels = list(df["labels"].unique())
    all_colors = list(mcolors.CSS4_COLORS.values())

    random.shuffle(all_colors)
    color_mapping = {label: color for label, color in zip(all_labels, all_colors)}
    df["color"] = df["labels"].apply(lambda x: color_mapping[x])
    return df


def get_datatable_columns(df: pd.DataFrame) -> List[str]:
    """"""
    columns = df.columns
    return [c for c in columns if c not in ["x", "y"]]
