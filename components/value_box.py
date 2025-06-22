import flet as ft

class ValueBox(ft.Row):
    def __init__(self, value, suffix):
        super().__init__(
            [
                ft.Container(
                    ft.Text(str(value), size=28, weight=ft.FontWeight.W_500),
                    width=110,
                    height=60,
                    alignment=ft.alignment.center,
                    border=ft.border.all(1, "#E4E8EE"),
                    border_radius=8,
                    bgcolor="#FAFCFF",
                ),
                ft.Text(
                    suffix,
                    size=24,
                    color="#1E65F2",  # azul
                    # spans=[
                    #     ft.TextSpan(
                    #         "₁", 
                    #         style=ft.TextStyle(
                    #             size=18, 
                    #             color="#1E65F2", 
                    #             baseline=ft.TextBaseline.IDEOGRAPHIC
                    #         )
                    #     )
                    # ]
                ),
            ],
            # alignment=ft.MainAxisAlignment.CENTER,
            # vertical_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10,
            width=150,
        )