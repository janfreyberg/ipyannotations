# flake8: noqa
import ipywidgets as widgets
import ipyevents
import ipycanvas
import os
import os.path


def recursively_remove_from_dom(
    container_widget,
    to_remove=(ipyevents.Event, ipycanvas.Canvas),
):
    assert hasattr(
        container_widget, "children"
    ), f"{container_widget} is a box, yet doesnt have children??"

    new_children = []

    for child in container_widget.children:
        if isinstance(child, to_remove):
            continue
        if isinstance(child, widgets.Box):
            child = recursively_remove_from_dom(child)
        new_children.append(child)
    container_widget.children = new_children
    return container_widget


def patch_canvas(annotator, img_path):
    with open(img_path, "rb") as f:
        bytesval = f.read()
    img_widg = widgets.Image(value=bytesval)

    annotator.children = [img_widg] + [
        child for child in annotator.children if child is not annotator.canvas
    ]
    # close these so the state doesn't get saved:
    for canvas in annotator.canvas:
        canvas.close()
    annotator.canvas.close()
    return annotator


def get_asset_path(path):
    if bool(os.getenv("READTHEDOCS")):
        return path
    else:
        return os.path.join("source", path)
