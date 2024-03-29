
```{hint}
This page is only partially interactive. Since this is a static HTML page, only
front-end interactivity works. This means you can click buttons, but the
relevant python-level responses to those actions won't occur.
```

# Captions and question answering or summarisation

Many tasks require free-text entry, such as image captioning,
question answering or translation, and summarisation.

This can be achieved with several freetext entry widgets.

## Image captioning

The `FreetextAnnotator` class supports freetext entry for image tasks:

```python
from ipyannotations.images import FreetextAnnotator

widget = FreetextAnnotator()
widget.display('img/vdnkh.jpg')

widget
```

```{jupyter-execute}
:hide-code:
from ipyannotations._doc_utils import recursively_remove_from_dom, patch_canvas, get_asset_path
from ipyannotations.images import FreetextAnnotator

widget = FreetextAnnotator()
widget.display(get_asset_path('img/vdnkh.jpg'))

recursively_remove_from_dom(widget)
```

## Freetext for text (translation, summarisation)

The `FreetextAnnotator` class supports freetext entry for summarisation:

```python
from ipyannotations.text import FreetextAnnotator

widget = FreetextAnnotator(
textbox_placeholder='Please provide a one-sentence summary. Use Shift+Enter to submit.')
widget.display(
    'Let $C$ be a smooth projective curve of genus $g≥2$ and let $N$ be the moduli '
    'space of stable rank 2 vector bundles on C of odd degree. We construct a '
    'semi-orthogonal decomposition of the bounded derived category of N '
    'conjectured by Narasimhan. It has two blocks for each i-th symmetric power '
    'of $C$ for $i=0,..,g−2$ and one block for the $(g−1)$-st symmetric power. We '
    'conjecture that the subcategory generated by our blocks has a trivial '
    'semi-orthogonal complement, proving the full Narasimhan conjecture. Our '
    'proof is based on an analysis of wall-crossing between moduli spaces of '
    'stable pairs, combining classical vector bundles techniques with the method '
    'of windows.')

widget
```

```{jupyter-execute}
:hide-code:
from ipyannotations._doc_utils import recursively_remove_from_dom, patch_canvas, get_asset_path
from ipyannotations.text import FreetextAnnotator

widget = FreetextAnnotator(
textbox_placeholder='Please provide a one-sentence summary. Use Shift+Enter to submit.')
widget.display(
    'Let $C$ be a smooth projective curve of genus $g≥2$ and let $N$ be the moduli '
    'space of stable rank 2 vector bundles on C of odd degree. We construct a '
    'semi-orthogonal decomposition of the bounded derived category of N '
    'conjectured by Narasimhan. It has two blocks for each i-th symmetric power '
    'of $C$ for $i=0,..,g−2$ and one block for the $(g−1)$-st symmetric power. We '
    'conjecture that the subcategory generated by our blocks has a trivial '
    'semi-orthogonal complement, proving the full Narasimhan conjecture. Our '
    'proof is based on an analysis of wall-crossing between moduli spaces of '
    'stable pairs, combining classical vector bundles techniques with the method '
    'of windows.')

widget

recursively_remove_from_dom(widget)
```

## Arbitrary captioning

As with classification, there is a generic captioning widget, which allows you
to pass your own display function. An example would be audio transcription:

```python
from ipyannotations.generic import FreetextAnnotator
from IPython.display import display, Audio


widget = ipyannotations.generic.FreetextAnnotator(
    display_function=lambda f: display(Audio(filename=f)),
    textbox_placeholder='Please transcribe the audio sample. Use Shift+Enter to submit.',
)
widget.display('audio/Akwai_ibom_state.ogg')

widget
```

```{jupyter-execute}
:hide-code:
from ipyannotations._doc_utils import recursively_remove_from_dom, patch_canvas, get_asset_path
import ipyannotations.generic
from IPython.display import display, Audio
audiopath = get_asset_path('audio/Akwai_ibom_state.ogg')

widget = ipyannotations.generic.FreetextAnnotator(
    display_function=lambda f: display(Audio(filename=f)),
    textbox_placeholder='Please transcribe the audio sample. Use Shift+Enter to submit.',
)
widget.display(audiopath)

recursively_remove_from_dom(widget)
```

_Audio file by Aliyu Shaba via [wikimedia commons](https://commons.wikimedia.org/wiki/File:Akwai_ibom_state.ogg)._
