from typing import Union, Callable

import flet as ft

class ValueBox(ft.Row):
    def __init__(self, page: ft.Page, value: Union[int, float], name: str, has_plus_icon: bool = False, on_change_value: Union[Callable[[float, str], None], None] = None, *args, **kwargs) -> None:
        self._on_change_callback = on_change_value
        self._name = name
        self._value = value
        self._page = page

        super(ValueBox, self).__init__(
            [
                ft.Container(
                    ft.TextField(
                        value=str(self._value),
                        width=110,
                        height=60,
                        text_size=28,
                        text_align=ft.TextAlign.CENTER,
                        border=ft.InputBorder.NONE,
                        content_padding=ft.padding.only(left=0, right=0, top=10, bottom=0),
                        on_change=self._on_change,
                        keyboard_type=ft.KeyboardType.NUMBER,
                        color=ft.Colors.BLACK,
                    ),
                    width=110,
                    height=60,
                    alignment=ft.alignment.center,
                    bgcolor="#FAFCFF",
                    border_radius=8,
                ),
                ft.Text(
                    name,
                    size=24,
                    color="#1E65F2",  # azul
                ),
                ft.Text(
                    "+",
                    style=ft.TextStyle(
                        color=ft.Colors.BLACK,  # azul
                        size=24,
                        weight=ft.FontWeight.W_500,
                    )
                ) if has_plus_icon else ft.Container()
            ],
            # alignment=ft.MainAxisAlignment.CENTER,
            # vertical_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10,
            width=175,
            *args,
            **kwargs,
        )

    def _on_change(self, e: ft.ControlEvent):
        """Handle the change event of the text field."""
        try:
            new_value = float(e.control.value)
            e.control.value = str(new_value)  # Ensure the value is a string

            self._value = new_value

            if self._on_change_callback is not None:
                self._on_change_callback(self._value, self._name)
        except ValueError:
            e.control.value = "0"

            self._value = 0.0
            
            if self._on_change_callback is not None:
                self._on_change_callback(self._value, self._name)
        finally:
            self.update()
            self._page.update()
