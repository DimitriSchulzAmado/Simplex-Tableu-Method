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

    # ALTERAÇÃO: CRIAÇÃO DO PLACEHOLDER DINÂMICO PARA RESULTADOS
    results_placeholder = ft.Container(
        padding=ft.padding.symmetric(horizontal=20, vertical=64),
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

    # Modificação: Criação do container global de resultados para atualização dinâmica
    # Modificação: Container global de resultados com estilização desejada e placeholder dinâmico
    result_container = ft.Container(
        content=ft.Column(
            controls=[
                # Cabeçalho "Resultados"
                ft.Container(
                    content=ft.Row(
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
                # Texto descritivo
                ft.Text(
                    "Os resultados aparecerão aqui após resolver o problema.",
                    theme_style=ft.TextThemeStyle.BODY_MEDIUM,
                    color=ft.Colors.GREY_700,
                    size=16,
                ),
                # ALTERAÇÃO: USA PLACEHOLDER DINÂMICO EM VEZ DO CONTAINER ESTÁTICO
                results_placeholder,
            ]
        ),
        padding=ft.padding.symmetric(horizontal=20, vertical=30),
        bgcolor=ft.Colors.WHITE,
        border_radius=ft.border_radius.all(4),
        margin=ft.margin.only(top=20),
        expand=True,
    )


    async def on_solve_click(e):
        """Callback para resolver o problema quando o botão é clicado."""
        # ALTERAÇÃO: EXIBE ANIMAÇÃO DE LOADING NO PLACEHOLDER
        results_placeholder.content.controls = [
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
        # 1) Cards de status e valor ótimo com tons de verde claro
        cards = ft.Row(
            spacing=20,
            controls=[
                ft.Card(
                    content=ft.Container(
                        padding=ft.padding.all(16),
                        bgcolor=ft.Colors.GREEN_100,              # FUNDO VERDE CLARO
                        border_radius=ft.border_radius.all(8),
                        content=ft.Column(
                            [
                                ft.Text("Status", weight=ft.FontWeight.BOLD, color=ft.Colors.GREEN_900),
                                ft.Text(solution["status"], color=ft.Colors.GREEN_800, size=20),
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                        ),
                    ),
                    elevation=2,
                    shape=ft.RoundedRectangleBorder(radius=8),
                ),
                ft.Card(
                    content=ft.Container(
                        padding=ft.padding.all(16),
                        bgcolor=ft.Colors.GREEN_100,
                        border_radius=ft.border_radius.all(8),
                        content=ft.Column(
                            [
                                ft.Text("Valor Ótimo", weight=ft.FontWeight.BOLD, color=ft.Colors.GREEN_900),
                                ft.Text(f"{solution['objective_value']:.2f}", color=ft.Colors.GREEN_800, size=20),
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                        ),
                    ),
                    elevation=2,
                    shape=ft.RoundedRectangleBorder(radius=8),
                ),
            ]
        )

        # 2) Tabela de variáveis com alto contraste e tons de verde
        table = ft.DataTable(
            columns=[
                ft.DataColumn(label=ft.Text("Variável", weight=ft.FontWeight.BOLD, color=ft.Colors.GREEN_900)),
                ft.DataColumn(label=ft.Text("Valor",     weight=ft.FontWeight.BOLD, color=ft.Colors.GREEN_900)),
            ],
            rows=[
                ft.DataRow(cells=[
                    ft.DataCell(ft.Text(name, color=ft.Colors.BLACK, weight=ft.FontWeight.BOLD)),
                    ft.DataCell(ft.Text(f"{value:.2f}", color=ft.Colors.GREEN_800, weight=ft.FontWeight.BOLD)),
                ])
                for name, value in solution["variables"].items()
            ],
            border=ft.border.all(1, ft.Colors.GREEN_300),                   # BORDA VERDE
            heading_row_color=ft.Colors.GREEN_200,                          # FUNDO DO CABEÇALHO
            data_row_color=lambda i: (ft.Colors.WHITE if i % 2 == 0 else ft.Colors.GREEN_50),
        )

        # 3) Divider em verde suave
        divider = ft.Divider(thickness=1, color=ft.Colors.GREEN_300)

        # 4) Título da seção em verde escuro
        section_title = ft.Text(
            "Valores das Variáveis:",
            weight=ft.FontWeight.BOLD,
            size=16,
            color=ft.Colors.GREEN_900,
        )

        # 5) Atualiza o placeholder
        results_placeholder.content.controls = [
            cards,
            divider,
            section_title,
            table,
        ]

        # Adicionando análise detalhada dos preços-sombra com limites de variação
        detailed_shadow_analysis = simplex_tableau.get_detailed_shadow_price_analysis()
        if detailed_shadow_analysis:
            # Criando tabela detalhada com informações de variação
            detailed_shadow_rows = []
            constraint_index = 0
            for constraint_name, analysis in detailed_shadow_analysis.items():
                if constraint_index < len(app_state.objective_function.constraints):
                    display_name = app_state.objective_function.constraints[constraint_index].name
                else:
                    display_name = constraint_name
                
                # Formatação segura para evitar erros com valores None e melhorar precisão
                shadow_price = analysis.get('shadow_price', 0) or 0
                original_rhs = analysis.get('original_rhs', 0) or 0
                max_increase = analysis.get('max_increase', 0) or 0
                max_decrease = analysis.get('max_decrease', 0) or 0
                valid_range_min = analysis.get('valid_range_min', 0) or 0
                valid_range_max = analysis.get('valid_range_max', 0) or 0
                
                if abs(shadow_price) < 1e-6:
                    shadow_price = 0.0
                
                detailed_shadow_rows.append(
                    ft.DataRow(cells=[
                        ft.DataCell(ft.Text(display_name, color=ft.Colors.BLACK, weight=ft.FontWeight.BOLD)),
                        ft.DataCell(ft.Text(f"{shadow_price:.3f}", color=ft.Colors.BLUE_800, weight=ft.FontWeight.BOLD)),
                        ft.DataCell(ft.Text(f"{original_rhs:.1f}", color=ft.Colors.GREY_700)),
                        ft.DataCell(ft.Text(f"+{max_increase:.1f}", color=ft.Colors.GREEN_700, weight=ft.FontWeight.BOLD)),
                        ft.DataCell(ft.Text(f"-{max_decrease:.1f}", color=ft.Colors.RED_700, weight=ft.FontWeight.BOLD)),
                        ft.DataCell(ft.Text(f"[{valid_range_min:.1f}, {valid_range_max:.1f}]", 
                                          color=ft.Colors.ORANGE_700, size=12)),
                    ])
                )
                constraint_index += 1
                
            results_placeholder.content.controls.extend([
                ft.Divider(thickness=1, color=ft.Colors.BLUE_300),
                ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Row(
                                controls=[
                                    ft.Icon(name=ft.Icons.INSIGHTS, color=ft.Colors.BLUE_700, size=24),
                                    ft.Text(
                                        "Análise de Sensibilidade - Preços-Sombra e Variação Permitida:",
                                        weight=ft.FontWeight.BOLD,
                                        size=16,
                                        color=ft.Colors.BLUE_900,
                                    ),
                                ]
                            ),
                            ft.Text(
                                "Esta tabela mostra o impacto de mudanças nos recursos disponíveis:",
                                color=ft.Colors.GREY_700,
                                size=14,
                                italic=True,
                            ),
                        ]
                    ),
                    margin=ft.margin.only(bottom=16),
                ),
                ft.DataTable(
                    columns=[
                        ft.DataColumn(label=ft.Text("Restrição", weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_900)),
                        ft.DataColumn(label=ft.Text("Preço-Sombra", weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_900, 
                                                   tooltip="Valor por unidade adicional de recurso")),
                        ft.DataColumn(label=ft.Text("Valor Atual", weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_900)),
                        ft.DataColumn(label=ft.Text("Máx Aumento", weight=ft.FontWeight.BOLD, color=ft.Colors.GREEN_800,
                                                   tooltip="Máximo que pode aumentar mantendo viabilidade")),
                        ft.DataColumn(label=ft.Text("Máx Redução", weight=ft.FontWeight.BOLD, color=ft.Colors.RED_800,
                                                   tooltip="Máximo que pode diminuir mantendo viabilidade")),
                        ft.DataColumn(label=ft.Text("Faixa Válida", weight=ft.FontWeight.BOLD, color=ft.Colors.ORANGE_800,
                                                   tooltip="Intervalo onde o preço-sombra permanece válido")),
                    ],
                    rows=detailed_shadow_rows,
                    border=ft.border.all(1, ft.Colors.BLUE_300),
                    heading_row_color=ft.Colors.BLUE_200,
                    data_row_color=lambda i: (ft.Colors.WHITE if i % 2 == 0 else ft.Colors.BLUE_50),
                    border_radius=ft.border_radius.all(8),
                ),
            ])

        # Controles para análise de mudança de disponibilidade
        availability_change_checkbox = ft.Checkbox(
            label="Alterar Disponibilidade de Recursos?",
            value=False,
            label_style=ft.TextStyle(
                size=16,
                color=ft.Colors.PURPLE_900,
                weight=ft.FontWeight.BOLD,
            ),
        )

        # Container para os campos de alteração de disponibilidade (inicialmente oculto)
        availability_analysis_container = ft.Container(
            visible=False,
            content=ft.Column(
            controls=[
                ft.Text(
                "Novos Valores de Disponibilidade (Lado Direito):",
                theme_style=ft.TextThemeStyle.BODY_LARGE,
                size=16,
                color=ft.Colors.PURPLE_900,
                weight=ft.FontWeight.BOLD,
                ),
                ft.Text(
                "Altere os valores do lado direito das restrições:",
                theme_style=ft.TextThemeStyle.BODY_MEDIUM,
                color=ft.Colors.GREY_700,
                size=14,
                ),
            ]
            ),
            padding=ft.padding.symmetric(horizontal=20, vertical=16),
            bgcolor=ft.Colors.PURPLE_50,
            border_radius=ft.border_radius.all(8),
            margin=ft.margin.only(top=16),
        )

        # Função auxiliar para remover análises anteriores
        def remove_previous_analysis():
            """Remove análises anteriores de mudança de disponibilidade."""
            controls_to_remove = []
            
            for i, control in enumerate(results_placeholder.content.controls):
                should_remove = False
                
                # Verifica se tem atributo especial de análise
                if hasattr(control, '_is_analysis_element'):
                    should_remove = True
                
                # Fallback: Divider grosso
                elif (isinstance(control, ft.Divider) and
                      hasattr(control, 'thickness') and
                      control.thickness >= 2):
                    should_remove = True
                
                # Fallback: Procurar por texto específico
                elif isinstance(control, ft.Container):
                    try:
                        content = control.content
                        if hasattr(content, 'controls'):
                            for inner in content.controls:
                                if isinstance(inner, ft.Row):
                                    for item in inner.controls:
                                        if (isinstance(item, ft.Text) and
                                            hasattr(item, 'value') and
                                            item.value and
                                            "Análise de Mudança" in item.value):
                                            should_remove = True
                                            break
                                if should_remove:
                                    break
                    except (AttributeError, TypeError):
                        pass
                
                if should_remove:
                    controls_to_remove.append(i)
            
            # Remover elementos (do maior para menor índice)
            for index in sorted(controls_to_remove, reverse=True):
                if index < len(results_placeholder.content.controls):
                    results_placeholder.content.controls.pop(index)
            
            return len(controls_to_remove) > 0

        # Função para analisar mudança de disponibilidade
        def analyze_availability_change():
            """Analisa as mudanças de disponibilidade e atualiza os resultados."""
            try:
                remove_previous_analysis()
                
                # Obter os novos valores dos campos de entrada
                new_values = []
                changes_summary = []
                for field in availability_analysis_container.availability_fields:
                    try:
                        value = float(field.value)
                        new_values.append(value)
                        constraint_index = field.constraint_index
                        original_value = app_state.objective_function.constraints[constraint_index].value
                        constraint_name = app_state.objective_function.constraints[constraint_index].name
                        changes_summary.append({
                            "name": constraint_name,
                            "original": original_value,
                            "new": value,
                            "change": value - original_value
                        })
                    except ValueError:
                        # Se não conseguir converter, usa o valor original
                        constraint_index = field.constraint_index
                        original_value = app_state.objective_function.constraints[constraint_index].value
                        new_values.append(original_value)
                        constraint_name = app_state.objective_function.constraints[constraint_index].name
                        changes_summary.append({
                            "name": constraint_name,
                            "original": original_value,
                            "new": original_value,
                            "change": 0
                        })

                # Usar o método de análise de disponibilidade existente
                availability_analysis = simplex_tableau.analyze_resource_availability_change(new_values)

                # Cores e status baseados na viabilidade
                if availability_analysis["is_viable"]:
                    status_color = ft.Colors.GREEN_800
                    status_text = "✓ Viável"
                    status_bg = ft.Colors.GREEN_100
                    icon = ft.Icons.CHECK_CIRCLE
                else:
                    status_color = ft.Colors.RED_800
                    status_text = "✗ Não Viável"
                    status_bg = ft.Colors.RED_100
                    icon = ft.Icons.ERROR

                # Criar cards visuais para o resultado
                status_card = ft.Card(
                    content=ft.Container(
                        padding=ft.padding.all(20),
                        bgcolor=status_bg,
                        content=ft.Row(
                            controls=[
                                ft.Icon(name=icon, color=status_color, size=32),
                                ft.Column(
                                    controls=[
                                        ft.Text(
                                            "Status da Análise",
                                            weight=ft.FontWeight.BOLD,
                                            color=status_color,
                                            size=14,
                                        ),
                                        ft.Text(
                                            status_text,
                                            weight=ft.FontWeight.BOLD,
                                            color=status_color,
                                            size=18,
                                        ),
                                    ],
                                    expand=True,
                                ),
                            ],
                        ),
                    ),
                    elevation=3,
                )

                # Card de comparação de lucros
                profit_card = ft.Card(
                    content=ft.Container(
                        padding=ft.padding.all(20),
                        bgcolor=ft.Colors.BLUE_50,
                        content=ft.Column(
                            controls=[
                                ft.Text(
                                    "Comparação de Lucros",
                                    weight=ft.FontWeight.BOLD,
                                    color=ft.Colors.BLUE_900,
                                    size=16,
                                ),
                                ft.Row(
                                    controls=[
                                        ft.Column(
                                            controls=[
                                                ft.Text("Lucro Original:", color=ft.Colors.BLUE_700, size=12),
                                                ft.Text(f"{availability_analysis['original_optimal_value']:.2f}", 
                                                       color=ft.Colors.BLUE_800, weight=ft.FontWeight.BOLD, size=16),
                                            ],
                                            expand=True,
                                        ),
                                        ft.Container(
                                            content=ft.Icon(name=ft.Icons.ARROW_FORWARD, color=ft.Colors.BLUE_600),
                                            alignment=ft.alignment.center,
                                        ),
                                        ft.Column(
                                            controls=[
                                                ft.Text("Novo Lucro:", color=ft.Colors.GREEN_700, size=12),
                                                ft.Text(
                                                    f"{availability_analysis['new_optimal_value']:.2f}" if availability_analysis["new_optimal_value"] is not None else "N/A",
                                                    color=ft.Colors.GREEN_800 if availability_analysis["new_optimal_value"] is not None else ft.Colors.RED_800,
                                                    weight=ft.FontWeight.BOLD,
                                                    size=16,
                                                ),
                                            ],
                                            expand=True,
                                        ),
                                    ],
                                ),
                                # Diferença
                                ft.Container(
                                    content=ft.Text(
                                        f"Diferença: {availability_analysis['new_optimal_value'] - availability_analysis['original_optimal_value']:.2f}"
                                        if availability_analysis["new_optimal_value"] is not None
                                        else "Diferença: Não calculável",
                                        color=ft.Colors.PURPLE_800,
                                        weight=ft.FontWeight.BOLD,
                                        size=14,
                                    ),
                                    bgcolor=ft.Colors.PURPLE_100,
                                    padding=ft.padding.all(8),
                                    border_radius=ft.border_radius.all(6),
                                    alignment=ft.alignment.center,
                                    margin=ft.margin.only(top=12),
                                ),
                            ],
                        ),
                    ),
                    elevation=3,
                )

                # Tabela de mudanças detalhadas
                changes_table = ft.DataTable(
                    columns=[
                        ft.DataColumn(label=ft.Text("Restrição", weight=ft.FontWeight.BOLD, color=ft.Colors.PURPLE_900)),
                        ft.DataColumn(label=ft.Text("Valor Original", weight=ft.FontWeight.BOLD, color=ft.Colors.PURPLE_900)),
                        ft.DataColumn(label=ft.Text("Novo Valor", weight=ft.FontWeight.BOLD, color=ft.Colors.PURPLE_900)),
                        ft.DataColumn(label=ft.Text("Variação", weight=ft.FontWeight.BOLD, color=ft.Colors.PURPLE_900)),
                    ],
                    rows=[
                        ft.DataRow(cells=[
                            ft.DataCell(ft.Text(change["name"], color=ft.Colors.BLACK, weight=ft.FontWeight.BOLD)),
                            ft.DataCell(ft.Text(f"{change['original']:.2f}", color=ft.Colors.GREY_700)),
                            ft.DataCell(ft.Text(f"{change['new']:.2f}", color=ft.Colors.BLUE_800)),
                            ft.DataCell(ft.Text(
                                f"{change['change']:+.2f}",
                                color=ft.Colors.GREEN_700 if change['change'] >= 0 else ft.Colors.RED_700,
                                weight=ft.FontWeight.BOLD,
                            )),
                        ])
                        for change in changes_summary
                    ],
                    border=ft.border.all(1, ft.Colors.PURPLE_300),
                    heading_row_color=ft.Colors.PURPLE_200,
                    data_row_color=lambda i: (ft.Colors.WHITE if i % 2 == 0 else ft.Colors.PURPLE_50),
                    border_radius=ft.border_radius.all(8),
                )

                # Criar elementos de resultado da análise
                divider = ft.Divider(thickness=2, color=ft.Colors.PURPLE_300)
                divider._is_analysis_element = True
                
                title_container = ft.Container(
                    content=ft.Row(
                        controls=[
                            ft.Icon(name=ft.Icons.SCIENCE, 
                                   color=ft.Colors.PURPLE_700, size=28),
                            ft.Text(
                                "Análise de Mudança de Disponibilidade",
                                weight=ft.FontWeight.BOLD,
                                size=18,
                                color=ft.Colors.PURPLE_900,
                            ),
                        ],
                    ),
                    margin=ft.margin.only(bottom=16),
                )
                title_container._is_analysis_element = True
                
                cards_row = ft.Row(
                    controls=[status_card, profit_card],
                    spacing=16,
                )
                cards_row._is_analysis_element = True
                
                spacer = ft.Container(height=16)
                spacer._is_analysis_element = True
                
                details_text = ft.Text(
                    "Detalhes das Mudanças:",
                    weight=ft.FontWeight.BOLD,
                    size=16,
                    color=ft.Colors.PURPLE_900,
                )
                details_text._is_analysis_element = True
                
                changes_table._is_analysis_element = True
                
                analysis_results = [
                    divider,
                    title_container,
                    cards_row,
                    spacer,
                    details_text,
                    changes_table,
                ]

                # Remover análises anteriores se existirem
                remove_previous_analysis()

                # Adicionar novos resultados
                results_placeholder.content.controls.extend(analysis_results)
                result_container.update()

            except Exception as e:
                print(f"Erro na análise de disponibilidade: {e}")
                # Remover análises anteriores primeiro
                remove_previous_analysis()
                
                # Exibir erro na interface
                error_message = ft.Container(
                    content=ft.Row(
                        controls=[
                            ft.Icon(name=ft.Icons.ERROR, 
                                   color=ft.Colors.RED_700),
                            ft.Text(f"Erro na análise: {str(e)}", 
                                   color=ft.Colors.RED_700),
                        ],
                    ),
                    bgcolor=ft.Colors.RED_100,
                    padding=ft.padding.all(16),
                    border_radius=ft.border_radius.all(8),
                )
                error_message._is_analysis_element = True
                results_placeholder.content.controls.append(error_message)
                result_container.update()

        # Botão para executar a análise
        analyze_button = ft.ElevatedButton(
            text="Analisar Mudança",
            height=40,
            icon=ft.Icons.ANALYTICS,
            color=ft.Colors.WHITE,
            bgcolor=ft.Colors.PURPLE_700,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=8),
                text_style=ft.TextStyle(
                    size=14,
                    color=ft.Colors.WHITE,
                ),
            ),
            on_click=lambda e: analyze_availability_change(),
        )

        def on_change_availability_checkbox_analysis(e):
            """Callback para mostrar/ocultar os controles de análise de disponibilidade."""
            availability_analysis_container.visible = e.control.value
            
            if e.control.value:
                # Criar campos de entrada para cada restrição
                availability_fields = []
                for i, constraint in enumerate(app_state.objective_function.constraints):
                    field = ft.TextField(
                        label=f"Nova disponibilidade para {constraint.name}",
                        value=str(constraint.value),
                        hint_text=f"Valor atual: {constraint.value}",
                        width=250,
                        height=50,
                        border_color=ft.Colors.PURPLE_300,
                        focused_border_color=ft.Colors.PURPLE_700,
                        text_style=ft.TextStyle(size=14, color=ft.Colors.BLACK),
                        label_style=ft.TextStyle(color=ft.Colors.PURPLE_800),
                    )
                    field.constraint_index = i  # Adicionar índice para identificação
                    availability_fields.append(field)
                
                # Adicionar os campos ao container
                fields_row = ft.Row(
                    controls=availability_fields,
                    wrap=True,
                    spacing=16,
                    run_spacing=8,
                )
                
                availability_analysis_container.content.controls.extend([fields_row, analyze_button])
                
                # Armazenar referência aos campos para uso posterior
                availability_analysis_container.availability_fields = availability_fields
            else:
                # Remover campos e botão quando desmarcado
                if len(availability_analysis_container.content.controls) > 2:
                    availability_analysis_container.content.controls = availability_analysis_container.content.controls[:2]
                
                # Remover análises anteriores dos resultados
                remove_previous_analysis()
                result_container.update()
            
            availability_analysis_container.update()

        availability_change_checkbox.on_change = on_change_availability_checkbox_analysis

        # Adicionar o checkbox e container aos resultados
        results_placeholder.content.controls.extend([
            ft.Divider(thickness=1, color=ft.Colors.GREY_300),
            availability_change_checkbox,
            availability_analysis_container,
        ])

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
