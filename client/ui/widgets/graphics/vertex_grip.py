from PySide6.QtWidgets import QGraphicsObject, QGraphicsItem
from PySide6.QtCore import Qt, QRectF, Signal, QPointF
from PySide6.QtGui import QBrush, QColor, QPen


class VertexGrip(QGraphicsObject):
    vertexMoved = Signal(int, QPointF)

    def __init__(self, index, pos, pixels_per_meter, grid_size_m=0.5, parent=None):
        super().__init__(parent)
        self._index = index
        self._size = 8
        self._pixels_per_meter = pixels_per_meter
        self._grid_size_m = grid_size_m

        self.setPos(pos)

        # ❌ УБИРАЕМ флаг ItemIsMovable, так как он вызывает движение родителя
        # self.setFlag(QGraphicsItem.ItemIsMovable, True)

        self.setFlag(QGraphicsItem.ItemIsSelectable, False)
        self.setCursor(Qt.SizeAllCursor)
        self.setZValue(100)
        self.hide()

    def boundingRect(self):
        half = self._size / 2
        return QRectF(-half, -half, self._size, self._size)

    def paint(self, painter, option, widget=None):
        painter.setBrush(QBrush(QColor(255, 255, 255)))
        painter.setPen(QPen(QColor("#BB86FC"), 2))
        painter.drawRect(self.boundingRect())

    # ⭐ НОВОЕ: РУЧНАЯ ОБРАБОТКА ПЕРЕТАСКИВАНИЯ (Drag & Drop) ⭐

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            # ОЧЕНЬ ВАЖНО: Принимаем событие!
            # Это блокирует передачу клика родительскому полигону
            event.accept()

    def mouseMoveEvent(self, event):
        # event.pos() - это координаты мыши внутри узла.
        # Переводим их в локальные координаты родительского полигона
        parent_pos = self.mapToParent(event.pos())

        # Вычисляем прилипание к сетке (Снаппинг)
        grid_px = self._grid_size_m * self._pixels_per_meter
        snapped_x = round(parent_pos.x() / grid_px) * grid_px
        snapped_y = round(parent_pos.y() / grid_px) * grid_px
        new_pos = QPointF(snapped_x, snapped_y)

        # Перемещаем сам узел
        self.setPos(new_pos)

        # Сигнализируем полигону, что вершина изменилась, чтобы он перерисовался
        self.vertexMoved.emit(self._index, new_pos)
        event.accept()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            event.accept()
