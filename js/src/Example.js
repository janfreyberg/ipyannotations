
import * as widgets from '@jupyter-widgets/base';

export class ExampleModel extends widgets.WidgetModel {
  defaults() {
    return {
      ...super.defaults(),
      _model_name: "ExampleModel",
      _view_name: "ExampleView"
    }
  }
}


export class ExampleView extends widgets.WidgetView {
  render() {
    console.log("hello example view");
  }
}
