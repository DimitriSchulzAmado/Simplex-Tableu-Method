import flet as ft


class ResultRow(ft.Container):
    def __init__(self, result: str, **kwargs):
        params = {
            "padding": ft.padding.symmetric(horizontal=20, vertical=18),
            "bgcolor": ft.Colors.LIGHT_BLUE_400,
            "border_radius": ft.border_radius.all(8),
            **kwargs
        }

        super(ResultRow, self).__init__(
            content=ft.Row(
                controls=[
                    ft.Text(
                        "X₁ + 2X₂ ≤ 14",
                        theme_style=ft.TextThemeStyle.BODY_MEDIUM,
                        color=ft.Colors.WHITE,
                        width=200,
                    ),
                    ft.Text(
                        "0.5",
                        theme_style=ft.TextThemeStyle.BODY_MEDIUM,
                        color=ft.Colors.WHITE,
                    ),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
            **params,
        )
