# -*- coding: utf-8 -*-
from .palette import ColorPalette, DARK_PALETTE, LIGHT_PALETTE


class StylesheetGenerator:
    def __init__(self, palette: ColorPalette):
        self.p = palette

    def generate_global(self) -> str:
        return f"""
        * {{
            font-family: "Segoe UI", Roboto, Arial, sans-serif;
            outline: none;
        }}

        QWidget {{
            background-color: {self.p.background_primary};
            color: {self.p.text_primary};
        }}

        QMainWindow {{
            background-color: {self.p.background_primary};
        }}

        QDialog {{
            background-color: {self.p.background_primary};
        }}

        QFrame, 
        QWidget#centralwidget,
        QWidget#layoutWidget,
        QWidget#layoutWidget1,
        QWidget#layoutWidget2 {{
            background-color: transparent;
            border: none;
        }}
        
        QWidget#equipmentContainer {{
        background-color: transparent;
        border: none;
        }}
        """

    def generate_labels(self) -> str:
        return f"""
        QLabel {{
            color: {self.p.text_primary};
            background-color: transparent;
            border: none;
        }}

        QLabel#label,
        QLabel#authLabel,
        QLabel#headline {{
            font-size: 20pt;
            font-weight: bold;
            qproperty-alignment: AlignCenter;
            padding: 20px;
        }}

        QLabel#loginLabel,
        QLabel#passwordLabel,
        QLabel#emailLabel,
        QLabel#label_2,
        QLabel#label_3 {{
            font-size: 11pt;
            padding: 4px 0px;
        }}

        QLabel#forgotPasswordLink,
        QLabel#registerLink,
        QLabel#ifExist {{
            color: {self.p.accent};
            text-decoration: underline;
        }}

        QLabel#labelEquipment {{
            background-color: transparent;
            color: {self.p.text_primary};
            font-weight: 500;
            padding: 6px 12px;
        }}
        """

    def generate_inputs(self) -> str:
        return f"""
        QLineEdit {{
            background-color: {self.p.surface};
            color: {self.p.text_primary};
            border: 1px solid {self.p.border};
            padding: 8px 12px;
            border-radius: 4px;
            min-height: 20px;
        }}

        QLineEdit:focus {{
            border: 2px solid {self.p.accent};
        }}

        QPlainTextEdit {{
            background-color: {self.p.surface};
            color: {self.p.text_primary};
            padding: 8px;
            border: none;
        }}
        """

    def generate_buttons(self) -> str:
        return f"""
        QPushButton {{
            background-color: {self.p.background_secondary};
            color: {self.p.text_primary};
            border: 1px solid {self.p.border};
            padding: 6px 20px;
            border-radius: 4px;
            font-weight: 500;
            min-height: 28px;
        }}

        QPushButton:hover {{
            background-color: {self.p.background_tertiary};
            border-color: {self.p.accent};
        }}

        QPushButton:pressed {{
            background-color: {self.p.accent};
            color: {self.p.text_on_accent};
        }}
        """

    def generate_menus(self) -> str:
        return f"""
        QMenuBar {{
            background-color: {self.p.background_secondary};
            color: {self.p.text_primary};
            border-bottom: 1px solid {self.p.border};
            padding: 4px;
        }}

        QMenuBar::item:selected {{
            background: {self.p.accent};
            color: {self.p.text_on_accent};
        }}

        QMenu {{
            background-color: {self.p.background_secondary};
            color: {self.p.text_primary};
            border: 1px solid {self.p.border};
        }}

        QMenu::item:selected {{
            background-color: {self.p.accent};
            color: {self.p.text_on_accent};
        }}

        QToolBar {{
            background-color: {self.p.background_secondary};
            border-bottom: 1px solid {self.p.border};
            padding: 4px;
            spacing: 4px;
        }}

        QToolButton {{
            background-color: transparent;
            border: 1px solid {self.p.border};
            border-radius: 4px;
            padding: 6px;
            min-width: 24px;
            min-height: 24px;
        }}

        QToolButton:hover {{
            background-color: {self.p.background_tertiary};
            border-color: {self.p.accent};
        }}
        """

    def generate_combobox(self) -> str:
        suffix = "FFFFFF" if self.p == DARK_PALETTE else "000000"

        return f"""
        QComboBox {{
            background-color: transparent;
            color: {self.p.text_primary};
            border: 1px solid {self.p.border};
            padding: 4px 12px;
            border-radius: 4px;
            min-width: 150px;
            min-height: 16px;
        }}

        QComboBox:hover {{
            border-color: {self.p.accent};
        }}
        
        QComboBox::drop-down {{
            subcontrol-origin: padding;
            subcontrol-position: top right;
            width: 24px;
            border-left: 1px solid {self.p.border};
            background-color: transparent;
        }}

        QComboBox::down-arrow {{
            image: url(Icons/arrow_drop_down_24dp_{suffix}.svg);
            width: 16px;
            height: 16px;
        }}
        
        

        QComboBox QAbstractItemView {{
            background-color: {self.p.surface};
            color: {self.p.text_primary};
            border: 1px solid {self.p.border};
            selection-background-color: {self.p.accent};
            selection-color: {self.p.text_on_accent};
            border-radius: 4px;
        }}
        """

    def generate_statusbar(self) -> str:
        return f"""
        QStatusBar {{
            background-color: {self.p.background_secondary};
            color: {self.p.text_primary};
            border-top: 1px solid {self.p.border};
        }}

        QStatusBar QLabel {{
            color: {self.p.text_primary};
            background-color: transparent;
        }}
        """

    def generate_graphics(self) -> str:
        return f"""
        QGraphicsView {{
            background-color: {self.p.background_secondary};
            border: 1px solid {self.p.border};
        }}
        """

    def generate_full_stylesheet(self) -> str:
        parts = [
            self.generate_global(),
            self.generate_labels(),
            self.generate_inputs(),
            self.generate_buttons(),
            self.generate_menus(),
            self.generate_combobox(),
            self.generate_statusbar(),
            self.generate_graphics(),
        ]
        return '\n'.join(parts)


def get_stylesheet(theme_name: str = 'dark') -> str:
    palette = DARK_PALETTE if theme_name == 'dark' else LIGHT_PALETTE
    generator = StylesheetGenerator(palette)
    return generator.generate_full_stylesheet()