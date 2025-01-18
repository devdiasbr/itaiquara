import flet as ft

def create_loading_view(page: ft.Page = None):
    return ft.Container(
        content=ft.Column(
            [
                ft.Text(
                    "GERADOR DE CONTRATOS",
                    size=40,
                    weight=ft.FontWeight.BOLD,
                    text_align=ft.TextAlign.CENTER,
                    color="#2196F3",
                ),
                ft.Container(height=20),  # Espaçamento
                ft.ProgressRing(
                    width=64,
                    height=64,
                    stroke_width=4,
                    color="#2196F3",
                ),
                ft.Container(height=20),  # Espaçamento
                ft.Text(
                    "Carregando...",
                    size=20,
                    color="#2196F3",
                    text_align=ft.TextAlign.CENTER,
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
        ),
        alignment=ft.alignment.center,
        expand=True,
        padding=ft.padding.only(top=350),
    )

# Execução direta para debug
if __name__ == "__main__":
    def main(page: ft.Page):
        page.title = "Debug Loading"
        page.window_maximized = True
        page.padding = 0
        page.bgcolor = "#f0f0f0"
        
        # Stack para mostrar o loading em tela cheia
        loading_stack = ft.Stack(
            [
                ft.Container(
                    expand=True,
                    bgcolor="#f0f0f0",
                ),
                ft.Container(
                    content=create_loading_view(page),
                    alignment=ft.alignment.center,
                    expand=True,
                ),
            ],
            expand=True,
        )
        
        page.add(loading_stack)

    ft.app(target=main)