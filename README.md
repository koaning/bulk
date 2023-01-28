<img src="lasso.svg" align="right" >

# bulk

Bulk is a quick developer tool to apply some bulk labels. Given a prepared dataset with 2d embeddings it can generate an interface that allows you to quickly add some bulk, albeit less precice, annotations.

https://user-images.githubusercontent.com/1019791/215258797-080dec5b-daf4-4d5c-843e-31088abff557.mp4

## Features 

Bulk gives you annotation interfaces based on UMAP representations of embeddings. It offers an interface for text. 

![](images/bulk-text.png)

But it also features an image interface. 

![](images/bulk-image.png)

## Learn

If you're curious to learn more, you may appreciated [this video on YouTube](https://www.youtube.com/watch?v=gDk7_f3ovIk&ab_channel=Explosion) for text and [this video on YouTube](https://youtu.be/DmH3JmX3w2I) for computer vision.

## Install 

```
python -m pip install --upgrade pip
python -m pip install bulk
```

## Bulk Text 

To use bulk for text, you'll first need to prepare a csv file first.

> **Note**
>
> The example below uses [embetter](https://github.com/koaning/embetter) to generate the embeddings and [umap](https://umap-learn.readthedocs.io/) to reduce the dimensions. But you're  totally free to use what-ever text embedding tool that you like. You will need to install these tools seperately. Note that embetter uses  [sentence-transformers](https://www.sbert.net/) under the hood.

```python
import pandas as pd
from umap import UMAP
from sklearn.pipeline import make_pipeline 
from sklearn.linear_model import LogisticRegression


# pip install "embetter[text]"
from embetter.text import SentenceEncoder

# Build a sentence encoder pipeline with UMAP at the end.
text_emb_pipeline = make_pipeline(
  SentenceEncoder('all-MiniLM-L6-v2'),
  UMAP()
)

# Load sentences
sentences = list(pd.read_csv("original.csv")['sentences'])

# Calculate embeddings 
X_tfm = text_emb_pipeline.fit_transform(sentences)

# Write to disk. Note! Text column must be named "text"
df = pd.DataFrame({"text": sentences})
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

### Extra Settings

You can also pass an extra column to your csv file called "color". This column will then be used to color the points in the interface. 

You can also pass `--keywords` to the command line app to highlight elements that contain specific keywords.

```
python -m bulk text ready.csv --keywords "deliver,card,website,compliment"
```

## Bulk Image

The example below uses the `embetter` library to create a dataset for bulk labelling images. 

> **Note**
>
> The example below uses [embetter](https://github.com/koaning/embetter) to generate the embeddings and [umap](https://umap-learn.readthedocs.io/) to reduce the dimensions. But you're  totally free to use what-ever text embedding tool that you like. You will need to install these tools seperately. Note that embetter uses [TIMM](https://github.com/rwightman/pytorch-image-models) under the hood.

```python
import pathlib
import pandas as pd
from sklearn.pipeline import make_pipeline 
from umap import UMAP
from sklearn.preprocessing import MinMaxScaler

# pip install "embetter[vision]"
from embetter.grab import ColumnGrabber
from embetter.vision import ImageLoader, TimmEncoder

# Build image encoding pipeline
image_emb_pipeline = make_pipeline(
    ColumnGrabber("path"),
    ImageLoader(convert="RGB"),
    TimmEncoder('xception'),
    UMAP(),
    MinMaxScaler()
)

# Make dataframe with image paths
img_paths = list(pathlib.Path("downloads", "pets").glob("*"))
dataf = pd.DataFrame({
    "path": [str(p) for p in img_paths]
})

# Make csv file with Umap'ed model layer 
# Note! Bulk assumes the image path column to be called "path"!
X = image_emb_pipeline.fit_transform(dataf)
dataf['x'] = X[:, 0]
dataf['y'] = X[:, 1]
dataf.to_csv(f"pets-xception.csv", index=False)
```

This generates a csv file that can be loaded in bulk via; 

```
python -m bulk image ready.csv
```

## Download 

You can also use bulk to download some datasets to play with. For more info:

```
python -m bulk download --help
```

## Usecase 

The interface may help you label very quickly, but the labels themselves may be faily noisy. The intended use-case for this tool is to prepare interesting subsets to be used later in [prodi.gy](https://prodi.gy). 
