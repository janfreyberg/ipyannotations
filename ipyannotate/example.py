import ipywidgets as widgets
from ipywidgets.widgets.trait_types import InstanceDict
from ipywidgets import Image
from traitlets import Unicode

from ._version import CLIENT_VERSION


class Example(widgets.DOMWidget):

    _view_name = Unicode("ExampleView").tag(sync=True)
    _model_name = Unicode("ExampleModel").tag(sync=True)
    _model_module = Unicode("ipyannotate").tag(sync=True)
    _view_module = Unicode("ipyannotate").tag(sync=True)
    _model_module_version = Unicode(CLIENT_VERSION).tag(sync=True)
    _view_module_version = Unicode(CLIENT_VERSION).tag(sync=True)
    source = InstanceDict(Image).tag(sync=True, **widgets.widget_serialization)
    # source = Unicode().tag(sync=True)
