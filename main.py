''' A column salary chart with minimum and maximum values.
This example shows the capability of exporting a csv file from ColumnDataSource.

'''
from os.path import dirname, join

import pandas as pd

from bokeh.io import curdoc
from bokeh.layouts import column, row
from bokeh.models import (Button, ColumnDataSource, CustomJS, DataTable,
                          NumberFormatter, RangeSlider, TableColumn)
from bokeh.layouts import gridplot
from bokeh.plotting import figure
from bokeh.models import DataTable, TableColumn

df = pd.read_csv(join(dirname(__file__), 'cluestarred.csv'))

source = ColumnDataSource(data=dict())
source_orig = ColumnDataSource(data=df)

def update(attr, old, new):
    # print(attr)
    # print(old)
    # print(new)
    source.data = df.iloc[new]

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
controls = column(p)

curdoc().add_root(row(controls, data_table))

# update()