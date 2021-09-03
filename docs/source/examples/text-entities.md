```{hint}
This page is only partially interactive. Since this is a static HTML page, only
front-end interactivity works. This means you can click buttons and highlight
text, but the relevant python-level responses to those actions won't occur.
```

# Text entity annotation

A common task in natural language processing is to extract entities of interest
from some text. This may be as simple as extracting the main content of interest
from some text that often comes with boilerplate, or involve identifying e.g.
place names or personal names.

To do this, ipyannotations has a widget called `ipyannotations.text.TextTagger`,
which allows you to highlight words, phrases or sentences and assign a class to
them.

The widget will display any string, including Markdown-formatted text.

```python
import ipyannotations.text
from ipyannotations._doc_utils import recursively_remove_from_dom


widget = ipyannotations.text.TextTagger()
widget.display("This is an *example sentence*. Try highlighting a word.")
widget
```

```{jupyter-execute}
:hide-code:

import ipyannotations.text
from ipyannotations._doc_utils import recursively_remove_from_dom


widget = ipyannotations.text.TextTagger()
widget.display("This is an example sentence. Try highlighting a word.")
recursively_remove_from_dom(widget)
```

The default entity types are `PER` (person), `ORG` (organisation), `LOC`
(location), and `MISC` (miscellaneous). These are chosen because they are
relatively standard in the Named Entity Recognition research community.

You can choose which entity type you are tagging at any point by toggling its
button, or using the hotkeys 1 – 0, mapped in order.

To set the classes you are interested in, you can pass them to the widget using
the `classes` argument:

```python
import ipyannotations.text

widget = ipyannotations.text.TextTagger(classes=["Insult", "Compliment"])
widget.display("You are annoying, but I like you.")
widget
```

```{jupyter-execute}
:hide-code:

import ipyannotations.text
from ipyannotations._doc_utils import recursively_remove_from_dom

widget = ipyannotations.text.TextTagger(classes=["Insult", "Compliment"])
widget.display("You are annoying, but I like you.")
widget.data = [(8, 16, 'Insult'), (22, 32, 'Compliment')]
recursively_remove_from_dom(widget)
```

The widget will snap to word boundaries by default. This means you can
double-click on a word to tag it, hopefully making tagging faster. If you need
to label entities at the character level, you can set `snap_to_word_boundary` to
False:

```python
import ipyannotations.text

widget = ipyannotations.text.TextTagger(
    classes=["Insult", "Compliment"],
    snap_to_word_boundary=False
)
widget.display("You are annoying, but I like you.")
widget
```

```{jupyter-execute}
:hide-code:

import ipyannotations.text
from ipyannotations._doc_utils import recursively_remove_from_dom

widget = ipyannotations.text.TextTagger(
    classes=["Insult", "Compliment"],
    snap_to_word_boundary=False,
)
widget.display("You are annoying, but I like you.")
widget.data = [(8, 16, 'Insult'), (22, 32, 'Compliment')]
recursively_remove_from_dom(widget)
```

The format for the annotations takes the form of a three-tuple with types (int,
int, str). The integers indicate the starting and ending character of the
selected span, and the string indicates the class name.

```python
widget.data
```

```{jupyter-execute}
:hide-code:

widget.data
```
