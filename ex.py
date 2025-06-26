import flet as ft

def main(page: ft.Page):
    # Badge do resultado ótimo
    badge = ft.Container(
        content=ft.Text("Resultado Ótimo: 156.80", color="#20613B", size=22, weight=ft.FontWeight.BOLD),
        bgcolor="#E1F7E9",
        border_radius=40,
        padding=ft.padding.symmetric(horizontal=36, vertical=12),
        alignment=ft.alignment.center,
        margin=ft.margin.only(bottom=32),
    )

    # Tabela de variáveis e valores
    columns = [
        ft.DataColumn(ft.Text("Variável", color="#858FA3", size=18, weight=ft.FontWeight.W_500)),
        ft.DataColumn(ft.Text("Valor Ótimo", color="#858FA3", size=18, weight=ft.FontWeight.W_500), numeric=True),
    ]

    rows = [
        ft.DataRow(
            cells=[
                ft.DataCell(ft.Text("X₁", color="#1B5EF7", size=18, spans=[ft.TextSpan("₁")], weight=ft.FontWeight.W_600)),
                ft.DataCell(ft.Text("6.780", color="#1A1B23", size=18, weight=ft.FontWeight.BOLD)),
            ]
        ),
        ft.DataRow(
            cells=[
                ft.DataCell(ft.Text("X₂", color="#1B5EF7", size=18, spans=[ft.TextSpan("₂")], weight=ft.FontWeight.W_600)),
                ft.DataCell(ft.Text("2.031", color="#1A1B23", size=18, weight=ft.FontWeight.BOLD)),
            ]
        ),
    ]

    # DataTable com borda inferior apenas no header (simulação)
    table = ft.Container(
        content=ft.DataTable(
            columns=columns,
            rows=rows,
            divider_thickness=0,    # remove divisórias entre linhas
            heading_row_color=None, # remove cor do header
            data_row_color=None,    # remove cor das linhas
            column_spacing=96,      # espaçamento entre colunas
            heading_row_height=56,
            data_row_min_height=52,
        ),
        border_radius=20,
        padding=ft.padding.symmetric(horizontal=36, vertical=8),
        bgcolor="#FFFFFF",
        margin=ft.margin.only(top=12),
        expand=True,
    )

    # Card externo com fundo verde claro e padding
    card = ft.Container(
        content=ft.Column(
            [
                # Título com ícone e texto grande
                ft.Row(
                    [
                        ft.Icon(name=ft.Icons.MILITARY_TECH_OUTLINED, color="#1C7A41", size=32),
                        ft.Text("Solução Ótima", size=32, weight=ft.FontWeight.BOLD, color="#0B1D15"),
                    ],
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=12,
                ),
                ft.Container(height=16),  # Espaço
                ft.Row(
                    [badge], alignment=ft.MainAxisAlignment.CENTER
                ),
                table,
            ],
            tight=True,
            spacing=0,
        ),
        padding=36,
        border_radius=24,
        bgcolor="#F4FFF8",
        margin=20,
        expand=True,
    )

    # Fim
    page.bgcolor = "#EAF2FF"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.add(card)

ft.app(target=main)
