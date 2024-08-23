import jscatter
import numpy as np
import pandas as pd
from IPython.display import display
from ipywidgets import HTML, Button, HBox, Layout, Text, VBox
from sklearn.metrics.pairwise import cosine_similarity


class BaseTextExplorer:
    """
    Interface for basic text exploration in embedded space.
    """

    def __init__(self, dataf, X=None, encoder=None):
        self.dataf = dataf
        self.scatter = jscatter.Scatter(
            data=self.dataf, x="x", y="y", width=500, height=500
        )
        self.html = HTML(
            layout=Layout(width="600px", overflow_y="scroll", height="400px")
        )
        self.sample_btn = Button(description="resample")
        self.elem = HBox([self.scatter.show(), VBox([self.sample_btn, self.html])])
        self.X = X
        self.encoder = encoder

        if self.encoder and (self.X is not None):
            self.text_input = Text(
                value="", placeholder="Type something", description="String:"
            )
            self.elem = HBox(
                [
                    VBox([self.text_input, self.scatter.show()]),
                    VBox([self.sample_btn, self.html]),
                ]
            )

            def update_text(change):
                X_tfm = encoder.transform([self.text_input.value])
                dists = cosine_similarity(X, X_tfm).reshape(1, -1)
                self.dists = dists
                norm_dists = 0.01 + (dists - dists.min()) / (
                    0.1 + dists.max() - dists.min()
                )
                self.scatter.color(by=norm_dists[0])
                self.scatter.size(by=norm_dists[0])

            self.text_input.observe(update_text)

        self.scatter.widget.observe(lambda d: self.update(), ["selection"])
        self.sample_btn.on_click(lambda d: self.update())

    def show(self):
        return self.elem

    def update(self):
        if len(self.scatter.selection()) > 10:
            texts = self.dataf.iloc[self.scatter.selection()].sample(10)["text"]
        else:
            texts = self.dataf.iloc[self.scatter.selection()]["text"]
        self.html.value = "".join([f'<p style="margin: 0px">{t}</p>' for t in texts])

    def observe(self, func):
        self.scatter.widget.observe(func, ["selection"])

    @property
    def selected_idx(self):
        return self.scatter.selection()

    @property
    def selected_texts(self):
        return list(self.dataf.iloc[self.selection_idx]["text"])

    @property
    def selected_dataframe(self):
        return self.dataf.iloc[self.selection_idx]

    def _repr_html_(self):
        return display(self.elem)
