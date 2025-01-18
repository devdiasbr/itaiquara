import flet as ft

def create_dropdown(
    label: str,
    hint_text: str = None,
    width: int = 400,
    height: int = 55,
    on_change=None
) -> ft.Dropdown:
    """
    Cria um dropdown padronizado com estilo consistente.
    Parâmetros:
        label: Texto do label do dropdown
        hint_text: Texto de dica
        width: Largura do dropdown (padrão 400px)
        height: Altura do dropdown (padrão 55px)
        on_change: Função callback para mudança de valor
    """
    return ft.Dropdown(
        label=label,
        hint_text=hint_text,
        width=width,
        height=height,
        filled=True,
        bgcolor="white",
        border_color="#2196F3",
        focused_border_color="#FF0000",
        color="#000000",
        label_style=ft.TextStyle(color="#000000", weight=ft.FontWeight.BOLD),
        text_style=ft.TextStyle(color="#000000", size=11, weight=ft.FontWeight.BOLD),
        content_padding=10,
        on_change=on_change,
    )
