import flet as ft
import asyncio  # Modificação: import para usar asyncio.sleep no callback de loading

from components.header import Header
from components.value_box import ValueBox
from components.variables_controls import VariablesControls
from components.constraint_values import ConstraintValues

from data.app_state import app_state, ObjectiveFunctionType, Variable, ConstraintSymbol
from methods.simplex_tableu import SimplexTableau


def on_variable_change(value: float, name: str):
    """Callback para atualizar o valor de uma variável."""
    app_state.objective_function.update_variable(name, value)

def on_constraint_variable_change(value: float, name: str, constraint_name: str):
    """Callback para atualizar o valor de uma variável de restrição."""
    app_state.objective_function.update_constraint_variable(
        constraint_name, Variable(name=name, value=value)
    )

def on_constraint_symbol_change(symbol: ConstraintSymbol, constraint_name: str):
    """Callback para atualizar o símbolo de uma restrição."""
    app_state.objective_function.update_contraint_symbol(
        constraint_name, symbol
    )

def on_constraint_value_change(value: float, constraint_name: str):
    """Callback para atualizar o valor de uma restrição."""
    app_state.objective_function.update_constraint_value(
        constraint_name, value
    )


def main(page: ft.Page):
    page.window.always_on_top = True
    page.title = "Simplex Solver"

    # page.window.opacity = .9
    page.horizontal_alignment = ft.CrossAxisAlignment.STRETCH

    page.padding = ft.padding.all(0)
    page.bgcolor = ft.Colors.GREY_200
    page.window.bgcolor = ft.Colors.GREY_200
    page.window.min_width = 1000

    page.scroll = ft.ScrollMode.AUTO

    header = Header.build()
    objective_function_items: list[ValueBox] = [
        ValueBox(page, variable.value, variable.name, 
                    has_plus_icon=variable_index < app_state.objective_function.quantity_of_variables - 1, on_change_value=on_variable_change)
        for variable_index, variable in enumerate(app_state.objective_function.variables)
    ]

    objective_function_row = ft.Row(
        wrap=True,
        spacing=8,         # espaço horizontal entre controles
        run_spacing=8,     # espaço vertical entre "linhas"
        alignment=ft.MainAxisAlignment.START,
        run_alignment=ft.MainAxisAlignment.START,
        controls=objective_function_items,
    )

    def update_objective_function_items():
        """Atualiza os itens da função objetivo com base no estado atual."""
        nonlocal objective_function_items, objective_function_row
        objective_function_items = [
            ValueBox(page, variable.value, variable.name, 
                        has_plus_icon=variable_index < app_state.objective_function.quantity_of_variables - 1, on_change_value=on_variable_change)
            for variable_index, variable in enumerate(app_state.objective_function.variables)
        ]

        objective_function_row.controls = objective_function_items
        objective_function_row.update()
        page.update()

    constraint_items = [
        ConstraintValues(
            page, 
            constraint,
            on_change_variable_value=on_constraint_variable_change,
            on_change_constraint_value=on_constraint_value_change,
            on_change_constraint_symbol=on_constraint_symbol_change,
        ) for constraint in app_state.objective_function.constraints
    ]

    constraint_items_column = ft.Column(
        controls=constraint_items,
        spacing=8,         # espaço horizontal entre controles
    )

    def update_constraint_items():
        """Atualiza os itens de restrição com base no estado atual."""
        nonlocal constraint_items
        constraint_items = [
            ConstraintValues(
                page, 
                constraint,
                on_change_variable_value=on_constraint_variable_change,
                on_change_constraint_value=on_constraint_value_change,
                on_change_constraint_symbol=on_constraint_symbol_change,
            ) for constraint in app_state.objective_function.constraints
        ]

        constraint_items_column.controls = constraint_items
        constraint_items_column.update()
        page.update()

    app_state.subscribe(update_objective_function_items, "objective_function")
    app_state.subscribe(update_constraint_items, "constraint")

    simplex_tableau = SimplexTableau()

    # Modificação: Criação do container global de resultados para atualização dinâmica
    result_container = ft.Column(
        controls=[
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
            )
        ]
    )

    async def on_solve_click(e):
        """Callback para resolver o problema quando o botão é clicado."""
        # Modificação: exibe animação de loading
        result_container.controls = [
            ft.Row(
                alignment=ft.MainAxisAlignment.CENTER,
                controls=[
                    ft.ProgressRing(color=ft.Colors.BLUE_700),
                    ft.Text("Resolvendo o problema...", size=16, color=ft.Colors.GREY_800),
                ],
            )
        ]
        result_container.update()
        await asyncio.sleep(0.1)  # Modificação: pausa para renderizar o loading

        # Aqui você pode chamar a lógica de resolução do problema
        print("Resolver o problema", app_state.objective_function.variables, app_state.objective_function.constraints)
        simplex_tableau.build(app_state.objective_function)
        simplex_tableau.solve()
        solution = simplex_tableau.get_solution()

        # Modificação: atualiza container com resultados
        result_controls = [
            ft.Text(f"Status: {solution['status']}", weight=ft.FontWeight.BOLD, size=18),
            ft.Text(f"Valor ótimo da função objetivo: {solution['objective_value']:.2f}", size=16),
            ft.Text("Valores das variáveis:", size=16, weight=ft.FontWeight.BOLD),
        ] + [
            ft.Text(f"{name} = {value:.2f}", size=15) for name, value in solution["variables"].items()
        ]
        result_container.controls = result_controls
        result_container.update()

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
                                                            VariablesControls(
                                                                page, 
                                                                "Variável",
                                                                on_change_value=app_state.set_quantity_of_variables,
                                                            ),
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
                                                            VariablesControls(
                                                                page, 
                                                                "Restrição",
                                                                on_change_value=app_state.set_quantity_of_constraints,
                                                            ),
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
                                                                    value=ObjectiveFunctionType.MAXIMIZE.value,
                                                                    active_color=ft.Colors.BLUE_700,
                                                                    label_style=ft.TextStyle(
                                                                        color=ft.Colors.GREY_800,
                                                                        size=14,
                                                                        weight=ft.FontWeight.NORMAL,
                                                                    ),
                                                                ),
                                                                ft.Radio(
                                                                    label="Minimizar",
                                                                    value=ObjectiveFunctionType.MINIMIZE.value,
                                                                    active_color=ft.Colors.BLUE_700,
                                                                    label_style=ft.TextStyle(
                                                                        color=ft.Colors.GREY_800,
                                                                        size=14,
                                                                        weight=ft.FontWeight.NORMAL,
                                                                    ),
                                                                ),
                                                            ]
                                                        ),
                                                        on_change=lambda e: app_state.objective_function.set_objective_function(
                                                            e.control.value
                                                        ),
                                                        value=app_state.objective_function.objective_function.value,
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
                                                        objective_function_row,
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
                                constraint_items_column,
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
                                                on_click=on_solve_click,  # Modificação: usa callback async com loading
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
                    # Modificação: substitui container estático de resultados pelo result_container dinâmico
                    result_container
                ]
            )
        )
    )

    page.update()


if __name__ == "__main__":
    ft.app(target=main)