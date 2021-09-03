# Introduction

This library is designed to give python developers an easy way of building a
dataset and collecting annotations.

It is built on ipywidgets, and all of the interfaces work in Jupyter notebooks
and Jupyter Lab.

## Why in the notebook?

The jupyter notebook interface is very widespread, and many developers -
especially those working with data, such as scientists - are familiar with it.

Additionally, many libraries actually provide great representations of their
data structures in the notebook. For example, the
[shapely](https://shapely.readthedocs.io/en/latest/) library displays its shape
objects as images natively in the notebook. Building a data annotation tool
around jupyter notebooks means much of this rich ecosystem can be used to
annotate data with ipywidgets.

Additionaly, recent developments in the ecosystem make jupyter notebooks a
viable way of deploying interactive web pages: the
[voila](https://voila.readthedocs.io/en/latest/?badge=latest) web server allows
you to display a notebook as a stand-alone website.

## Basics

ipyannotations implements data labelling widgets with a common protocol:

- all widgets implement a `display` method, which accepts a data point to be
  labelled
- all widgets store the current label or annotation in the `data` attribute
- all widgets have a `submit` method, which in triggers callbacks registered by
  the user
- all widgets have a `skip` method, which submits `None`
- all widgets implement an `undo` function, which triggers callbacks registered
  by the user

The intended workflow is therefore to do the following for each data point to
be labelled or annotated:

1. Call `display` on the data point, which clears the previous annotation and
   presents the data point to the user
2. Wait for the user to annotate the data point, and submit this annotation in
   the UI, thereby triggering `submit`
3. The submit callback handles the label, e.g. by storing it in a database, and
   calls `display` on the next datapoint to be labelled.

All of the above actions have corresponding UI elements, but these elements
can be different for different widgets. All widgets also respond to hotkeys,
meaning you can submit data using `Enter`, undo an action using `Backspace`,
and in many cases select options from within the widget using the 1-0 keys.

An very simple example of this process might be something like:

```python
import ipyannotations.text

sports_headlines = [
    "Rowan Crothers leads strong Australian showing in the pool",
    "Tokyo 2020 Paralympics briefing: Ukraine and GB swim to glory",
    "Chelsea hold on despite James red for handball on the line! Liverpool 1-1 Chelsea",
    "Root thanks players after becoming England’s most successful Test captain",
    "Andy Murray concerned by low uptake of vaccine among tour pros",
    "Husband and wife Neil and Lora Fachie each win cycling gold at Paralympics",
    "County cricket: Sussex, Hampshire, Somerset and Kent reach Finals Day",
    "European roundup: Juventus lose at home to Empoli, Bayern thrash Hertha",
]
labels = []

widget = ipyannotations.text.TextTagger()

def store_annotations(entity_annotation):
    labels.append(entity_annotation)
    try:
        widget.display(input_queue.pop(0))
    except IndexError:
        print("Finished.")

widget.on_submit(store_annotations)
# start the iterations:
widget.display(input_queue.pop(0))
widget
```

```{jupyter-execute}
:hide-code:
import ipyannotations.text
from ipyannotations._doc_utils import recursively_remove_from_dom


sports_headlines = [
    "Rowan Crothers leads strong Australian showing in the pool",
    "Tokyo 2020 Paralympics briefing: Ukraine and GB swim to glory",
    "Chelsea hold on despite James red for handball on the line! Liverpool 1-1 Chelsea",
    "Root thanks players after becoming England’s most successful Test captain",
    "Andy Murray concerned by low uptake of vaccine among tour pros",
    "Husband and wife Neil and Lora Fachie each win cycling gold at Paralympics",
    "County cricket: Sussex, Hampshire, Somerset and Kent reach Finals Day",
    "European roundup: Juventus lose at home to Empoli, Bayern thrash Hertha",
]
labels = []

widget = ipyannotations.text.TextTagger()

def store_annotations(entity_annotation):
    """The handler for new annotations"""
    labels.append(entity_annotation)
    try:
        widget.display(sports_headlines.pop(0))
    except IndexError:
        print("Finished.")

widget.on_submit(store_annotations) # register the handler
widget.display(sports_headlines.pop(0)) # start the iterations:
recursively_remove_from_dom(widget)
```

However, I would recommend a much more robust label storage system, as well as
a label handler that stops accepting new labels when the input queue is
exhausted.

If you would like to have a library to manage this queue for you, you can take
a look at [superintendent], a library that is specifically designed to work with
ipyannotations. [superintendent] provides the looping over data, data storage
either in memory or in a database, and more.

## Getting started

After following the {ref}`installation` instructions, take a look at the
{ref}`examples` to find a widget that suits your workflow.

## Alternatives

There are plenty of existing labelling tools in python already, and they may
suit your needs more, so you should take a look.

- [Label Studio](https://labelstud.io/) is an application that runs as an
  executable. It is a more full-fledged ecosystem, which also offers paid
  customer support.
- [Prodigy](https://prodi.gy/) is a paid tool that specialises in text
  annotations.
- [ipyannotate](https://github.com/ipyannotate/ipyannotate) is a jupyter widget
  specialised in text annotations

There are various other specialised data labelling tools, as well - if you know
of one that would be useful to list here, please open a PR.

## Contributing

I would appreciate any and all contributions. If you have suggestions for new
widgets, or improved options for existing widgets, please open an issue on
Github for discussion. I would also appreciate any bug reports, bug fixes, etc.

Since I am building a small ecosystem around these labelling tools, I would
also be excited to see new libraries that implement the same protocol as
ipyannotations widgets. This would allow them to interact with [superintendent].

% links

[superintendent]: https://superintendent.readthedocs.io/en/latest/
