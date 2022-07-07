import numpy as np
import pandas as pd
from bokeh.layouts import column, row
from bokeh.models import Button, ColumnDataSource, TextInput, DataTable, TableColumn, ColorBar, HTMLTemplateFormatter, Spinner, RangeSlider
from bokeh.plotting import figure
from bokeh.palettes import Spectral6

from .utils import get_color_mapping

def path_to_image_html(path):
    template = '<img src="'+ path + '" width="60">'
    return HTMLTemplateFormatter(template=template)

def determine_keyword(text, keywords):
    for kw in keywords:
        if kw in text:
            return kw
    return "none"

def bulk_images(path, keywords=None):
    def bkapp(doc):
        df = pd.read_csv(path)
        df['alpha'] = 0.5
        if keywords:
            df['color'] = [determine_keyword(str(t), keywords) for t in df['text']]
            df['alpha'] = [0.4 if c == 'none' else 1 for c in df['color']]

        highlighted_idx = []

        mapper, df = get_color_mapping(df)
        columns = [
            TableColumn(field="image", title="images", formatter=HTMLTemplateFormatter(template='<img src="<%= image %>" width=60>'))
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
            global highlighted_idx
            df.iloc[highlighted_idx][['text']].to_csv(text_filename.value, index=False)

        source = ColumnDataSource(data=dict())
        source_orig = ColumnDataSource(data=df)

        data_table = DataTable(source=source, columns=columns, row_height=100, width=500 if "color" in df.columns else 500)
        source.data = df

        p = figure(title="", sizing_mode="scale_both", tools=["lasso_select", "box_select", "pan", "box_zoom", "wheel_zoom", "reset"])
        p.toolbar.active_drag = None
        p.toolbar.active_inspect = None

        circle_kwargs = {"x": "x", "y": "y", "size": 1, "source": source_orig, "alpha": "alpha"}
        if "color" in df.columns:
            circle_kwargs.update({"color": mapper})
            color_bar = ColorBar(color_mapper=mapper['transform'], width=8)
            p.add_layout(color_bar, 'right')

        scatter = p.circle(**circle_kwargs)
        p.plot_width = 500
        if "color" in df.columns:
            p.plot_width=350
        p.plot_height = 500

        ## Spinner for Node Size
        spinner = Spinner(title="Circle Size", low = 1, high=60, step=1, value=scatter.glyph.size, width=200)
        spinner.js_link("value", scatter.glyph, "size")

        ## Adjust Row Height
        row_spinner = Spinner(title="Row Height", low = 100, high=1000, step=10, value=data_table.row_height, width=200)
        row_spinner.js_link("value", data_table, "row_height")

        scatter.data_source.selected.on_change('indices', update)

        text_filename = TextInput(value="out.csv", title="Filename:")
        save_btn = Button(label="SAVE")
        save_btn.on_click(save)

        controls_main = column(spinner, p, text_filename, save_btn)
        controls = column(row_spinner, data_table)
        return doc.add_root(
            row(controls_main, controls)
        )

    return bkapp
