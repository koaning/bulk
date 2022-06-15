import numpy as np
import pandas as pd
from bokeh.layouts import column, row
from bokeh.models import (Button, ColumnDataSource, TextInput)
from bokeh.models import DataTable, TableColumn
from bokeh.plotting import figure

from .utils import add_color_mapping, get_datatable_columns


def bulk_text(path):
    def bkapp(doc):
        df = pd.read_csv(path)
        highlighted_idx = []

        datatable_columns = get_datatable_columns(df)
        columns = [
            TableColumn(field=col, title=col) for col in datatable_columns
        ]

        def update(attr, old, new):
            """Callback used for plot update when lasso selecting"""
            global highlighted_idx
            subset = df.iloc[new]
            highlighted_idx = new
            subset = subset.iloc[np.random.permutation(len(subset))]
            source.data = subset

        def save():
            """Callback used to save highlighted data points"""
            df.iloc[highlighted_idx][datatable_columns].to_csv(text_filename.value)

        has_labels = "labels" in df.columns
        if has_labels:
            df = add_color_mapping(df)

        source = ColumnDataSource(data=dict())
        source_orig = ColumnDataSource(data=df)

        data_table = DataTable(source=source, columns=columns, width=800)
        source.data = df

        p = figure(title="", sizing_mode="scale_both", tools="lasso_select")

        circle_kwargs = {"x": "x", "y": "y", "size": 1, "source": source_orig}
        if has_labels:
            circle_kwargs.update({"color": "color", "legend": "labels"})

        scatter = p.circle(**circle_kwargs)
        p.plot_width = 600
        p.plot_height = 600

        scatter.data_source.selected.on_change('indices', update)

        text_filename = TextInput(value="out.csv", title="Filename:")
        save_btn = Button(label="SAVE")
        save_btn.on_click(save)

        controls = column(p, text_filename, save_btn)
        return doc.add_root(
            row(controls, data_table)
        )

    return bkapp
