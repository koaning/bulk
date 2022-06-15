from tornado.ioloop import IOLoop

import numpy as np
import pandas as pd

from bokeh.io import curdoc
from bokeh.layouts import column, row
from bokeh.models import (Button, ColumnDataSource, DataTable, TableColumn, TextInput)
from bokeh.plotting import figure
from bokeh.models import DataTable, TableColumn

def bulk_text(path):

    def bkapp(doc):
        df = pd.read_csv(path)
        saved_idx = []
        highlighed_idx = []

        source = ColumnDataSource(data=dict())
        source_orig = ColumnDataSource(data=df)

        def update(attr, old, new):
            global highlighed_idx
            subset = df.iloc[new]
            highlighed_idx = new
            subset = subset.iloc[np.random.permutation(len(subset))]
            source.data = subset

        def save():
            global highlighed_idx
            df.iloc[highlighed_idx][['text']].to_csv(text_filename.value)

        columns = [
            TableColumn(field="text", title="text")
        ]

        data_table = DataTable(source=source, columns=columns, width=800)
        source.data = df

        p = figure(title="", sizing_mode="scale_both", tools="lasso_select")
        scatter = p.circle(x="x", y="y", size=1, source=source_orig)
        p.plot_width = 300
        p.plot_height = 300

        scatter.data_source.selected.on_change('indices', update)

        text_filename = TextInput(value="out.csv", title="Filename:")
        save_btn = Button(label="SAVE")
        save_btn.on_click(save)

        controls = column(p, text_filename, save_btn)
        return doc.add_root(
            row(controls, data_table)
        )

    return bkapp
