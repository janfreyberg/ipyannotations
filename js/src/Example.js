
import * as widgets from '@jupyter-widgets/base';

export class ExampleModel extends widgets.DOMWidgetModel {
  defaults() {
    return {
      ...super.defaults(),
      _model_name: "ExampleModel",
      _view_name: "ExampleView"
    }
  }
}

ExampleModel.serializers = {
  ...widgets.DOMWidgetModel.serializers,
  source: { deserialize: widgets.unpack_models }
}

export class ExampleView extends widgets.DOMWidgetView {
  render() {
    console.log("hello example view");
    console.log(this.model.get("source"));
  }
}
