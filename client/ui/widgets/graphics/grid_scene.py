from PySide6.QtWidgets import QGraphicsScene
from PySide6.QtGui import QPen, QColor


class GridScene(QGraphicsScene):
    def __init__(self, grid_size=10, parent=None):
        super().__init__(parent)
        self._grid_size = grid_size
        self.setSceneRect(0, 0, 10000, 10000)

    def drawBackground(self, painter, rect):
        super().drawBackground(painter, rect)

        # Цвет сетки зависит от темы
        from PySide6.QtWidgets import QApplication
        is_dark = "121212" in QApplication.instance().styleSheet()
        grid_color = QColor(60, 60, 60) if is_dark else QColor(200, 200, 200)

        grid_pen = QPen(grid_color)
        grid_pen.setWidth(1)
        painter.setPen(grid_pen)

        left = int(rect.left()) - (int(rect.left()) % self._grid_size)
        top = int(rect.top()) - (int(rect.top()) % self._grid_size)

        x = left
        while x < rect.right():
            painter.drawLine(x, rect.top(), x, rect.bottom())
            x += self._grid_size

        y = top
        while y < rect.bottom():
            painter.drawLine(rect.left(), y, rect.right(), y)
            y += self._grid_size