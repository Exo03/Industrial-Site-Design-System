# -*- coding: utf-8 -*-
from dataclasses import dataclass
from typing import Dict


@dataclass
class ColorPalette:
    """Material Design цветовая палитра"""

    # Фоны
    background_primary: str  # Основной фон окна
    background_secondary: str  # Фон карточек/панелей
    background_tertiary: str  # Фон ввода/hover
    surface: str  # Поверхности (кнопки, поля)

    # Акценты
    accent: str
    accent_hover: str
    accent_pressed: str
    accent_secondary: str

    # Текст
    text_primary: str
    text_secondary: str
    text_disabled: str
    text_on_accent: str

    # Границы и разделители
    border: str
    divider: str

    # Состояния
    error: str
    success: str
    warning: str

    # Специфичные
    shadow: str
    overlay: str

DARK_PALETTE = ColorPalette(
    background_primary='#121212',
    background_secondary='#1E1E1E',
    background_tertiary='#2A2A2A',
    surface='#1E1E1E',

    accent='#BB86FC',
    accent_hover='#CC99FF',
    accent_pressed='#AA77DD',
    accent_secondary='#03DAC6',

    text_primary='#FFFFFF',
    text_secondary='#B3B3B3',
    text_disabled='#666666',
    text_on_accent='#000000',

    border='#333333',
    divider='#333333',

    error='#CF6679',
    success='#03DAC6',
    warning='#F9AA33',

    shadow='#000000',
    overlay='rgba(255,255,255,0.1)'
)

LIGHT_PALETTE = ColorPalette(
    background_primary='#F5F5F5',
    background_secondary='#FFFFFF',
    background_tertiary='#FAFAFA',
    surface='#FFFFFF',

    accent='#6200EE',
    accent_hover='#3700B3',
    accent_pressed='#5600E8',
    accent_secondary='#03DAC6',

    text_primary='#212121',
    text_secondary='#757575',
    text_disabled='#9E9E9E',
    text_on_accent='#FFFFFF',

    border='#E0E0E0',
    divider='#E0E0E0',

    error='#B00020',
    success='#018786',
    warning='#F9AA33',

    shadow='rgba(0,0,0,0.2)',
    overlay='rgba(0,0,0,0.05)'
)

SYSTEM_PALETTE = None

PALETTES: Dict[str, ColorPalette] = {
    'dark': DARK_PALETTE,
    'light': LIGHT_PALETTE,
    'system': SYSTEM_PALETTE
}