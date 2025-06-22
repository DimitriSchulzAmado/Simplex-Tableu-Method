import flet as ft

from typing import Callable, Union


class VariablesControls(ft.Container):
    def __init__(
      self, 
      page: ft.Page, 
      suffix: str, 
      on_change_value: Union[Callable[[int], None], None] = None,
      initial_value: int = 2,
      *args, 
      **kwargs
    ) -> None:
        self._page = page
        self._suffix = suffix
        self._on_change_value = on_change_value
        self._value = initial_value
        self._text = ft.Text()

        super(VariablesControls, self).__init__(
          content=ft.Row(
              controls=[
                  ft.IconButton(
                      icon=ft.Icons.REMOVE,
                      tooltip=f"Diminuir {suffix}(s)",
                      style=ft.ButtonStyle(
                          shape=ft.RoundedRectangleBorder(
                              radius=8
                          ),
                          side={
                              ft.ControlState.DEFAULT: ft.BorderSide(
                                  color=ft.Colors.GREY_800,
                                  width=2
                              ),
                              ft.ControlState.HOVERED: ft.BorderSide(
                                  color=ft.Colors.GREY_500,
                                  width=2
                              ),
                          },
                          icon_color={
                              ft.ControlState.DEFAULT: ft.Colors.GREEN_800,
                              ft.ControlState.HOVERED: ft.Colors.GREY_300,
                          },
                      ),
                      on_click=lambda _: self.decrement(),
                  ),
                  ft.Container(
                      content=self._build_text_label(),
                      bgcolor=ft.Colors.GREY_200,
                      border_radius=ft.border_radius.all(8),
                      padding=ft.padding.symmetric(horizontal=20, vertical=10),
                  ),
                  ft.IconButton(
                      icon=ft.Icons.ADD,
                      tooltip=f"Aumentar {suffix}(s)",
                      style=ft.ButtonStyle(
                          shape=ft.RoundedRectangleBorder(
                              radius=8
                          ),
                          side={
                              ft.ControlState.DEFAULT: ft.BorderSide(
                                  color=ft.Colors.GREY_800,
                                  width=2
                              ),
                              ft.ControlState.HOVERED: ft.BorderSide(
                                  color=ft.Colors.GREY_500,
                                  width=2
                              ),
                          },
                          icon_color={
                              ft.ControlState.DEFAULT: ft.Colors.GREEN_800,
                              ft.ControlState.HOVERED: ft.Colors.GREY_300,
                          }
                      ),
                      on_click=lambda _: self.increment(),
                  )
              ]
          ),
          *args,
          **kwargs,
        )
    
    def _build_text_label(self) -> ft.Text:
        self._text = ft.Text(
          f"{2} {self._suffix}(s)",
          theme_style=ft.TextThemeStyle.BODY_MEDIUM,
          color=ft.Colors.GREY_800,
          text_align=ft.TextAlign.CENTER,
        )

        return self._text
    
    def increment(self) -> None:
        """Increments the variable or constraint count."""
        self._value += 1

        if self._on_change_value is not None:
            self._on_change_value(self._value)

        self._text.value = f"{self._value} {self._suffix}(s)"
        self._page.update()

    def decrement(self) -> None:
        """Decrements the variable or constraint count."""
        if self._value > 2:
            self._value -= 1

            if self._on_change_value is not None:
                self._on_change_value(self._value)

            self._text.value = f"{self._value} {self._suffix}(s)"
        self._page.update()
