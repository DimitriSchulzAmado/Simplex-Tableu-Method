from typing import Callable, Union

import flet as ft

from data.app_state import Constraint, ConstraintSymbol
from components.value_box import ValueBox


class ConstraintValues(ft.Container):
    def __init__(
          self, 
          page: ft.Page, 
          constraint: Constraint, 
          on_change_variable_value: Union[Callable[[float, str], None], None] = None,
          on_change_constraint_value: Union[Callable[[str], None], None] = None,
          on_change_constraint_symbol: Union[Callable[[str], None], None] = None,
          *args, 
          **kwargs
        ) -> None:
        self._page = page
        self._constraint = constraint
        self._on_change_variable_value_callback = on_change_variable_value
        self._on_change_constraint_value_callback = on_change_constraint_value
        self._on_change_constraint_symbol_callback = on_change_constraint_symbol

        super(ConstraintValues, self).__init__(
            content=ft.Column(
                controls=[
                    ft.Text(
                        self._constraint.name,
                        theme_style=ft.TextThemeStyle.BODY_LARGE,
                        size=20,
                        color=ft.Colors.BLACK,
                    ),
                    ft.Row(
                        wrap=True,
                        spacing=8,         # espaço horizontal entre controles
                        run_spacing=8,     # espaço vertical entre "linhas"
                        alignment=ft.MainAxisAlignment.START,
                        run_alignment=ft.MainAxisAlignment.START,
                        controls=[
                            *self._build_values_box(),
                            ft.Dropdown(
                                options=[
                                    ft.DropdownOption(
                                        key=ConstraintSymbol.EQUAL.value,
                                        text=ConstraintSymbol.EQUAL.value,
                                        style=ft.ButtonStyle(
                                          color=ft.Colors.BLACK,
                                        ),
                                    ),
                                    ft.DropdownOption(
                                        key=ConstraintSymbol.LESS_THAN_OR_EQUAL.value,
                                        text=ConstraintSymbol.LESS_THAN_OR_EQUAL.value,
                                        style=ft.ButtonStyle(
                                          color=ft.Colors.BLACK,
                                        ),
                                    ),
                                    ft.DropdownOption(
                                        key=ConstraintSymbol.GREATER_THAN_OR_EQUAL.value,
                                        text=ConstraintSymbol.GREATER_THAN_OR_EQUAL.value,
                                        style=ft.ButtonStyle(
                                          color=ft.Colors.BLACK,
                                        ),
                                    ),
                                ],
                                value=self._constraint.symbol.value,
                                on_change=self._on_change_constraint_symbol,
                                width=150,
                                # height=60,
                                fill_color=ft.Colors.WHITE,       # requer filled=True
                                filled=True,
                                border_radius=8,
                                color=ft.Colors.BLACK,
                                bgcolor=ft.Colors.WHITE,
                                text_size=20,
                                text_align=ft.TextAlign.CENTER,
                                border_width=0,
                            ),
                            ft.Container(
                              ft.TextField(
                                  value=str(self._constraint.value),
                                  width=110,
                                  height=60,
                                  text_size=28,
                                  text_align=ft.TextAlign.CENTER,
                                  border=ft.InputBorder.NONE,
                                  content_padding=ft.padding.only(left=0, right=0, top=10, bottom=0),
                                  on_change=self._on_change_constraint_value,
                                  keyboard_type=ft.KeyboardType.NUMBER,
                                  color=ft.Colors.BLACK,
                              ),
                              width=110,
                              height=60,
                              alignment=ft.alignment.center,
                              bgcolor="#FAFCFF",
                              border_radius=8,
                          ),
                        ],
                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
            ),
            bgcolor=ft.Colors.GREY_100,
            border_radius=ft.border_radius.all(8),
            padding=ft.padding.symmetric(horizontal=20, vertical=10),
            margin=ft.margin.only(top=10),
            expand=True,
            *args,
            **kwargs,
        )

    def _build_values_box(self) -> list[ft.Control]:
        """Builds the value boxes for each variable."""
        return [
            ValueBox(
                page=self._page,
                value=variable.value,
                name=variable.name,
                has_plus_icon=variable_index < len(self._constraint.variables) - 1,  # Add plus icon except for the last variable
                on_change_value=self._on_change_value,
            ) for variable_index, variable in enumerate(self._constraint.variables)
        ]

    def _on_change_value(self, value: float, variable_name: str):
        """Handles the change of value in the ValueBox."""
        # Find the variable in the constraint and update its value
        if self._on_change_variable_value_callback:
            self._on_change_variable_value_callback(value, variable_name)
        
        # Optionally, you can trigger a re-render or update the page
        self._page.update()

    def _on_change_constraint_value(self, e: ft.ControlEvent):
        """Handles the change event of the constraint value."""
        if self._on_change_constraint_value_callback is not None:
            self._on_change_constraint_value_callback(e.control.value)

        self.update()
        self._page.update()

    def _on_change_constraint_symbol(self, e: ft.ControlEvent):
        """Handles the change event of the constraint symbol."""
        if self._on_change_constraint_symbol_callback is not None:
            self._on_change_constraint_symbol_callback(e.control.value)
        
        self.update()
        self._page.update()
        