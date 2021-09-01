(classification)=

```{hint}
This page is only partially interactive. Since this is a static HTML page, only
front-end interactivity works. This means you can click buttons, but the
relevant python-level responses to those actions won't occur.
```

# Classifying images, text, and arbitrary input

Classification is a standard task in data labelling, and ipyannotations has
support for varying input types.

All classification widgets share some parameters and arguments, such as:

- `options`: the classes you're assigning
- `allow_freetext`: whether to allow free text entry of new class labels
- `max_buttons`: depending on the labelling job, it may get too unwieldy to
  have every option as a button. Setting this allows the widget to switch to a
  different method of class selection.


## Image classification

This is a standard task in machine learning, and the data required for these
tasks can be generated quickly with ipyannotations.

```python
import ipyannotations.images

widget = ipyannotations.images.ClassLabeller(
    options=['baboon', 'orangutan'], allow_freetext=True)
widget.display('source/img/baboon.png')
widget
```

```{jupyter-execute}
:hide-code:
import os
import ipyannotations.images
from ipyannotations._doc_utils import recursively_remove_from_dom, get_asset_path

widget = ipyannotations.images.ClassLabeller(options=['baboon', 'orangutan'])
widget.display(get_asset_path('img/baboon.png'))
recursively_remove_from_dom(widget)
```


## Text classification

The text classification widget works much the same way. Imagine you want to
classify things as spam or not spam:

```python
import ipyannotations.text

widget = ipyannotations.text.ClassLabeller(
    options=['spam', 'not spam'], allow_freetext=False)
widget.display(
    "Greetings! Your esteemed research would be suitable "
    "for publication in our scientific journal.")
widget
```

```{jupyter-execute}
:hide-code:
import ipyannotations.text

widget = ipyannotations.text.ClassLabeller(
    options=['spam', 'not spam'], allow_freetext=False)
widget.display(
    "Greetings! Your esteemed research would be suitable "
    "for publication in our scientific journal.")
recursively_remove_from_dom(widget)
```

<br/>

There is also a special classification widget for sentiment in the text module:

```python
import ipyannotations.text

widget = ipyannotations.text.SentimentLabeller()
widget.display("You look nice today.")
widget
```

```{jupyter-execute}
:hide-code:
import ipyannotations.text

widget = ipyannotations.text.SentimentLabeller()
widget.display("You look nice today.")
recursively_remove_from_dom(widget)
```


## Multiple class labels (multiclass)

You can also assign multiple classes to a data point, with the
`MulticlassLabeller`. It exists for both images and text, and allows the user
to toggle multiple classes, then click `submit` (or hit `Enter`):

```python
import ipyannotations.images

widget = ipyannotations.images.MulticlassLabeller(
    options=['baboon', 'mammal', 'toucan', 'bird'], allow_freetext=True)
widget.display('source/img/baboon.png')
widget
```

```{jupyter-execute}
:hide-code:
import ipyannotations.images
from ipyannotations._doc_utils import recursively_remove_from_dom, get_asset_path

widget = ipyannotations.images.MulticlassLabeller(
    options=['baboon', 'mammal', 'toucan', 'bird'], allow_freetext=True)
widget.display(get_asset_path('img/baboon.png'))
recursively_remove_from_dom(widget)
```

## Arbitrary data with self-written display functions

In addition to the image and text widgets, you can build a custom
classification widget by using the widgets from the `ipyannotations.generic`
submodule. (In fact, the image and text widgets are just wrappers around this).

The display function for these widgets can be anything that displays output in
a jupyter notebook.

For example, if you wanted to classify graphs of points into periodic and
non-periodic:

```python
import ipyannotations.generic
import numpy as np
import matplotlib.pyplot as plt

plt.ioff() # turn off default inline plotting

def plotting_function(data):
    fig, ax = plt.subplots(1, 1)
    ax.plot(data)
    display(fig)

widget = ipyannotations.generic.ClassLabeller(
    options=['periodic', 'non-periodic'], allow_freetext=False,
    display_function=plotting_function)
widget.display(np.random.rand(100))
widget
```

```{jupyter-execute}
:hide-code:
import ipyannotations.generic
import numpy as np
import matplotlib.pyplot as plt

plt.ioff() # turn off default inline plotting

def plotting_function(data):
    fig, ax = plt.subplots(1, 1)
    ax.plot(data)
    display(fig)

widget = ipyannotations.generic.ClassLabeller(
    options=['periodic', 'non-periodic'], allow_freetext=False,
    display_function=plotting_function)
widget.display(np.random.rand(100))
recursively_remove_from_dom(widget)
```
