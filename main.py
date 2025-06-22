import flet as ft

from components.header import Header
from components.value_box import ValueBox

from data.app_state import app_state
from events.variables_and_constraint_event import VariablesAndConstraintEvent, TextEnum


def main(page: ft.Page):
    # page.window.always_on_top = True
    page.title = "Simplex Solver"

    # page.window.opacity = .9
    page.horizontal_alignment = ft.CrossAxisAlignment.STRETCH

    page.padding = ft.padding.all(0)
    page.bgcolor = ft.Colors.GREY_200
    page.window.bgcolor = ft.Colors.GREY_200
    page.window.min_width = 1000

    page.scroll = ft.ScrollMode.AUTO

    variable_label = ft.Text(
        f"{app_state.objective_function.quantity_of_variables} Variaveis",
        theme_style=ft.TextThemeStyle.BODY_MEDIUM,
        color=ft.Colors.GREY_800,
        text_align=ft.TextAlign.CENTER,
    )

    constraint_label = ft.Text(
        f"{app_state.objective_function.quantity_of_constraints} Restrições",
        theme_style=ft.TextThemeStyle.BODY_MEDIUM,
        color=ft.Colors.GREY_800,
        text_align=ft.TextAlign.CENTER,
    )

    variables_and_constraint_event = VariablesAndConstraintEvent(page, {
        TextEnum.VARIABLE_LABEL: variable_label,
        TextEnum.CONSTRAINT_LABEL: constraint_label,
    })

    header = Header.build()

    page.add(
        ft.Container(
            padding=ft.padding.all(20),
            content=ft.Column(
                expand=True,
                horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
                controls=[
                    header,
                    ft.Container(
                        content=ft.Column(
                            controls=[
                                ft.Container(
                                    margin=ft.margin.only(bottom=20),
                                    content=ft.Row(
                                        controls=[
                                            ft.Icon(
                                                name=ft.Icons.LIGHTBULB_OUTLINE_ROUNDED,
                                                color=ft.Colors.YELLOW_700,
                                            ),
                                            ft.Text(
                                                "Configuração do Problema",
                                                theme_style=ft.TextThemeStyle.TITLE_LARGE,
                                                color=ft.Colors.BLACK,
                                            )
                                        ]
                                    )
                                ),
                                ft.Container(
                                    content=ft.Column(
                                        spacing=32,
                                        controls=[
                                            ft.Column(
                                                controls=[
                                                    ft.Column(
                                                        controls=[
                                                            ft.Text(
                                                                "Variáveis de Decisão",
                                                                theme_style=ft.TextThemeStyle.BODY_LARGE,
                                                                size=20,
                                                                color=ft.Colors.BLACK,
                                                            ),
                                                            ft.Row(
                                                                controls=[
                                                                    ft.IconButton(
                                                                        icon=ft.Icons.REMOVE,
                                                                        tooltip="Diminuir Variável",
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
                                                                        on_click=variables_and_constraint_event.remove_variable
                                                                    ),
                                                                    ft.Container(
                                                                        content=variable_label,
                                                                        bgcolor=ft.Colors.GREY_200,
                                                                        border_radius=ft.border_radius.all(8),
                                                                        padding=ft.padding.symmetric(horizontal=20, vertical=10),
                                                                    ),
                                                                    ft.IconButton(
                                                                        icon=ft.Icons.ADD,
                                                                        tooltip="Aumentar Variável",
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
                                                                        on_click=variables_and_constraint_event.add_variable
                                                                    )
                                                                ]
                                                            )
                                                        ]
                                                    ),
                                                    ft.Column(
                                                        controls=[
                                                            ft.Text(
                                                                "Restrições",
                                                                theme_style=ft.TextThemeStyle.BODY_LARGE,
                                                                size=20,
                                                                color=ft.Colors.BLACK,
                                                            ),
                                                            ft.Row(
                                                                controls=[
                                                                    ft.IconButton(
                                                                        icon=ft.Icons.REMOVE,
                                                                        tooltip="Diminuir Restrição",
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
                                                                        on_click=variables_and_constraint_event.remove_constraint
                                                                    ),
                                                                    ft.Container(
                                                                        content=constraint_label,
                                                                        bgcolor=ft.Colors.GREY_200,
                                                                        border_radius=ft.border_radius.all(8),
                                                                        padding=ft.padding.symmetric(horizontal=20, vertical=10),
                                                                    ),
                                                                    ft.IconButton(
                                                                        icon=ft.Icons.ADD,
                                                                        tooltip="Aumentar restrições",
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
                                                                        on_click=variables_and_constraint_event.add_constraint
                                                                    )
                                                                ]
                                                            )
                                                        ]
                                                    ),
                                                ]
                                            ),
                                            ft.Column(
                                                spacing=4,
                                                controls=[
                                                    ft.Text(
                                                        "Objetivo",
                                                        theme_style=ft.TextThemeStyle.BODY_LARGE,
                                                        size=20,
                                                        color=ft.Colors.BLACK,
                                                    ),
                                                    ft.RadioGroup(
                                                        content=ft.Row(
                                                            controls=[
                                                                ft.Radio(
                                                                    label="Maximizar",
                                                                    value="max",
                                                                    active_color=ft.Colors.BLUE_700,
                                                                    label_style=ft.TextStyle(
                                                                        color=ft.Colors.GREY_800,
                                                                        size=14,
                                                                        weight=ft.FontWeight.NORMAL,
                                                                    )
                                                                ),
                                                                ft.Radio(
                                                                    label="Minimizar",
                                                                    value="min",
                                                                    active_color=ft.Colors.BLUE_700,
                                                                    label_style=ft.TextStyle(
                                                                        color=ft.Colors.GREY_800,
                                                                        size=14,
                                                                        weight=ft.FontWeight.NORMAL,
                                                                    )
                                                                ),
                                                            ]
                                                        )
                                                    )
                                                ]
                                            ),
                                        ]
                                    )
                                ),
                                ft.Divider(
                                    color=ft.Colors.GREY_300,
                                    thickness=1,
                                    height=1,
                                ),
                                ft.Container(
                                    content=ft.Column(
                                        controls=[
                                            ft.Container(
                                                ft.Row(
                                                    controls=[
                                                        ft.Text(
                                                            "Função Objetivo",
                                                            theme_style=ft.TextThemeStyle.TITLE_LARGE,
                                                            color=ft.Colors.BLACK,
                                                        ),
                                                        ft.Icon(
                                                            name=ft.Icons.INFO_OUTLINE,
                                                            color=ft.Colors.GREY_600,
                                                            tooltip="A função objetivo é a equação que você deseja maximizar ou minimizar.",
                                                            size=20,
                                                        )
                                                    ]
                                                ),
                                            ),
                                            ft.Container(
                                                content=ft.Column(
                                                    controls=[
                                                        ft.Text(
                                                            "Maximizar Z =",
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
                                                                ValueBox(20, "x₁"),
                                                                ft.Text(
                                                                    "+",
                                                                    size=20,
                                                                    color=ft.Colors.GREY_800,
                                                                ),
                                                                ValueBox(30, "x₂"),
                                                                ft.Text(
                                                                    "+",
                                                                    size=20,
                                                                    color=ft.Colors.GREY_800,
                                                                ),
                                                                ValueBox(40, "x₃"),
                                                            ],
                                                        )
                                                    ],
                                                    horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
                                                ),
                                                bgcolor=ft.Colors.GREY_100,
                                                border_radius=ft.border_radius.all(8),
                                                padding=ft.padding.symmetric(horizontal=20, vertical=10),
                                                margin=ft.margin.only(top=10),
                                                expand=True,
                                            )
                                        ]
                                    )
                                ),
                                ft.Container(
                                    ft.Divider(
                                        color=ft.Colors.GREY_300,
                                        thickness=1,
                                        height=1,
                                    ),
                                    margin=ft.margin.only(top=20, bottom=20),
                                ),
                                ft.Container(
                                    ft.Column(
                                        controls=[
                                            ft.Container(
                                                ft.Row(
                                                    controls=[
                                                        ft.Text(
                                                            "Restrições",
                                                            theme_style=ft.TextThemeStyle.TITLE_LARGE,
                                                            color=ft.Colors.BLACK,
                                                        ),
                                                        ft.Icon(
                                                            name=ft.Icons.INFO_OUTLINE,
                                                            color=ft.Colors.GREY_600,
                                                            tooltip="As restrições são as limitações ou condições que devem ser atendidas no problema.",
                                                            size=20,
                                                        )
                                                    ]
                                                ),
                                            ),
                                        ],
                                    ),
                                ),
                                ft.Container(
                                    ft.Column(
                                        controls=[
                                            ft.Text(
                                                "Restrição 1",
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
                                                    ValueBox(10, "x₁"),
                                                    ft.Text(
                                                        "+",
                                                        size=20,
                                                        color=ft.Colors.GREY_800,
                                                    ),
                                                    ValueBox(5, "x₂"),
                                                    ft.Text(
                                                        "<=",
                                                        size=20,
                                                        color=ft.Colors.GREY_800,
                                                    ),
                                                    ValueBox(15, ""),
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
                                ),
                                ft.Container(
                                    ft.Column(
                                        controls=[
                                            ft.Text(
                                                "Restrição 2",
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
                                                    ValueBox(10, "x₁"),
                                                    ft.Text(
                                                        "+",
                                                        size=20,
                                                        color=ft.Colors.GREY_800,
                                                    ),
                                                    ValueBox(5, "x₂"),
                                                    ft.Text(
                                                        "<=",
                                                        size=20,
                                                        color=ft.Colors.GREY_800,
                                                    ),
                                                    ValueBox(15, ""),
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
                                ),
                                ft.Container(
                                    ft.Column(
                                        controls=[
                                            ft.Text(
                                                "Restrição 3",
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
                                                    ValueBox(10, "x₁"),
                                                    ft.Text(
                                                        "+",
                                                        size=20,
                                                        color=ft.Colors.GREY_800,
                                                    ),
                                                    ValueBox(5, "x₂"),
                                                    ft.Text(
                                                        "<=",
                                                        size=20,
                                                        color=ft.Colors.GREY_800,
                                                    ),
                                                    ValueBox(15, ""),
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
                                ),
                                ft.Container(
                                    ft.Column(
                                        controls=[
                                            ft.ElevatedButton(
                                                text="Resolver",
                                                height=64,
                                                icon=ft.Icons.EQUALIZER,
                                                color=ft.Colors.WHITE,
                                                bgcolor=ft.Colors.BLUE_700,
                                                style=ft.ButtonStyle(
                                                    shape=ft.RoundedRectangleBorder(radius=8),
                                                    padding=ft.padding.symmetric(horizontal=20, vertical=10),
                                                    text_style=ft.TextStyle(
                                                        size=20,
                                                        color=ft.Colors.WHITE,
                                                    ),
                                                ),
                                            ),
                                        ],
                                        horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
                                    ),
                                ),
                            ],
                        ),
                        bgcolor=ft.Colors.WHITE,
                        border_radius=ft.border_radius.all(4),
                        padding=ft.padding.symmetric(horizontal=20, vertical=30),
                    ),
                    ft.Container(
                        ft.Column(
                            controls=[
                                ft.Container(
                                    ft.Row(
                                        controls=[
                                            ft.Icon(
                                                name=ft.Icons.ANALYTICS_ROUNDED,
                                                color=ft.Colors.BLUE,
                                                tooltip="Os resultados mostram a solução ótima do problema e as variáveis de decisão.",
                                                size=32,
                                            ),
                                            ft.Text(
                                                "Resultados",
                                                theme_style=ft.TextThemeStyle.TITLE_LARGE,
                                                weight=ft.FontWeight.BOLD,
                                                color=ft.Colors.BLACK,
                                            ),
                                        ],
                                    ),
                                ),
                                ft.Text(
                                    "Os resultados aparecerão aqui após resolver o problema.",
                                    theme_style=ft.TextThemeStyle.BODY_MEDIUM,
                                    color=ft.Colors.GREY_700,
                                    size=16,
                                ),
                                ft.Container(
                                    padding=ft.padding.symmetric(horizontal=20, vertical=128),
                                    content=ft.Column(
                                        controls=[
                                            ft.Icon(
                                                name=ft.Icons.WORKSPACES,
                                                color=ft.Colors.GREY_300,
                                                size=44,
                                            ),
                                            ft.Text(
                                                "Configure o problema e clique em \"Resolver\"",
                                                theme_style=ft.TextThemeStyle.BODY_LARGE,
                                                color=ft.Colors.GREY_400,
                                                size=14,
                                                text_align=ft.TextAlign.CENTER,
                                            ),
                                        ],
                                        horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
                                    ),
                                ),
                            ],
                        ),
                        padding=ft.padding.symmetric(horizontal=20, vertical=30),
                        bgcolor=ft.Colors.WHITE,
                        border_radius=ft.border_radius.all(4),
                        margin=ft.margin.only(top=20),
                        expand=True,
                    ),
                ]
            )
        )
    )

    page.update()


if __name__ == "__main__":
    ft.app(target=main)