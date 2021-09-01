# ipyannotations

Create rich adata annotations in jupyter notebooks.

## Quickstart

To get started with ipyannotations, install with pip:

```
pip install ipyannotations
```

To start labelling data, import from the appropriate ipyannotations module. For
example, for text span/entity labelling:

```python
from ipyannotations import text
widget = text.TextTagger()
widget.display("This is a text tagging widget. Highlight words "
               "or phrases to tag them with a class.")
widget
```

```{jupyter-execute}
:hide-code:

from ipyannotations import text
widget = text.TextTagger()
widget.display("This is a text tagging widget. Highlight words "
               "or phrases to tag them with a class.")
from ipyannotations._doc_utils import recursively_remove_from_dom
widget = recursively_remove_from_dom(widget)
widget
```

Or, if you would like to classify images:

```python
from ipyannotations import images
widget = images.ClassLabeller(options=["monkey", "ape"])
widget.display("img/baboon.png")
widget
```

```{jupyter-execute}
:hide-code:

from ipyannotations._doc_utils import recursively_remove_from_dom, get_asset_path
from ipyannotations import images
widget = images.ClassLabeller(options=["monkey", "ape"])
widget.display(get_asset_path("img/baboon.png"))
widget = recursively_remove_from_dom(widget)
widget
```

<br/>

```{note}
Throughout this documentation, UI elements can be interacted with (e.g.
buttons can be clicked, sliders can be moved), but because there is no
python process running in the background, the effect will mostly not be
visible.
```

```{toctree}
:caption: Contents
:maxdepth: 2

installing
introduction
examples/index
widget-list
api
```

```{toctree}
:caption: Development
:maxdepth: 2

develop-install
```

% links

[jupyter widgets]: https://jupyter.org/widgets.html
[notebook]: https://jupyter-notebook.readthedocs.io/en/latest/
