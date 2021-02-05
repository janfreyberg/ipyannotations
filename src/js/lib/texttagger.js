var widgets = require('@jupyter-widgets/base');
var _ = require('lodash');


// When serialiazing the entire widget state for embedding, only values that
// differ from the defaults will be specified.
var TextTaggerModel = widgets.DOMWidgetModel.extend({
    defaults: _.extend(widgets.DOMWidgetModel.prototype.defaults(), {
        _model_name: 'TextTaggerModel',
        _view_name: 'TextTaggerView',
        _model_module: 'ipyannotations',
        _view_module: 'ipyannotations',
        _model_module_version: '0.1.0',
        _view_module_version: '0.1.0',
        text: '',
        classes: [],
        selected_class: '',
        entity_spans: [],
        palette: []
    })
});


// Custom View. Renders the widget model.
var TextTaggerView = widgets.DOMWidgetView.extend({
    // Defines how the widget gets rendered into the DOM
    render: function () {
        this.el.classList.add("entity-tagger")
        this._render_text()
        // Observe changes in the value traitlet in Python, and define
        // a custom callback.
        this.listenTo(this.model, 'change:text', this._render_text, this)
        this.listenTo(this.model, 'change:entity_spans', this._render_text, this)
        this.el.addEventListener('mouseup', this.on_click.bind(this))
    },

    _render_text: function () {
        var text = this.model.get('text')
        var entity_spans = this.model.get('entity_spans')
        entity_spans.sort(
            function (a, b) { return a[0] - b[0] })
        for (var i = entity_spans.length - 1; i >= 0; i--) {
            var span = entity_spans[i]
            text = this._format_entity(text, span, i)
        }
        this.el.innerHTML = text;
    },

    _format_entity: function (text, span, span_index) {
        var classes = this.model.get('classes')
        var class_idx = classes.indexOf(span[2])
        var palette = this.model.get('palette')
        // note: can be undefined, defaults to CSS value (grey)
        var colour = palette[class_idx]
        text = (
            text.slice(0, span[0])
            + `<mark class="entity" data-span_index="${span_index}"`
            + ` style="background:${colour}">`
            + text.slice(span[0], span[1])
            + '<span class="entity-label"> '
            + span[2]
            + '</span>'
            + '</mark>'
            + text.slice(span[1], text.length)
        )
        return text
    },

    on_click: function (event) {
        clicked = event.target
        if (clicked.classList && clicked.classList.contains("entity-label")) {
            clicked = clicked.parentNode
        }
        if (clicked.classList && clicked.classList.contains("entity")) {
            // Remove the clicked-on span:
            var span_index = parseInt(clicked.dataset.span_index)
            var entity_spans = this.model.get('entity_spans')
            var new_entity_spans = [...entity_spans]
            new_entity_spans.splice(span_index, 1)
            this.model.set('entity_spans', new_entity_spans)
        }
        // we are only iterested in text events:
        selection = window.getSelection();
        // if selected:
        if (!selection.isCollapsed) {
            this.on_select()
        }
        this.model.save_changes()
        this.touch()
        this._render_text()
    },

    on_select: function (e) {
        var txt = ""

        selection = window.getSelection()

        if (this.el.contains(selection.baseNode)
            && this.el.contains(selection.focusNode)) {
            snap_to_word(selection)
            var offset = get_offset_relative_to(this.el)
            txt = selection.toString()
            var raw_text = this.model.get('text')
            // append this span as start idx, end idx, class
            var entity_spans = this.model.get('entity_spans')
            var new_entity_spans = [...entity_spans]
            var selected_class = this.model.get('selected_class')
            var span = [offset, offset + txt.length, selected_class]
            new_entity_spans.push(span)
            this.model.set('entity_spans', new_entity_spans)
        }
    }
});

function snap_to_word(selection) {
    // Detect if selection is backwards
    var range = document.createRange();
    range.setStart(selection.anchorNode, selection.anchorOffset);
    range.setEnd(selection.focusNode, selection.focusOffset);
    var backwards = range.collapsed;
    range.detach();
    // modify() works on the focus of the selection
    var endNode = selection.focusNode
    var endOffset = selection.focusOffset;
    selection.collapse(selection.anchorNode, selection.anchorOffset);
    if (backwards) {
        selection.modify("move", "backward", "character");
        selection.modify("move", "forward", "word");
        selection.extend(endNode, endOffset);
        selection.modify("extend", "forward", "character");
        selection.modify("extend", "backward", "word");

    } else {
        selection.modify("move", "forward", "character");
        selection.modify("move", "backward", "word");
        selection.extend(endNode, endOffset);
        selection.modify("extend", "backward", "character");
        selection.modify("extend", "forward", "word");
    }
}

function get_offset_relative_to(parentElement, currentNode) {

    var currentSelection, currentRange,
        offset = 0,
        prevSibling,
        nodeContent;

    if (!currentNode) {
        currentSelection = window.getSelection();
        currentRange = currentSelection.getRangeAt(0);
        currentNode = currentRange.startContainer;
        offset += currentRange.startOffset;
    }

    if (currentNode === parentElement) {
        return offset;
    }

    if (!parentElement.contains(currentNode)) {
        return -1;
    }

    while (prevSibling = (prevSibling || currentNode).previousSibling) {
        nodeContent = get_text_without_label(prevSibling)
        // prevSibling.innerText || prevSibling.nodeValue || "";
        offset += nodeContent.length;
    }

    return offset + get_offset_relative_to(parentElement, currentNode.parentNode);

}

function get_text_without_label(node) {
    if (node.classList && node.classList.contains('entity-label')) {
        return ''
    } else if (node.classList && node.classList.contains('entity')) {
        return node.firstChild.textContent
    } else {
        return node.innerText || node.nodeValue || '';
    }
}

module.exports = {
    TextTaggerModel: TextTaggerModel,
    TextTaggerView: TextTaggerView
};
