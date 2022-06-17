from typing import List

import bokeh.transform
import pandas as pd
from bokeh.palettes import Cividis256, cividis
from bokeh.transform import linear_cmap, factor_cmap


def get_color_mapping(df: pd.DataFrame) -> bokeh.transform.transform:
    """Creates a color mapping"""
    color_datatype = str(df["color"].dtype)
    if color_datatype == "object":  # string
        all_values = list(df["color"].unique())
        palette = cividis(len(all_values))
        mapper = factor_cmap(
            field_name="color",
            palette=palette,
            factors=all_values
        )
    elif color_datatype.startswith("float") or color_datatype.startswith("int"):
        all_values = df["color"].dropna().values
        mapper = linear_cmap(
            field_name="color",
            palette=Cividis256,
            low=all_values.min(),
            high=all_values.max(),
            nan_color="grey"
        )
    else:
        raise TypeError(
            f"We currently only support the following type for 'color' column: 'int*', 'float*', 'object'. "
            f"Got {color_datatype}."
        )
    return mapper


def get_datatable_columns(df: pd.DataFrame) -> List[str]:
    """"""
    columns = df.columns
    filtered_columns = []
    for c in columns:
        if c in ["x", "y"] or c.startswith("Unnamed"):
            continue
        filtered_columns.append(c)
    return filtered_columns
