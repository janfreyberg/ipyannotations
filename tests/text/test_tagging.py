from ipyannotations import text


def test_displaying_text_clears_data():

    widget = text.TextTagger()
    widget.data = [(0, 1, "MISC")]

    widget.display("Some other text.")

    assert widget.data == []


def test_undo_queue():

    widget = text.TextTagger()

    widget.display("Start text.")
    widget.data = [(0, 2, "MISC")]
    widget.data = [(0, 2, "MISC"), (3, 7, "LOC")]
    widget.data = []

    widget.undo()
    assert widget.data == [(0, 2, "MISC"), (3, 7, "LOC")]
    widget.undo()
    assert widget.data == [(0, 2, "MISC")]
    widget.undo()
    assert widget.data == []


def test_keystroke_handling():
    widget = text.TextTagger(classes=["MISC", "PER"])
    widget.display("Start text.")
    assert widget.class_selector.value == "MISC"
    widget._handle_keystroke({"type": "keyup", "key": "2"})
    assert widget.class_selector.value == "PER"
