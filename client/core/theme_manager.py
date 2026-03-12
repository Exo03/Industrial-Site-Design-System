import platform
from typing import Optional, Callable, List

from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QObject, Signal, QTimer
from PySide6.QtGui import QPalette, QColor

from ..ui.styles.palette import ColorPalette, DARK_PALETTE, LIGHT_PALETTE, PALETTES
from ..ui.styles.stylesheets import StylesheetGenerator


class ThemeManager(QObject):

    theme_changed = Signal(str)
    palette_changed = Signal(ColorPalette)

    _instance: Optional['ThemeManager'] = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return

        super().__init__()
        self._current_theme = 'dark'
        self._app: Optional[QApplication] = None
        self._initialized = True

        self._stylesheet_cache: dict = {}

    def initialize(self, app: QApplication, default_theme: str = 'dark'):
        self._app = app
        self.apply_theme(default_theme)

    @property
    def current_theme(self) -> str:
        return self._current_theme

    @property
    def current_palette(self) -> ColorPalette:
        return PALETTES.get(self._current_theme, DARK_PALETTE)

    def get_color(self, color_name: str) -> str:
        palette = self.current_palette
        return getattr(palette, color_name, '#000000')

    def apply_theme(self, theme_name: str):
        if theme_name not in ['dark', 'light']:
            theme_name = 'dark'

        self._current_theme = theme_name
        palette = PALETTES[theme_name]

        if theme_name not in self._stylesheet_cache:
            generator = StylesheetGenerator(palette)
            self._stylesheet_cache[theme_name] = generator.generate_full_stylesheet()

        stylesheet = self._stylesheet_cache[theme_name]

        if self._app:
            self._app.setStyleSheet(stylesheet)
            self._apply_native_palette(palette)

        self.theme_changed.emit(theme_name)
        self.palette_changed.emit(palette)

    def _apply_native_palette(self, palette: ColorPalette):
        if not self._app:
            return

        p = QPalette()
        p.setColor(QPalette.ColorRole.Window, QColor(palette.background_primary))
        p.setColor(QPalette.ColorRole.WindowText, QColor(palette.text_primary))
        p.setColor(QPalette.ColorRole.Base, QColor(palette.surface))
        p.setColor(QPalette.ColorRole.AlternateBase, QColor(palette.background_tertiary))
        p.setColor(QPalette.ColorRole.Text, QColor(palette.text_primary))
        p.setColor(QPalette.ColorRole.Button, QColor(palette.surface))
        p.setColor(QPalette.ColorRole.ButtonText, QColor(palette.text_primary))
        p.setColor(QPalette.ColorRole.Highlight, QColor(palette.accent))
        p.setColor(QPalette.ColorRole.HighlightedText, QColor(palette.text_on_accent))

        self._app.setPalette(p)

    def toggle_theme(self):
        new_theme = 'light' if self._current_theme == 'dark' else 'dark'
        self.apply_theme(new_theme)
        return new_theme

    def is_dark(self) -> bool:
        return self._current_theme == 'dark'


# Глобальный экземпляр
theme_manager = ThemeManager()