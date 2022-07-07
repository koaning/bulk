<img src="lasso.svg" align="right" >

# bulk-images
This repository adds image support for the bulk library.

![](screenshot-images.png)


## Usage
In the command line, run:
```
python -m bulk images bhl_umap_subsample.csv
```

## To-Do
- [x] add basic support for images
- [ ] have images populate in a grid
- [ ] allow users to control size of plot with sliders
- [ ] allow users to control size of circles with sliders
- [ ] allow users to control size of DataTable (or grid) with sliders

# bulk (initial README)

Bulk is a quick developer tool to apply some bulk labels. Given a prepared dataset with 2d embeddings it can generate an interface that allows you to quickly add some bulk, albeit less precice, annotations.

![](screenshot.png)

# Learn

If you're curious to learn more, you may appreciated [this demo video on YouTube](https://www.youtube.com/watch?v=gDk7_f3ovIk&ab_channel=Explosion).

# Install

```
python -m pip install --upgrade pip
python -m pip install bulk
```

## Usage

To use bulk, you'll first need to prepare a csv file for the lasso widget.

> **Note**
>
> The example below uses [sentence-transformers](https://www.sbert.net/) to generate the embeddings and [umap](https://umap-learn.readthedocs.io/) to reduce the dimensions. But you're  totally free to use what-ever text embedding tool that you like. You will need to install these tools seperately.

```python
import pandas as pd
from umap import UMAP

# pip install -U sentence-transformers
from sentence_transformers import SentenceTransformer

# Load the universal sentence encoder
model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

# Load original dataset
df = pd.read_csv("original.csv")

# Calculate embeddings
X =  model.encode(sentences)

# Reduce the dimensions with UMAP
umap = UMAP()
X_tfm = umap.fit_transform(X)

# Apply coordinates
df['x'] = X_tfm[:, 0]
df['y'] = X_tfm[:, 1]
df.to_csv("ready.csv")
```

You can now use this `ready.csv` file to apply some bulk labelling.

```
python -m bulk text ready.csv
```

If you're looking for an example file to play around with you can download
[the demo .csv file](https://github.com/koaning/bulk/blob/main/cluestarred.csv) in this repository. This dataset
contains a subset of a dataset found on Kaggle. You can find the original [here](https://www.kaggle.com/datasets/thoughtvector/customer-support-on-twitter).

### Extras

You can also pass an extra column to your csv file called "color". This column will then be used to color the points in the interface.

You can also pass `--keywords` to the command line app to highlight elements that contain specific keywords.

```
python -m bulk text ready.csv --keywords "deliver,card,website,compliment"
```

## Usecase

The interface may help you label very quickly, but the labels themselves may be faily noisy. The intended use-case for this tool is to prepare interesting subsets to be used later in [prodi.gy](https://prodi.gy).
