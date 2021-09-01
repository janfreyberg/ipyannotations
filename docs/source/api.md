# API documentation

```{contents}
:local:
```

## Image submodule

### Classification

```{eval-rst}
.. autoclass:: ipyannotations.images.ClassLabeller
    :members: display, data, on_submit, submit, on_undo, undo, skip, clear

.. autoclass:: ipyannotations.images.MulticlassLabeller
    :members: display, data, on_submit, submit, on_undo, undo, skip, clear
```

### Landmarks, polygons, and bounding boxes

```{eval-rst}
.. autoclass:: ipyannotations.images.PolygonAnnotator
    :members: display, data, on_submit, submit, on_undo, undo, skip, clear

.. autoclass:: ipyannotations.images.PointAnnotator
    :members: display, data, on_submit, submit, on_undo, undo, skip, clear

.. autoclass:: ipyannotations.images.BoxAnnotator
    :members: display, data, on_submit, submit, on_undo, undo, skip, clear

```

### Captions

```{eval-rst}
.. autoclass:: ipyannotations.images.FreetextAnnotator
    :members: display, data, on_submit, submit, on_undo, undo, skip, clear
```

## Text submodule

### Classification

```{eval-rst}
.. autoclass:: ipyannotations.text.ClassLabeller
    :members: display, data, on_submit, submit, on_undo, undo, skip, clear

.. autoclass:: ipyannotations.text.MulticlassLabeller
    :members: display, data, on_submit, submit, on_undo, undo, skip, clear

.. autoclass:: ipyannotations.text.SentimentLabeller
    :members: display, data, on_submit, submit, on_undo, undo, skip, clear

```

### Entity tagging

```{eval-rst}
.. autoclass:: ipyannotations.text.TextTagger
    :members: display, data, on_submit, submit, on_undo, undo, skip, clear
```

### Captioning

```{eval-rst}
.. autoclass:: ipyannotations.text.FreetextAnnotator
    :members: display, data, on_submit, submit, on_undo, undo, skip, clear
```


## Generic widgets

```{eval-rst}
.. autoclass:: ipyannotations.generic.ClassLabeller
    :members: display, data, on_submit, submit, on_undo, undo, skip, clear

.. autoclass:: ipyannotations.generic.MulticlassLabeller
    :members: display, data, on_submit, submit, on_undo, undo, skip, clear

.. autoclass:: ipyannotations.generic.FreetextAnnotator
    :members: display, data, on_submit, submit, on_undo, undo, skip, clear
```
