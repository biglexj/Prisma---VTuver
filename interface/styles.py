import flet as ft

APP_TITLE = "Prisma VTuber - Ely"

URL_INPUT_STYLE = {
    "label": "URL del video en vivo de YouTube",
    "hint_text": "Pega la URL aquí...",
    "width": 550,
    "border_color": ft.colors.PURPLE_300,
}

LOG_VIEW_STYLE = {
    "label": "Logs y Respuestas",
    "multiline": True,
    "read_only": True,
    "expand": True,
    "min_lines": 15,
}

START_BUTTON_STYLE = {
    "text": "Iniciar",
    "bgcolor": ft.colors.GREEN_700,
    "color": ft.colors.WHITE,
}

STOP_BUTTON_STYLE = {
    "text": "Detener",
    "bgcolor": ft.colors.RED_700,
    "color": ft.colors.WHITE,
}