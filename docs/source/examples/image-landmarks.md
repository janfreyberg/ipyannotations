```{hint}
This page is only partially interactive. Since this is a static HTML page, only
front-end interactivity works. This means you can click buttons, but the
relevant python-level responses to those actions won't occur.
```

# Segmenting images, labelling landmarks, and drawing bounding boxes

ipyannotations also supports image annotations. It currently has support for:

- drawing polygons onto images
- annotating points in an image
- drawing bounding boxes on an image

All of the image annotation widgets share some parameters:

- `canvas_size`, the size of the canvas on which the image is drawn, in pixels.
  The format is (width, height), and the default is (700, 500)
- `classes`, the types of objects you'd like to annotate. This should be a list
  of strings. The default is `None`.

All image annotation widgets also share some common UI elements to make
annotating easier, such as brightness / contrast adjustments.

All image annotation widgets also have an "edit mode", which allows adjusting
existing annotations by click-and-dragging any given point. All widgets also
support submitting data using the "Enter" key.

## Drawing polygons around shapes of interest

The `PolygonAnnotator` is designed to draw the outlines of shapes of interest.
This can be useful when you are interested in identifying exactly where an
object is in an image, i.e. if you are training an image segmentation model.

```python
from ipyannotations.images import PolygonAnnotator

widget = PolygonAnnotator(options=["eye", "mouth"])
widget.display("img/baboon.png")

widget
```

```{jupyter-execute}
:hide-code:

from ipyannotations.images import PolygonAnnotator
from ipyannotations._doc_utils import recursively_remove_from_dom, patch_canvas, get_asset_path

widget = PolygonAnnotator(options=["eye", "mouth"])
widget.display(get_asset_path("img/baboon.png"))

widget.opacity_slider.value = 0.75

widget.data = [
    {'type': 'polygon', 'label': 'eye', 'points': [
        (widget.canvas.canvas_to_image_coordinates(p)[0] + 100,
         widget.canvas.canvas_to_image_coordinates(p)[1]) for p in
        [(147, 46), (147, 72), (171, 72), (191, 66), (192, 50), (147, 46)]
    ]},
    {'type': 'polygon', 'label': 'eye', 'points': [
        (widget.canvas.canvas_to_image_coordinates(p)[0] + 100,
         widget.canvas.canvas_to_image_coordinates(p)[1]) for p in
        [(308, 45), (303, 58), (313, 68), (332, 72), (350, 63), (350, 54), (348, 44), (329, 39), (308, 45)]
    ]},
    {'type': 'polygon', 'label': 'nose', 'points': [
        (widget.canvas.canvas_to_image_coordinates(p)[0] + 100,
         widget.canvas.canvas_to_image_coordinates(p)[1]) for p in
        [(211, 121), (206, 231), (214, 286), (163, 340), (154, 383), (185, 418), (239, 431), (303, 419), (321, 378), (314, 353), (278, 326), (270, 290), (280, 217), (279, 125), (211, 121)]
    ]},
]

widget = patch_canvas(widget, get_asset_path("img/baboon-polygons.png"))
recursively_remove_from_dom(widget)
```

The data in this widget has the following format (note that you can call help
on the `data` property of a widget class to see this text):

```{eval-rst}
.. autoproperty:: ipyannotations.images.PolygonAnnotator.data
```

## Annotating key points, for counting or key-point regression

Key point detection is often used when building augmented reality algorithms
like snapchat filters. To do so, you usually annotate certain points like a
person's eyes, nose, and mouth, and the model learns to predict those. You can
then place things like funny noses relative to the keypoints in an image.

Key points can also be useful if you are merely interested in the location or
count of an object, not the size or shape.

For example, if you were interested in counting the pigeons in a given
photograph (starting with this one taken at the Kazakh pavillion of the VDNKh):

```python
from ipyannotations.images import PointAnnotator
point_widget = PointAnnotator(options=["pigeon"])
point_widget.display("img/vdnkh.jpg")
point_widget
```

```{jupyter-execute}
:hide-code:
from ipyannotations._doc_utils import recursively_remove_from_dom, patch_canvas, get_asset_path
from ipyannotations.images import PointAnnotator
point_widget = PointAnnotator(options=["pigeon"])
point_widget.display(get_asset_path("img/vdnkh.jpg"))
patch_canvas(point_widget, get_asset_path('img/vdnkh-annotated.png'))
recursively_remove_from_dom(point_widget)
```

The data for this `PointAnnotator` widget looks like:

```{eval-rst}
.. autoproperty:: ipyannotations.images.PointAnnotator.data
```

## Annotating bounding boxes

Lastly, a common computer vision task is to place a bounding box around an
object of interest. This is less precise than polygon segmentation, but often
provides enough information for a given application.

To annotate bounding boxes, simply use the `BoxAnnotator`:

```python
from ipyannotations.images import BoxAnnotator
box_widget = BoxAnnotator(options=["eye", "mouth", "nose", "cheek"])
box_widget.display("img/baboon.png")
box_widget
```

```{jupyter-execute}
:hide-code:
from ipyannotations._doc_utils import recursively_remove_from_dom, patch_canvas, get_asset_path
from ipyannotations.images import BoxAnnotator
box_widget = BoxAnnotator(options=["eye", "mouth", "nose", "cheek"])
box_widget.display(get_asset_path("img/baboon.png"))
patch_canvas(box_widget, get_asset_path("img/baboon-boxes.png"))
recursively_remove_from_dom(box_widget)
```

The data for the `BoxAnnotator` widget looks like:

```{eval-rst}
.. autoproperty:: ipyannotations.images.BoxAnnotator.data
```
