from PySide6.QtWidgets import QGraphicsView, QGraphicsPathItem
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QPainter, QWheelEvent, QPainterPath, QPen, QColor

from client.ui.widgets.graphics.snappable_object import PIXELS_PER_METER  # Убедись, что путь импорта верный


class ZoomableGraphicsView(QGraphicsView):
    # Сигнал, который отправляет массив точек [(x, y), ...] в метрах при завершении рисования
    polygonDrawn = Signal(list)

    def __init__(self, scene, parent=None):
        super().__init__(scene, parent)
        self.setTransformationAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)
        self.setResizeAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.setDragMode(QGraphicsView.DragMode.NoDrag)

        self._panning = False
        self._last_pan_pos = None

        # --- Переменные для режима рисования ---
        self._is_drawing = False
        self._draw_points = []  # Список QPointF в координатах сцены

        # Элемент для отображения временной линии при рисовании
        self._preview_path_item = QGraphicsPathItem()
        pen = QPen(QColor(187, 134, 252))  # Фиолетовый (можно заменить на цвет вашей темы)
        pen.setWidth(2)
        pen.setStyle(Qt.DashLine)
        self._preview_path_item.setPen(pen)
        self._preview_path_item.setZValue(9999)  # Рисуем поверх всего

    def start_drawing(self):
        """Включает режим рисования полигона"""
        self._is_drawing = True
        self._draw_points = []
        self._preview_path_item.setPath(QPainterPath())

        if self._preview_path_item not in self.scene().items():
            self.scene().addItem(self._preview_path_item)

        self.setCursor(Qt.CrossCursor)  # Меняем курсор на прицел

    def stop_drawing(self):
        """Выключает режим рисования"""
        self._is_drawing = False
        if self._preview_path_item in self.scene().items():
            self.scene().removeItem(self._preview_path_item)
        self.setCursor(Qt.ArrowCursor)

    def mousePressEvent(self, event):
        if self._is_drawing:
            if event.button() == Qt.LeftButton:
                # Добавляем точку (привязка к сетке 0.5м для точности)
                scene_pos = self.mapToScene(event.pos())
                grid_px = 0.5 * PIXELS_PER_METER
                snapped_x = round(scene_pos.x() / grid_px) * grid_px
                snapped_y = round(scene_pos.y() / grid_px) * grid_px

                snapped_pos = scene_pos.__class__(snapped_x, snapped_y)
                self._draw_points.append(snapped_pos)
                self._update_preview(snapped_pos)
                event.accept()

            elif event.button() == Qt.RightButton:
                # Правый клик - завершить фигуру
                self._finish_drawing()
                event.accept()
            return  # Прерываем стандартную обработку

        # Стандартная логика панорамирования (правая кнопка мыши)
        if event.button() == Qt.MouseButton.RightButton:
            self._panning = True
            self._last_pan_pos = event.position()
            self.setCursor(Qt.CursorShape.ClosedHandCursor)
            event.accept()
        else:
            super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self._is_drawing and self._draw_points:
            # Обновляем линию предпросмотра до текущей позиции мыши
            scene_pos = self.mapToScene(event.pos())
            self._update_preview(scene_pos)
            event.accept()
            return

        if self._panning and self._last_pan_pos:
            delta = event.position() - self._last_pan_pos
            self.horizontalScrollBar().setValue(
                self.horizontalScrollBar().value() - int(delta.x())
            )
            self.verticalScrollBar().setValue(
                self.verticalScrollBar().value() - int(delta.y())
            )
            self._last_pan_pos = event.position()
            event.accept()
        else:
            super().mouseMoveEvent(event)

    def mouseDoubleClickEvent(self, event):
        if self._is_drawing and event.button() == Qt.LeftButton:
            # Двойной левый клик - также завершает фигуру
            self._finish_drawing()
            event.accept()
            return
        super().mouseDoubleClickEvent(event)

    def _update_preview(self, current_pos):
        if not self._draw_points:
            return
        path = QPainterPath()
        path.moveTo(self._draw_points[0])
        for pt in self._draw_points[1:]:
            path.lineTo(pt)
        path.lineTo(current_pos)
        self._preview_path_item.setPath(path)

    def _finish_drawing(self):
        # Если точек меньше 3, это не полигон
        if len(self._draw_points) >= 3:
            # Переводим из пикселей в метры
            polygon_m = [(pt.x() / PIXELS_PER_METER, pt.y() / PIXELS_PER_METER)
                         for pt in self._draw_points]
            self.polygonDrawn.emit(polygon_m)

        self.stop_drawing()

    def wheelEvent(self, event: QWheelEvent):
        # Оставил твой оригинальный код масштабирования
        if event.modifiers() == Qt.KeyboardModifier.ControlModifier:
            delta = event.angleDelta().y()
            if delta != 0:
                zoom_factor = 1.25 if delta > 0 else 1 / 1.25
                self.scale(zoom_factor, zoom_factor)
                event.accept()
        else:
            super().wheelEvent(event)