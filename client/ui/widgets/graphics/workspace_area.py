from PySide6.QtWidgets import QGraphicsObject, QGraphicsItem
from PySide6.QtCore import QRectF
from PySide6.QtGui import QPen, QColor, Qt

from client.core import theme_manager
from .snappable_object import PIXELS_PER_METER


class WorkspaceArea(QGraphicsObject):
    def __init__(self, width_m, height_m, pixels_per_meter=PIXELS_PER_METER):
        super().__init__()
        self._width_m = width_m
        self._height_m = height_m
        self._pixels_per_meter = pixels_per_meter

        self.setFlag(QGraphicsItem.ItemIsSelectable, False)
        self.setFlag(QGraphicsItem.ItemIsMovable, False)
        self.setFlag(QGraphicsItem.ItemIsFocusable, False)

    def boundingRect(self):
        w_px = self._width_m * self._pixels_per_meter
        h_px = self._height_m * self._pixels_per_meter
        return QRectF(0, 0, w_px, h_px)

    def paint(self, painter, option, widget=None):
        w_px = self._width_m * self._pixels_per_meter
        h_px = self._height_m * self._pixels_per_meter

        if theme_manager.current_theme == "dark":
            color = QColor(255, 255, 255)
        else:
            color = QColor(0, 0, 0)

        pen = QPen(color)
        pen.setWidth(3)
        painter.setPen(pen)
        painter.setBrush(Qt.NoBrush)
        painter.drawRect(0, 0, w_px, h_px)