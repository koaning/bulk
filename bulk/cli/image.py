import base64
import numpy as np
import pandas as pd
from itertools import zip_longest

from bokeh.plotting import figure
from bokeh.layouts import column, row
from bokeh.models import (
    Button,
    ColumnDataSource,
    TextInput,
    DataTable,
    TableColumn,
    ColorBar,
    HTMLTemplateFormatter,
)

from bulk._bokeh_utils import get_color_mapping


def encode_image(path):
    with open(path, "rb") as image_file:
        enc_str = base64.b64encode(image_file.read()).decode("utf-8")
    return f'<img style="object-fit: scale-down;" width="100%" height="100%" src="data:image/png;base64,{enc_str}">'


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


def bulk_images(path):
    def bkapp(doc):
        df = pd.read_csv(path).assign(
            image=lambda d: [encode_image(p) for p in d["path"]]
        )
        df["alpha"] = 0.5

        highlighted_idx = []

        mapper, df = get_color_mapping(df)
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
            df.iloc[highlighted_idx][["path"]].to_csv(text_filename.value, index=False)

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
            circle_kwargs.update({"color": mapper})
            color_bar = ColorBar(color_mapper=mapper["transform"], width=8)
            p.add_layout(color_bar, "right")

        scatter = p.circle(**circle_kwargs)
        p.plot_width = 300
        if "color" in df.columns:
            p.plot_width = 350
        p.plot_height = 300

        scatter.data_source.selected.on_change("indices", update)

        text_filename = TextInput(value="out.csv", title="Filename:")
        save_btn = Button(label="SAVE")
        save_btn.on_click(save)

        controls = column(p, text_filename, save_btn)
        return doc.add_root(row(controls, data_table))

    return bkapp
