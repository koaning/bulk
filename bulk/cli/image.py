import base64
from itertools import zip_longest

import numpy as np
import pandas as pd
from bokeh.layouts import column, row
from bokeh.models import (Button, ColorBar, ColumnDataSource, CustomJS,
                          DataTable, HTMLTemplateFormatter, TableColumn,
                          TextInput)
from bokeh.plotting import figure
from wasabi import msg

from bulk._bokeh_utils import download_js_code, read_file, save_file


def grouper(iterable, n, *, incomplete="fill", fillvalue=None):
    "Collect data into non-overlapping fixed-length chunks or blocks"
    args = [iter(iterable)] * n
    if incomplete == "fill":
        return zip_longest(*args, fillvalue=fillvalue)
    if incomplete == "strict":
        return zip(*args, strict=True)
    if incomplete == "ignore":
        return zip(*args)
    else:
        raise ValueError("Expected fill, strict, or ignore")


def bulk_images(path, download=False, keywords=None):
    def bkapp(doc):
        df, colormap, orig_cols = read_file(path, keywords=keywords)
        if "path" not in df.columns:
            msg.fail(
                "Received a datafile that does not have a `path` column. This is a requirement.",
                exits=True,
            )
        highlighted_idx = []

        columns = [
            TableColumn(
                field="image0",
                title="",
                formatter=HTMLTemplateFormatter(template="<%=image0%>"),
            ),
            TableColumn(
                field="image1",
                title="",
                formatter=HTMLTemplateFormatter(template="<%=image1%>"),
            ),
            TableColumn(
                field="image2",
                title="",
                formatter=HTMLTemplateFormatter(template="<%=image2%>"),
            ),
            TableColumn(
                field="image3",
                title="",
                formatter=HTMLTemplateFormatter(template="<%=image3%>"),
            ),
            TableColumn(
                field="image4",
                title="",
                formatter=HTMLTemplateFormatter(template="<%=image4%>"),
            ),
        ]

        def update(attr, old, new):
            """Callback used for plot update when lasso selecting"""
            global highlighted_idx
            subset = df.iloc[new]
            highlighted_idx = new
            subset = subset.iloc[np.random.permutation(len(subset))]
            groups = grouper(subset["image"], n=5, incomplete="ignore")
            new_view = pd.DataFrame(groups, columns=[f"image{i}" for i in "01234"])
            source.data = new_view

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
            source=source,
            columns=columns,
            row_height=100,
            width=750 if "color" in df.columns else 800,
        )
        source.data = df

        p = figure(
            title="",
            sizing_mode="scale_both",
            tools="lasso_select,box_select,pan,box_zoom,wheel_zoom,reset",
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
            print(download_js_code())
            save_btn.js_on_click(
                CustomJS(args=dict(source=source_orig), code=download_js_code())
            )
        else:
            save_btn.on_click(save)

        controls = column(p, text_filename, save_btn)
        return doc.add_root(row(controls, data_table))

    return bkapp
