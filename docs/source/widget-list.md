# Full widget list

```{contents}
:local:
```

## Image widgets

### {class}`ipyannotations.images.ClassLabeller`

```python
import ipyannotations.images

widget = ipyannotations.images.ClassLabeller(
    options=['baboon', 'orangutan'],
    max_buttons=12,
    allow_freetext=True,
)
widget.display('source/img/baboon.png')
widget
```

```{jupyter-execute}
:hide-code:
import os
import ipyannotations.images
from ipyannotations._doc_utils import recursively_remove_from_dom, get_asset_path

widget = ipyannotations.images.ClassLabeller(
    options=['baboon', 'orangutan'],
    max_buttons=12,
    allow_freetext=True,
)
widget.display(get_asset_path('img/baboon.png'))
recursively_remove_from_dom(widget)
```

### {class}`ipyannotations.images.MulticlassLabeller`

```python
import ipyannotations.images

widget = ipyannotations.images.MulticlassLabeller(
    options=['baboon', 'mammal', 'toucan', 'bird'],
    max_buttons=12,
    allow_freetext=True,
)
widget.display('source/img/baboon.png')
widget
```

```{jupyter-execute}
:hide-code:
import ipyannotations.images
from ipyannotations._doc_utils import recursively_remove_from_dom, get_asset_path

widget = ipyannotations.images.MulticlassLabeller(
    options=['baboon', 'mammal', 'toucan', 'bird'],
    max_buttons=12,
    allow_freetext=True,
)
widget.display(get_asset_path('img/baboon.png'))
recursively_remove_from_dom(widget)
```


### {class}`ipyannotations.images.PolygonAnnotator`

```python
from ipyannotations import images
widget = images.PolygonAnnotator(
    options=["eye", "mouth"],
    canvas_size=(700, 500)
)
widget.display("img/baboon.png")
widget
```

```{jupyter-execute}
:hide-code:
from ipyannotations._doc_utils import recursively_remove_from_dom, patch_canvas, get_asset_path
from ipyannotations import images
widget = images.PolygonAnnotator(options=["eye", "mouth"])
widget.display(get_asset_path("img/baboon.png"))
widget = patch_canvas(widget, get_asset_path("img/baboon-polygons.png"))
recursively_remove_from_dom(widget)
```
---

### {class}`ipyannotations.images.PointAnnotator`

```python
from ipyannotations import images
widget = images.PointAnnotator(
    options=["pigeon"],
    canvas_size=(700, 500)
)
widget.display("img/vdnkh.jpg")
widget
```

```{jupyter-execute}
:hide-code:
from ipyannotations._doc_utils import recursively_remove_from_dom, patch_canvas, get_asset_path
from ipyannotations import images
widget = images.PointAnnotator(options=["pigeon"])
widget.display(get_asset_path("img/vdnkh.jpg"))
patch_canvas(widget, get_asset_path('img/vdnkh-annotated.png'))
recursively_remove_from_dom(widget)
```

### {class}`ipyannotations.images.BoxAnnotator`

```python
from ipyannotations import images
widget = images.BoxAnnotator(
    options=["eye", "mouth", "nose", "cheek"],
    canvas_size=(700, 500)
)
widget.display("img/baboon.png")
widget
```

```{jupyter-execute}
:hide-code:
from ipyannotations._doc_utils import recursively_remove_from_dom, patch_canvas, get_asset_path
from ipyannotations import images
widget = images.BoxAnnotator(
    options=["eye", "mouth", "nose", "cheek"],
    canvas_size=(700, 500)
)
widget.display(get_asset_path("img/baboon.png"))
patch_canvas(widget, get_asset_path('img/baboon-boxes.png'))
recursively_remove_from_dom(widget)
```

### {class}`ipyannotations.images.FreetextAnnotator`

```python
from ipyannotations.images import FreetextAnnotator
widget = FreetextAnnotator(
    textbox_placeholder="Please caption this image and press Shift+Enter to submit.",
    num_textbox_rows=5,
)
widget.display('img/vdnkh.jpg')
widget
```

```{jupyter-execute}
:hide-code:
from ipyannotations._doc_utils import recursively_remove_from_dom, patch_canvas, get_asset_path
from ipyannotations.images import FreetextAnnotator
widget = FreetextAnnotator(
    textbox_placeholder="Please caption this image and press Shift+Enter to submit.",
    num_textbox_rows=5,
)
widget.display(get_asset_path('img/vdnkh.jpg'))
recursively_remove_from_dom(widget)
```


## Text widgets

### {class}`ipyannotations.text.ClassLabeller`

```python
import ipyannotations.text

widget = ipyannotations.text.ClassLabeller(
    options=['spam', 'not spam'],
    max_buttons=12,
    allow_freetext=True,
)
widget.display(
    "Greetings! Your esteemed research would be suitable "
    "for publication in our scientific journal.")
widget
```

```{jupyter-execute}
:hide-code:
from ipyannotations._doc_utils import recursively_remove_from_dom, get_asset_path
import ipyannotations.text

widget = ipyannotations.text.ClassLabeller(
    options=['spam', 'not spam'], allow_freetext=False)
widget.display(
    "Greetings! Your esteemed research would be suitable "
    "for publication in our scientific journal.")
recursively_remove_from_dom(widget)
```

### {class}`ipyannotations.text.MulticlassLabeller`

```python
import ipyannotations.text

widget = ipyannotations.text.MulticlassLabeller(
    options=['spam', 'academia', 'not spam', 'industry'],
    max_buttons=12,
    allow_freetext=True,
)
widget.display(
    "Greetings! Your esteemed research would be suitable "
    "for publication in our scientific journal.")
widget
```

```{jupyter-execute}
:hide-code:
from ipyannotations._doc_utils import recursively_remove_from_dom, get_asset_path
import ipyannotations.text

widget = ipyannotations.text.MulticlassLabeller(
    options=['spam', 'academia', 'not spam', 'industry'],
    max_buttons=12,
    allow_freetext=True,
)
widget.display(
    "Greetings! Your esteemed research would be suitable "
    "for publication in our scientific journal.")
recursively_remove_from_dom(widget)
```

### {class}`ipyannotations.text.SentimentLabeller`

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

### {class}`ipyannotations.text.TextTagger`

```python
import ipyannotations.text

widget = ipyannotations.text.TextTagger(
    classes=["MISC", "PER", "LOC", "ORG"],
    button_width="5em",
    snap_to_word_boundary=True,
)
widget.display("This is an *example sentence*. Try highlighting a word.")
widget
```

```{jupyter-execute}
:hide-code:

import ipyannotations.text
from ipyannotations._doc_utils import recursively_remove_from_dom


widget = ipyannotations.text.TextTagger(
    classes=["MISC", "PER", "LOC", "ORG"],
    button_width="5em",
    snap_to_word_boundary=True,
)
widget.display("This is an example sentence. Try highlighting a word.")
recursively_remove_from_dom(widget)
```


## Generic widgets

### {class}`ipyannotations.generic.ClassLabeller`

```python
import ipyannotations.generic
import IPython.display

widget = ipyannotations.generic.ClassLabeller(
    options=['a', 'b'],
    allow_freetext=True,
    display_function=IPython.display.display,
)
widget.display('This could be arbitrary data.')
widget
```

```{jupyter-execute}
:hide-code:

from ipyannotations._doc_utils import recursively_remove_from_dom, get_asset_path
import ipyannotations.generic
import IPython.display

widget = ipyannotations.generic.ClassLabeller(
    options=['a', 'b'],
    allow_freetext=True,
    display_function=IPython.display.display,
)
widget.display('This could be arbitrary data.')
recursively_remove_from_dom(widget)
```

### {class}`ipyannotations.generic.MulticlassLabeller`

```python
import ipyannotations.generic
import IPython.display

widget = ipyannotations.generic.MulticlassLabeller(
    options=['a', 'b'],
    allow_freetext=True,
    display_function=IPython.display.display,
)
widget.display('This could be arbitrary data.')
widget
```

```{jupyter-execute}
:hide-code:

from ipyannotations._doc_utils import recursively_remove_from_dom, get_asset_path
import ipyannotations.generic
import IPython.display

widget = ipyannotations.generic.MulticlassLabeller(
    options=['a', 'b'],
    allow_freetext=True,
    display_function=IPython.display.display,
)
widget.display('This could be arbitrary data.')
recursively_remove_from_dom(widget)
```

### {class}`ipyannotations.generic.FreetextAnnotator`

```python
import ipyannotations.generic
import IPython.display

widget = ipyannotations.generic.FreetextAnnotator(
    textbox_placeholder="Type a response and press Shift+Enter to submit.",
    num_textbox_rows=5,
    display_function=IPython.display.display,
)
widget.display('This could be arbitrary data.')
widget
```

```{jupyter-execute}
:hide-code:

from ipyannotations._doc_utils import recursively_remove_from_dom, get_asset_path
import ipyannotations.generic
import IPython.display

widget = ipyannotations.generic.FreetextAnnotator(
    textbox_placeholder="Type a response and press Shift+Enter to submit.",
    num_textbox_rows=5,
    display_function=IPython.display.display,
)
widget.display('This could be arbitrary data.')
recursively_remove_from_dom(widget)
```
