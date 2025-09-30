# interface/ui.py
import flet as ft
from .styles import (
    URL_INPUT_STYLE,
    LOG_VIEW_STYLE,
    START_BUTTON_STYLE
)

class AppUI:
    """
    Clase que construye y contiene los elementos de la interfaz de usuario.
    """
    def __init__(self, toggle_process_handler):
        """
        Inicializa la UI y conecta los manejadores de eventos.
        
        :param toggle_process_handler: La función del core que se llamará al hacer clic en el botón.
        """
        self.url_input = ft.TextField(**URL_INPUT_STYLE)
        self.start_button = ft.ElevatedButton(
            **START_BUTTON_STYLE, 
            on_click=toggle_process_handler
        )
        self.log_view = ft.TextField(**LOG_VIEW_STYLE)

    def build_layout(self) -> ft.Column:
        """
        Construye y devuelve el layout principal de la aplicación.
        """
        return ft.Column(
            controls=[
                self.url_input,
                ft.Row([self.start_button], alignment=ft.MainAxisAlignment.CENTER),
                ft.Container(self.log_view, expand=True, padding=ft.padding.only(top=10))
            ],
            expand=True
        )