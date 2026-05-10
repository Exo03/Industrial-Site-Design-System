from PySide6.QtWidgets import QGraphicsObject, QGraphicsItem
from PySide6.QtCore import QPointF
from PySide6.QtGui import QPen, QColor, Qt, QPolygonF, QPainterPath

from client.core import theme_manager
from .snappable_object import PIXELS_PER_METER


class WorkspaceArea(QGraphicsObject):
    def __init__(self, width_m=None, height_m=None, polygon_m=None, pixels_per_meter=PIXELS_PER_METER):
        super().__init__()
        self._pixels_per_meter = pixels_per_meter

        # Формируем полигон площадки
        self._polygon_px = QPolygonF()
        if polygon_m:
            # Если передан список координат [(x, y), ...]
            for pt in polygon_m:
                self._polygon_px.append(QPointF(pt[0] * pixels_per_meter, pt[1] * pixels_per_meter))
        elif width_m is not None and height_m is not None:
            # Обратная совместимость для прямоугольных площадок
            self._width_m = width_m
            self._height_m = height_m
            w_px = width_m * pixels_per_meter
            h_px = height_m * pixels_per_meter
            self._polygon_px = QPolygonF([
                QPointF(0, 0), QPointF(w_px, 0), QPointF(w_px, h_px), QPointF(0, h_px)
            ])

        self.setFlag(QGraphicsItem.ItemIsSelectable, False)
        self.setFlag(QGraphicsItem.ItemIsMovable, False)
        self.setFlag(QGraphicsItem.ItemIsFocusable, False)

    def boundingRect(self):
        # Возвращаем описывающий прямоугольник полигона
        return self._polygon_px.boundingRect()

    def shape(self):
        # Точный контур площадки (нужен для точных коллизий)
        path = QPainterPath()
        path.addPolygon(self._polygon_px)
        return path

    def paint(self, painter, option, widget=None):
        if theme_manager.current_theme == "dark":
            color = QColor(255, 255, 255)
        else:
            color = QColor(0, 0, 0)

        pen = QPen(color)
        pen.setWidth(3)
        painter.setPen(pen)
        painter.setBrush(Qt.NoBrush)
        # Рисуем полигон вместо прямоугольника
        painter.drawPolygon(self._polygon_px)