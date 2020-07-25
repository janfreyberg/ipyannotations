from src.ipyannotations.images.zoom_utils import ZoomController


def test_zoom_controller():
    zoom_controller = ZoomController()

    zoom_controller.zoom_plus()
    assert zoom_controller.zoom_scale == 1.1

    zoom_controller.zoom_minus()
    assert zoom_controller.zoom_scale == 1.

    zoom_controller.zoom_minus()
    assert zoom_controller.zoom_scale == 1.

    assert zoom_controller.canvas.rect_width == 1 / zoom_controller.zoom_scale
    assert zoom_controller.canvas.rect_height == 1 / zoom_controller.zoom_scale