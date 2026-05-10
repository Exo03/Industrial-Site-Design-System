from PySide6.QtWidgets import QGraphicsObject, QGraphicsItem
from PySide6.QtCore import Qt, QRectF, QPointF, Signal
from PySide6.QtGui import QBrush, QColor, QPen, QFont, QFontMetrics, QPolygonF, QPainterPath, QPainterPathStroker

from client.core import theme_manager
from .vertex_grip import VertexGrip

PIXELS_PER_METER = 20

class SnappableObject(QGraphicsObject):
    def __init__(self, text="Объект", width_m=6.0, height_m=4.0, polygon_m=None, color="#96C8FF",
                 grid_size_m=0.5, pixels_per_meter=PIXELS_PER_METER, parent=None,
                 zone_margin_m=0.0):
        super().__init__(parent)
        self._pixels_per_meter = pixels_per_meter
        self._grid_size_m = grid_size_m

        # Оставляем для совместимости со старым кодом
        self._width_m = width_m
        self._height_m = height_m

        self._text = text
        self._color = QColor(color)
        self._zone_margin_m = zone_margin_m

        self._is_zone_outside_area = False
        self._is_zone_overlapping = False
        self._is_outside_area = False
        self._is_overlapping = False

        # ... (существующий код __init__ в SnappableObject) ...
        self.setFlag(QGraphicsItem.ItemIsMovable, True)
        self.setFlag(QGraphicsItem.ItemIsSelectable, True)
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges, True)

        # Формируем полигон
        self._polygon_px = QPolygonF()
        if polygon_m:
            for pt in polygon_m:
                self._polygon_px.append(QPointF(pt[0] * pixels_per_meter, pt[1] * pixels_per_meter))
        else:
            w_px = self._px(self._width_m)
            h_px = self._px(self._height_m)
            self._polygon_px = QPolygonF([
                QPointF(0, 0), QPointF(w_px, 0), QPointF(w_px, h_px), QPointF(0, h_px)
            ])
        self._grips = []
        self._create_grips()

    def _px(self, meters):
        return meters * self._pixels_per_meter

    def bodyPath(self):
        """Возвращает точный контур самого объекта"""
        path = QPainterPath()
        path.addPolygon(self._polygon_px)
        return path

    def zonePath(self):
        """Вычисляет расширенный контур зоны обслуживания"""
        path = self.bodyPath()
        margin_px = self._px(self._zone_margin_m)
        if margin_px > 0:
            stroker = QPainterPathStroker()
            # Ширина линии равна двум отступам, так как она растет в обе стороны от контура
            stroker.setWidth(margin_px * 2)
            stroker.setJoinStyle(Qt.MiterJoin)
            stroker.setCapStyle(Qt.SquareCap)
            stroked = stroker.createStroke(path)
            # Объединяем исходный полигон с его обводкой для получения сплошной зоны
            path = path.united(stroked)
        return path

    def boundingRect(self):
        return self.zonePath().boundingRect()

    def shape(self):
        # Этот метод критически важен для кликов мышью и выделения
        return self.zonePath()

    # Сеттеры оставляем без изменений...
    def set_zone_outside_area(self, is_outside: bool):
        if self._is_zone_outside_area != is_outside:
            self._is_zone_outside_area = is_outside
            self.update()

    def set_zone_overlapping(self, is_overlapping: bool):
        if self._is_zone_overlapping != is_overlapping:
            self._is_zone_overlapping = is_overlapping
            self.update()

    def set_outside_area(self, is_outside: bool):
        if self._is_outside_area != is_outside:
            self._is_outside_area = is_outside
            self.update()

    def set_overlapping(self, is_overlapping: bool):
        if self._is_overlapping != is_overlapping:
            self._is_overlapping = is_overlapping
            self.update()

    def update_zone_margin(self, margin_m):
        self.prepareGeometryChange()
        self._zone_margin_m = margin_m
        self.update()

    def paint(self, painter, option, widget=None):
        zone_path = self.zonePath()
        body_path = self.bodyPath()

        # 1. ОТРИСОВКА ЗОНЫ ОБСЛУЖИВАНИЯ
        if self._zone_margin_m > 0:
            if self._is_zone_outside_area:
                fill_color = QColor(255, 0, 0, 50)
                pen_color = QColor(255, 0, 0, 255)
            elif self._is_zone_overlapping:
                fill_color = QColor(255, 255, 0, 50)
                pen_color = QColor(255, 255, 0, 255)
            else:
                fill_color = QColor(128, 128, 128, 30)
                is_dark = theme_manager.current_theme == "dark"
                pen_color = QColor(255, 255, 255, 200) if is_dark else QColor(0, 0, 0, 200)

            painter.setBrush(QBrush(fill_color))
            pen = QPen(pen_color)
            pen.setWidth(1)
            painter.setPen(pen)
            painter.drawPath(zone_path)

        # 2. ОТРИСОВКА САМОГО ОБЪЕКТА
        painter.setBrush(QBrush(self._color))
        base_pen = QPen(QColor(0, 0, 0, 150))
        base_pen.setWidth(1)
        painter.setPen(base_pen)
        painter.drawPath(body_path)

        # Рисуем текст по центру габаритов полигона
        bounds = self._polygon_px.boundingRect()
        self._draw_wrapped_text(painter, bounds.width(), bounds.height())

        # Выделение объекта
        if self.isSelected():
            pen = QPen(QColor(255, 255, 255))
            pen.setWidth(1)
            pen.setStyle(Qt.DashLine)
            painter.setPen(pen)
            painter.setBrush(Qt.NoBrush)
            painter.drawPath(body_path)

        # Коллизия
        if self._is_overlapping:
            painter.setPen(QPen(QColor(255, 255, 0), 2))
            painter.setBrush(Qt.NoBrush)
            painter.drawPath(body_path)

        # Выход за пределы
        if self._is_outside_area:
            painter.setPen(QPen(QColor(255, 0, 0), 2))
            painter.setBrush(Qt.NoBrush)
            painter.drawPath(body_path)

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
        elif change == QGraphicsItem.ItemSelectedHasChanged:
            is_selected = bool(value)
            for grip in self._grips:
                grip.setVisible(is_selected)
        return super().itemChange(change, value)

    def update_text(self, text):
        self._text = text
        self.update()

    def _create_grips(self):
        """Создает интерактивные точки для каждой вершины полигона"""
        # Очищаем старые узлы, если они были
        for grip in self._grips:
            self.scene().removeItem(grip) if self.scene() else None
            grip.deleteLater()
        self._grips.clear()

        # Создаем новые узлы
        for i in range(self._polygon_px.count()):
            grip = VertexGrip(
                index=i,
                pos=self._polygon_px.at(i),
                pixels_per_meter=self._pixels_per_meter,
                grid_size_m=self._grid_size_m,
                parent=self  # Делаем узел дочерним элементом объекта!
            )
            # Подписываемся на перемещение узла
            grip.vertexMoved.connect(self._on_grip_moved)
            self._grips.append(grip)

    def _on_grip_moved(self, index, new_pos):
        """Вызывается, когда пользователь перетаскивает узел (VertexGrip)"""
        self.prepareGeometryChange()  # Обязательно перед изменением формы!

        # Обновляем координаты конкретной вершины
        points = [self._polygon_px.at(i) for i in range(self._polygon_px.count())]
        points[index] = new_pos
        self._polygon_px = QPolygonF(points)

        # Пересчитываем габариты объекта (Bounding Box)
        # Если мы вытянули точку далеко, ширина и длина объекта изменились
        bounds = self._polygon_px.boundingRect()
        self._width_m = bounds.width() / self._pixels_per_meter
        self._height_m = bounds.height() / self._pixels_per_meter

        self.update()  # Перерисовываем объект
        self.geometryChanged.emit()  # Сигнализируем окну для проверки коллизий

    def update_size(self, width_m, height_m):
        """
        Масштабирует полигон объекта так, чтобы его габаритный контейнер (Bounding Box)
        соответствовал новым значениям width_m и height_m.
        """
        self.prepareGeometryChange()

        # Получаем текущие габариты полигона в пикселях
        current_bounds = self._polygon_px.boundingRect()
        current_w_px = current_bounds.width()
        current_h_px = current_bounds.height()

        if current_w_px > 0 and current_h_px > 0:
            # Переводим целевые метры в пиксели
            target_w_px = self._px(width_m)
            target_h_px = self._px(height_m)

            # Вычисляем коэффициенты масштабирования (Scale)
            scale_x = target_w_px / current_w_px
            scale_y = target_h_px / current_h_px

            # Создаем новый отмасштабированный полигон
            new_polygon = QPolygonF()
            for i in range(self._polygon_px.count()):
                pt = self._polygon_px.at(i)
                # Умножаем координаты каждой вершины на коэффициенты
                # Масштабирование происходит относительно точки (0,0) (локального начала координат)
                new_polygon.append(QPointF(pt.x() * scale_x, pt.y() * scale_y))

            self._polygon_px = new_polygon

        # Обязательно сохраняем новые габариты, чтобы при следующем открытии окна
        # редактирования (EditObjectWindow) отображались актуальные данные
        self._width_m = width_m
        self._height_m = height_m

        self._create_grips()
        if self.isSelected():
            for grip in self._grips:
                grip.show()

        self.update()

    def update_color(self, color):
        self._color = QColor(color)
        self.update()