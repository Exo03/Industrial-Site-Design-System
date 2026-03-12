from PySide6.QtWidgets import QGraphicsObject, QGraphicsItem
from PySide6.QtCore import Qt, QRectF, QPointF, Signal
from PySide6.QtGui import QBrush, QColor, QPen, QFont, QFontMetrics

from client.core import theme_manager

PIXELS_PER_METER = 20


class SnappableObject(QGraphicsObject):
    def __init__(self, text="Объект", width_m=6.0, height_m=4.0, color="#96C8FF",
                 grid_size_m=0.5, pixels_per_meter=PIXELS_PER_METER, parent=None):
        super().__init__(parent)
        self._pixels_per_meter = pixels_per_meter
        self._grid_size_m = grid_size_m
        self._width_m = width_m
        self._height_m = height_m
        self._text = text
        self._color = QColor(color)

        self.setFlag(QGraphicsItem.ItemIsMovable, True)
        self.setFlag(QGraphicsItem.ItemIsSelectable, True)
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges, True)

        self._is_outside_area = False
        self._is_overlapping = False

    def _px(self, meters):
        return meters * self._pixels_per_meter

    def boundingRect(self):
        return QRectF(0, 0, self._px(self._width_m), self._px(self._height_m))

    def set_outside_area(self, is_outside: bool):
        if self._is_outside_area != is_outside:
            self._is_outside_area = is_outside
            self.update()

    def set_overlapping(self, is_overlapping: bool):
        if self._is_overlapping != is_overlapping:
            self._is_overlapping = is_overlapping
            self.update()

    def paint(self, painter, option, widget=None):
        w_px = self._px(self._width_m)
        h_px = self._px(self._height_m)

        painter.setBrush(QBrush(self._color))
        base_pen = QPen(QColor(0, 0, 0, 150))
        base_pen.setWidth(1)
        painter.setPen(base_pen)
        painter.drawRect(0, 0, w_px, h_px)

        self._draw_wrapped_text(painter, w_px, h_px)

        if self.isSelected():

            if theme_manager.current_theme == "dark":
                color = QColor(255, 255, 255)
            else:
                color = QColor(255, 255, 255)

            pen = QPen(color)
            pen.setWidth(1)
            pen.setStyle(Qt.DashLine)
            painter.setPen(pen)
            painter.setBrush(Qt.NoBrush)
            painter.drawRect(0, 0, w_px, h_px)

        if self._is_overlapping:
            yellow_pen = QPen(QColor(255, 255, 0))
            yellow_pen.setWidth(2)
            painter.setPen(yellow_pen)
            painter.setBrush(Qt.NoBrush)
            painter.drawRect(0, 0, w_px, h_px)

        if self._is_outside_area:
            red_pen = QPen(QColor(255, 0, 0))
            red_pen.setWidth(2)
            painter.setPen(red_pen)
            painter.setBrush(Qt.NoBrush)
            painter.drawRect(0, 0, w_px, h_px)

    def _draw_wrapped_text(self, painter, w_px, h_px):
        margin = max(4, int(min(w_px, h_px) * 0.05))
        available_width = w_px - 2 * margin
        available_height = h_px - 2 * margin

        if available_width <= 0 or available_height <= 0:
            return

        max_font_size = 12
        min_font_size = 6

        font = painter.font()
        best_font_size = min_font_size
        best_lines = []

        for font_size in range(max_font_size, min_font_size - 1, -1):
            font.setPointSize(font_size)
            font.setBold(False)
            metrics = QFontMetrics(font)
            line_height = metrics.height()

            lines = self._wrap_text(self._text, metrics, available_width)
            total_height = len(lines) * line_height

            if total_height <= available_height:
                best_font_size = font_size
                best_lines = lines
                break

        if not best_lines:
            font.setPointSize(min_font_size)
            font.setBold(True)
            metrics = QFontMetrics(font)
            best_lines = self._wrap_text(self._text, metrics, available_width)

        painter.setFont(font)
        text_color = self._get_contrast_color(self._color)
        painter.setPen(text_color)

        metrics = QFontMetrics(font)
        line_height = metrics.height()
        total_text_height = len(best_lines) * line_height

        start_y = (h_px - total_text_height) / 2 + metrics.ascent()

        for i, line in enumerate(best_lines):
            text_width = metrics.horizontalAdvance(line)
            x = (w_px - text_width) / 2
            y = start_y + i * line_height
            painter.drawText(int(x), int(y), line)

    def _wrap_text(self, text, metrics, max_width):
        words = text.split()
        lines = []
        current_line = ""

        for word in words:
            test_line = current_line + " " + word if current_line else word
            text_width = metrics.horizontalAdvance(test_line)

            if text_width <= max_width:
                current_line = test_line
            else:
                if current_line:
                    lines.append(current_line)

                if metrics.horizontalAdvance(word) > max_width:
                    lines.extend(self._break_long_word(word, metrics, max_width))
                    current_line = ""
                else:
                    current_line = word

        if current_line:
            lines.append(current_line)

        return lines if lines else [text]

    def _break_long_word(self, word, metrics, max_width):
        lines = []
        current = ""

        for char in word:
            test = current + char
            if metrics.horizontalAdvance(test) <= max_width:
                current = test
            else:
                if current:
                    lines.append(current)
                current = char

        if current:
            lines.append(current)

        return lines if lines else [word]

    def _get_contrast_color(self, background_color):
        luminance = (0.299 * background_color.red() +
                     0.587 * background_color.green() +
                     0.114 * background_color.blue()) / 255
        return QColor(0, 0, 0) if luminance > 0.5 else QColor(255, 255, 255)

    geometryChanged = Signal()

    def itemChange(self, change, value):
        if change == QGraphicsItem.ItemPositionChange and self.scene():
            grid_px = self._px(self._grid_size_m)
            x = round(value.x() / grid_px) * grid_px
            y = round(value.y() / grid_px) * grid_px
            new_value = QPointF(x, y)
            result = super().itemChange(change, new_value)
            self.geometryChanged.emit()
            return result
        elif change == QGraphicsItem.ItemTransformHasChanged:
            self.geometryChanged.emit()
        return super().itemChange(change, value)

    def update_text(self, text):
        self._text = text
        self.update()

    def update_size(self, width_m, height_m):
        self._width_m = width_m
        self._height_m = height_m
        self.prepareGeometryChange()
        self.update()

    def update_color(self, color):
        self._color = QColor(color)
        self.update()