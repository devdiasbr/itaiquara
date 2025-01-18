from pickle import TRUE
import flet as ft
import logging
from views.visualizar_view import create_visualizar_view
from views.incluir_view import create_incluir_view
from views.alterar_view import create_alterar_view
from views.excluir_view import create_excluir_view
from views.loading_view import create_loading_view
import asyncio

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

def main(page: ft.Page):
    page.title = "KML Itaiquara"
    page.window_maximized = True
    page.window_resizable = True  # Permite redimensionar
    page.window_maximizable = True  # Remove apenas o botão do meio
    page.window_minimizable = True  # Mantém o botão de minimizar
    page.padding = 0  # Removendo padding da página
    page.bgcolor = "#f0f0f0"
    page.scroll = None  # Removendo scroll da página
    page.window_title_bar_hidden = False
    page.window_title_bar_buttons_hidden = False

    # Configuração do tema da scrollbar
    page.theme = ft.Theme(
        scrollbar_theme=ft.ScrollbarTheme(
            track_color={
                ft.MaterialState.DEFAULT: ft.colors.TRANSPARENT,
            },
            track_visibility=True,
            track_border_color=ft.colors.TRANSPARENT,
            thumb_visibility=True,
            thumb_color={
                ft.MaterialState.DEFAULT: "#2196F3",
            },
            thickness=5,
            radius=5,
            main_axis_margin=5,
            cross_axis_margin=10,
        )
    )

    async def change_tab(e):
        tab_name = e.control.data
        # Show loading screen
        content_area.content = create_loading_view(page)
        page.update()

        # Simulate loading delay
        await asyncio.sleep(0.5)  # Small delay to show loading

        # Change content based on tab
        if tab_name == "visualizar":
            content_area.content = create_visualizar_view(page).controls[0]
        elif tab_name == "incluir":
            content_area.content = create_incluir_view(page).controls[0]
        elif tab_name == "alterar":
            content_area.content = create_alterar_view(page).controls[0]
        elif tab_name == "excluir":
            content_area.content = create_excluir_view(page).controls[0]
        
        page.update()
    
    # Criar botões de navegação
    navigation = ft.Container(
        content=ft.Row(
            [
                ft.TextButton(
                    text="Visualizar",
                    icon=ft.icons.VISIBILITY,
                    style=ft.ButtonStyle(color={"": "#2196F3"}),
                    on_click=change_tab,
                    data="visualizar",
                ),
                ft.VerticalDivider(width=1, color="#E0E0E0"),
                ft.TextButton(
                    text="Incluir",
                    icon=ft.icons.ADD_CIRCLE_OUTLINE,
                    style=ft.ButtonStyle(color={"": "#2196F3"}),
                    on_click=change_tab,
                    data="incluir",
                ),
                ft.TextButton(
                    text="Editar",
                    icon=ft.icons.EDIT,
                    style=ft.ButtonStyle(color={"": "#2196F3"}),
                    on_click=change_tab,
                    data="alterar",
                ),
                ft.TextButton(
                    text="Excluir",
                    icon=ft.icons.DELETE,
                    style=ft.ButtonStyle(color={"": "#2196F3"}),
                    on_click=change_tab,
                    data="excluir",
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=0,  # Remove espaço entre os botões
        ),
        margin=ft.margin.only(top=30),  # Adicionando margin top de volta
        visible=False,  # Começa invisível
    )

    # Área de conteúdo começando com loading em tela cheia
    loading_container = ft.Stack(
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

    content_area = ft.Container(
        expand=True,
        padding=20,  # Adicionando padding apenas para o conteúdo normal
    )

    # Criar o layout principal
    main_column = ft.Column([
        navigation,
        ft.Divider(height=2, color="#E0E0E0"),
        content_area,
    ])

    # Stack para sobrepor o loading sobre o conteúdo
    main_stack = ft.Stack([
        main_column,
        loading_container,
    ])

    # Layout principal
    page.add(main_stack)

    # Função para carregar a visualização inicial
    async def load_initial_view():
        navigation.visible = True  # Mostra o menu
        loading_container.visible = False  # Esconde o loading
        content_area.content = create_visualizar_view(page).controls[0]
        page.update()

    # Carregar a visualização inicial em segundo plano
    page.run_task(load_initial_view)

if __name__ == "__main__":
    try:
        ft.app(target=main)
    except Exception as e:
        logger.error(f"Erro ao iniciar a aplicação: {str(e)}", exc_info=True)
