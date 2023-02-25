import numpy as np
import pandas as pd
from bokeh.layouts import column, row
from bokeh.models import (Button, ColorBar, ColumnDataSource, CustomJS,
                          DataTable, TableColumn, TextInput)
from bokeh.plotting import figure
from wasabi import msg

from bulk._bokeh_utils import download_js_code, read_file, save_file


def bulk_text(path, keywords=None, download=True):
    def bkapp(doc):
        df, colormap, orig_cols = read_file(path, keywords=keywords)
        if "text" not in df.columns:
            msg.fail(
                "Received a datafile that does not have a `text` column. This is a requirement.",
                exits=True,
            )

        highlighted_idx = []

        columns = [TableColumn(field="text", title="text")]

        def update(attr, old, new):
            """Callback used for plot update when lasso selecting"""
            global highlighted_idx
            subset = df.iloc[new]
            highlighted_idx = new
            subset = subset.iloc[np.random.permutation(len(subset))]
            source.data = subset

        def save():
            """Callback used to save highlighted data points"""
            global highlighted_idx
            save_file(
                dataf=df,
                highlighted_idx=highlighted_idx,
                filename=text_filename.value,
                orig_cols=orig_cols,
            )

        source = ColumnDataSource(data=dict())
        source_orig = ColumnDataSource(data=df)

        data_table = DataTable(
            source=source, columns=columns, width=750 if "color" in df.columns else 800
        )
        source.data = df

        p = figure(
            title="",
            sizing_mode="scale_both",
            tools=[
                "lasso_select",
                "box_select",
                "pan",
                "box_zoom",
                "wheel_zoom",
                "reset",
            ],
            active_drag="box_select",
        )

        circle_kwargs = {
            "x": "x",
            "y": "y",
            "size": 1,
            "source": source_orig,
            "alpha": "alpha",
        }
        if "color" in df.columns:
            circle_kwargs.update({"color": colormap})
            color_bar = ColorBar(color_mapper=colormap["transform"], width=8)
            p.add_layout(color_bar, "right")

        scatter = p.circle(**circle_kwargs)
        p.plot_width = 300
        if "color" in df.columns:
            p.plot_width = 350
        p.plot_height = 300

        scatter.data_source.selected.on_change("indices", update)

        text_filename = TextInput(
            value="out.jsonl" if download else "out.csv",
            title="Filename:",
            name="filename",
        )
        save_btn = Button(label="DOWNLOAD" if download else "SAVE")
        if download:
            save_btn.js_on_click(
                CustomJS(args=dict(source=source), code=download_js_code())
            )
        else:
            save_btn.on_click(save)

        controls = column(p, text_filename, save_btn)
        return doc.add_root(row(controls, data_table))

    return bkapp
