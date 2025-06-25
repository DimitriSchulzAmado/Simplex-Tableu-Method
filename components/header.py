import flet as ft

class Header:
    @staticmethod
    def build():
        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text(
                        "Solver de Programação Linear", 
                        theme_style=ft.TextThemeStyle.DISPLAY_SMALL,
                        color=ft.Colors.BLUE_900,
                        weight=ft.FontWeight.BOLD,
                    ),
                    ft.Text(
                        "Resolução pelo Método Simplex com Análise de Sensibilidade",
                        theme_style=ft.TextThemeStyle.BODY_MEDIUM,
                        color=ft.Colors.GREY_700,
                    )
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            bgcolor=ft.Colors.WHITE,
            border_radius=ft.border_radius.all(4),
            padding=ft.padding.symmetric(horizontal=20, vertical=30),
        )
        
    