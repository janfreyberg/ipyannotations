
import ipywidgets as widgets
from traitlets import Unicode

from ._version import CLIENT_VERSION


class Example(widgets.Widget):

    _view_name = Unicode('ExampleView').tag(sync=True)
    _model_name = Unicode('ExampleModel').tag(sync=True)
    _model_module = Unicode('ipyannotate').tag(sync=True)
    _view_module = Unicode('ipyannotate').tag(sync=True)
    _model_module_version = Unicode(CLIENT_VERSION).tag(sync=True)
    _view_module_version = Unicode(CLIENT_VERSION).tag(sync=True)
