from typing import Tuple, Optional

import bokeh.transform
import numpy as np
import pandas as pd
from bokeh.palettes import Category10, Cividis256
from bokeh.transform import linear_cmap, factor_cmap


def get_color_mapping(df: pd.DataFrame) -> Tuple[Optional[bokeh.transform.transform], pd.DataFrame]:
    """Creates a color mapping"""
    if "color" not in df.columns:
        return None, df

    color_datatype = str(df["color"].dtype)
    if color_datatype == "object":
        df["color"] = df["color"].apply(
            lambda x: str(x) if not (type(x) == float and np.isnan(x)) else x
        )
        all_values = list(df["color"].dropna().unique())
        if len(all_values) == 2:
            all_values.extend([""])
        mapper = factor_cmap(
            field_name="color",
            palette=Category10[len(all_values)],
            factors=all_values,
            nan_color="grey"
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
    return mapper, df
