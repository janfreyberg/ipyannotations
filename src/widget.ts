// Copyright (c) Jan Freyberg
// Distributed under the terms of the Modified BSD License.

import {
  DOMWidgetModel,
  DOMWidgetView,
  ISerializers,
} from '@jupyter-widgets/base';

import { MODULE_NAME, MODULE_VERSION } from './version';

// Import the CSS
import '../css/widget.css';

interface NonStandardSelection extends Selection {
  modify(s: string, t: string, u: string): void;
}

export class TextTaggerModel extends DOMWidgetModel {
  defaults() {
    return {
      ...super.defaults(),
      _model_name: TextTaggerModel.model_name,
      _model_module: TextTaggerModel.model_module,
      _model_module_version: TextTaggerModel.model_module_version,
      _view_name: TextTaggerModel.view_name,
      _view_module: TextTaggerModel.view_module,
      _view_module_version: TextTaggerModel.view_module_version,
      text: '',
      classes: [],
      selected_class: '',
      entity_spans: [],
      palette: [],
    };
  }

  static serializers: ISerializers = {
    ...DOMWidgetModel.serializers,
    // Add any extra serializers here
  };

  static model_name = 'TextTaggerModel';
  static model_module = MODULE_NAME;
  static model_module_version = MODULE_VERSION;
  static view_name = 'TextTaggerView'; // Set to null if no view
  static view_module = MODULE_NAME; // Set to null if no view
  static view_module_version = MODULE_VERSION;
}

export class TextTaggerView extends DOMWidgetView {
  render() {
    this.el.classList.add('entity-tagger');
    this._render_text();
    // Observe changes in the value traitlet in Python, and define
    // a custom callback.
    this.listenTo(this.model, 'change:text', this._render_text);
    this.listenTo(this.model, 'change:entity_spans', this._render_text);
    this.el.addEventListener('mouseup', this.on_click.bind(this));
  }

  _render_text() {
    var text = this.model.get('text');
    var entity_spans = this.model.get('entity_spans');
    entity_spans.sort(function (a: number[], b: number[]) {
      return a[0] - b[0];
    });
    for (var i = entity_spans.length - 1; i >= 0; i--) {
      var span = entity_spans[i];
      text = this._format_entity(text, span, i);
    }
    this.el.innerHTML = text;
  }

  _format_entity(text: string, span: number[], span_index: number) {
    var classes = this.model.get('classes');
    var class_idx = classes.indexOf(span[2]);
    var palette = this.model.get('palette');
    // note: can be undefined, defaults to CSS value (grey)
    var colour = palette[class_idx];
    text =
      text.slice(0, span[0]) +
      `<mark class="entity" data-span_index="${span_index}"` +
      ` style="background:${colour}">` +
      text.slice(span[0], span[1]) +
      '<span class="entity-label"> ' +
      span[2] +
      '</span>' +
      '</mark>' +
      text.slice(span[1], text.length);
    return text;
  }

  on_click(event: Event) {
    // if (!event.target) {
    //   return
    // }
    let clicked: HTMLElement = event.target as HTMLElement;
    if (
      clicked.classList &&
      clicked.classList.contains('entity-label') &&
      clicked.parentNode
    ) {
      clicked = clicked.parentNode as HTMLElement;
    }
    if (
      clicked.classList &&
      clicked.classList.contains('entity') &&
      clicked.dataset.span_index
    ) {
      // Remove the clicked-on span:
      let span_index: number = parseInt(clicked.dataset.span_index);
      var entity_spans = this.model.get('entity_spans');
      var new_entity_spans = [...entity_spans];
      new_entity_spans.splice(span_index, 1);
      this.model.set('entity_spans', new_entity_spans);
    }
    // we are only iterested in text events:
    let selection: Selection = window.getSelection() as Selection;
    // if selected:
    if (!selection.isCollapsed) {
      this.on_select();
    }
    this.model.save_changes();
    this.touch();
    this._render_text();
  }

  on_select() {
    var txt = '';

    let selection: NonStandardSelection =
      window.getSelection() as NonStandardSelection;

    if (
      this.el.contains(selection.anchorNode) &&
      this.el.contains(selection.focusNode)
    ) {
      snap_to_word(selection);
      var offset = get_offset_relative_to(this.el);
      txt = selection.toString();
      // var raw_text = this.model.get('text')
      // append this span as start idx, end idx, class
      var entity_spans = this.model.get('entity_spans');
      var new_entity_spans = [...entity_spans];
      var selected_class = this.model.get('selected_class');
      var span = [offset, offset + txt.length, selected_class];
      new_entity_spans.push(span);
      this.model.set('entity_spans', new_entity_spans);
    }
  }
}

function snap_to_word(selection: NonStandardSelection) {
  // Detect if selection is backwards
  var range = document.createRange();
  range.setStart(selection.anchorNode as Node, selection.anchorOffset);
  range.setEnd(selection.focusNode as Node, selection.focusOffset);
  var backwards = range.collapsed;
  range.detach();
  // modify() works on the focus of the selection
  let endNode: Node = selection.focusNode as Node;
  let endOffset: number = selection.focusOffset;
  selection.collapse(selection.anchorNode, selection.anchorOffset);
  if (backwards) {
    selection.modify('move', 'backward', 'character');
    selection.modify('move', 'forward', 'word');
    selection.extend(endNode, endOffset);
    selection.modify('extend', 'forward', 'character');
    selection.modify('extend', 'backward', 'word');
  } else {
    selection.modify('move', 'forward', 'character');
    selection.modify('move', 'backward', 'word');
    selection.extend(endNode, endOffset);
    selection.modify('extend', 'backward', 'character');
    selection.modify('extend', 'forward', 'word');
  }
}

function get_offset_relative_to(
  parentElement: Node,
  currentNode?: Node
): number {
  var currentSelection,
    currentRange,
    offset = 0,
    prevSibling,
    nodeContent;

  if (!currentNode) {
    currentSelection = window.getSelection();
    if (!currentSelection) {
      return -1;
    }
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

  while (
    (prevSibling = (prevSibling || currentNode).previousSibling as HTMLElement)
  ) {
    nodeContent = get_text_without_label(prevSibling) as string;
    // prevSibling.innerText || prevSibling.nodeValue || "";
    offset += nodeContent.length;
  }

  return (
    offset +
    get_offset_relative_to(parentElement, currentNode.parentNode as Node)
  );
}

function get_text_without_label(node: HTMLElement) {
  if (node.classList && node.classList.contains('entity-label')) {
    return '';
  } else if (
    node.classList &&
    node.classList.contains('entity') &&
    node.firstChild
  ) {
    return node.firstChild.textContent;
  } else {
    return node.innerText || node.nodeValue || '';
  }
}
