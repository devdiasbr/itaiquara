import flet as ft
import sqlite3
import logging
import os
from utils.dropdown_helper import create_dropdown

def create_excluir_view(page: ft.Page):
    """Cria a view de exclusão de distribuidores"""
    try:
        # Configurar caminho do banco de dados
        current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        db_path = os.path.join(current_dir, 'database/database.db')

        # Status text para feedback
        status_text = ft.Text(
            value="",
            color="black",
            size=11,
            text_align=ft.TextAlign.CENTER,
        )

        # Dropdown de distribuidores
        distribuidor_dropdown = create_dropdown(
            label="Município",
            hint_text="Selecione o Município",
            width=400,  # Largura padrão
            on_change=lambda e: load_distribuidor_data(e)
        )

        # Campos do formulário (read-only)
        cnpj_field = ft.TextField(
            label="CNPJ",
            width=300,
            bgcolor="white",
            border_color="#2196F3",
            focused_border_color="#FF0000",
            focused_color="#000000",
            color="#000000",
            label_style=ft.TextStyle(color="#000000"),
            read_only=True,
        )

        razao_social_field = ft.TextField(
            label="Razão Social",
            width=300,
            bgcolor="white",
            border_color="#2196F3",
            focused_border_color="#FF0000",
            focused_color="#000000",
            color="#000000",
            label_style=ft.TextStyle(color="#000000"),
            read_only=True,
        )

        nome_fantasia_field = ft.TextField(
            label="Nome Fantasia",
            width=300,
            bgcolor="white",
            border_color="#2196F3",
            focused_border_color="#FF0000",
            focused_color="#000000",
            color="#000000",
            label_style=ft.TextStyle(color="#000000"),
            read_only=True,
        )

        responsavel_field = ft.TextField(
            label="Responsável",
            width=300,
            bgcolor="white",
            border_color="#2196F3",
            focused_border_color="#FF0000",
            focused_color="#000000",
            color="#000000",
            label_style=ft.TextStyle(color="#000000"),
            read_only=True,
        )

        telefone_responsavel_field = ft.TextField(
            label="Telefone Responsável",
            width=300,
            bgcolor="white",
            border_color="#2196F3",
            focused_border_color="#FF0000",
            focused_color="#000000",
            color="#000000",
            label_style=ft.TextStyle(color="#000000"),
            read_only=True,
        )

        contrato_field = ft.TextField(
            label="Contrato",
            width=300,
            bgcolor="white",
            border_color="#2196F3",
            focused_border_color="#FF0000",
            focused_color="#000000",
            color="#000000",
            label_style=ft.TextStyle(color="#000000"),
            read_only=True,
        )

        codigo_field = ft.TextField(
            label="Código",
            width=300,
            bgcolor="white",
            border_color="#2196F3",
            focused_border_color="#FF0000",
            focused_color="#000000",
            color="#000000",
            label_style=ft.TextStyle(color="#000000"),
            read_only=True,
        )

        distribuidor_outros_field = ft.TextField(
            label="Distribuidor Outros",
            width=300,
            bgcolor="white",
            border_color="#2196F3",
            focused_border_color="#FF0000",
            focused_color="#000000",
            color="#000000",
            label_style=ft.TextStyle(color="#000000"),
            read_only=True,
        )

        insc_estadual_field = ft.TextField(
            label="Inscrição Estadual",
            width=300,
            bgcolor="white",
            border_color="#2196F3",
            focused_border_color="#FF0000",
            focused_color="#000000",
            color="#000000",
            label_style=ft.TextStyle(color="#000000"),
            read_only=True,
        )

        contato_field = ft.TextField(
            label="Contato",
            width=300,
            bgcolor="white",
            border_color="#2196F3",
            focused_border_color="#FF0000",
            focused_color="#000000",
            color="#000000",
            label_style=ft.TextStyle(color="#000000"),
            read_only=True,
        )

        telefone_distribuidor_field = ft.TextField(
            label="Telefone Distribuidor",
            width=300,
            bgcolor="white",
            border_color="#2196F3",
            focused_border_color="#FF0000",
            focused_color="#000000",
            color="#000000",
            label_style=ft.TextStyle(color="#000000"),
            read_only=True,
        )

        celular_field = ft.TextField(
            label="Celular",
            width=300,
            bgcolor="white",
            border_color="#2196F3",
            focused_border_color="#FF0000",
            focused_color="#000000",
            color="#000000",
            label_style=ft.TextStyle(color="#000000"),
            read_only=True,
        )

        fax_field = ft.TextField(
            label="Fax",
            width=300,
            bgcolor="white",
            border_color="#2196F3",
            focused_border_color="#FF0000",
            focused_color="#000000",
            color="#000000",
            label_style=ft.TextStyle(color="#000000"),
            read_only=True,
        )

        endereco_field = ft.TextField(
            label="Endereço",
            width=300,
            bgcolor="white",
            border_color="#2196F3",
            focused_border_color="#FF0000",
            focused_color="#000000",
            color="#000000",
            label_style=ft.TextStyle(color="#000000"),
            read_only=True,
        )

        cidade_field = ft.TextField(
            label="Cidade",
            width=300,
            bgcolor="white",
            border_color="#2196F3",
            focused_border_color="#FF0000",
            focused_color="#000000",
            color="#000000",
            label_style=ft.TextStyle(color="#000000"),
            read_only=True,
        )

        uf_field = ft.TextField(
            label="UF",
            width=300,
            bgcolor="white",
            border_color="#2196F3",
            focused_border_color="#FF0000",
            focused_color="#000000",
            color="#000000",
            label_style=ft.TextStyle(color="#000000"),
            read_only=True,
        )

        cep_field = ft.TextField(
            label="CEP",
            width=300,
            bgcolor="white",
            border_color="#2196F3",
            focused_border_color="#FF0000",
            focused_color="#000000",
            color="#000000",
            label_style=ft.TextStyle(color="#000000"),
            read_only=True,
        )

        email_field = ft.TextField(
            label="Email",
            width=300,
            bgcolor="white",
            border_color="#2196F3",
            focused_border_color="#FF0000",
            focused_color="#000000",
            color="#000000",
            label_style=ft.TextStyle(color="#000000"),
            read_only=True,
        )

        def show_error_message(message):
            status_text.value = message
            status_text.color = "red"
            page.update()

        def show_success_message(message):
            status_text.value = message
            status_text.color = "green"
            page.update()

        def clear_fields():
            cnpj_field.value = ""
            razao_social_field.value = ""
            nome_fantasia_field.value = ""
            responsavel_field.value = ""
            telefone_responsavel_field.value = ""
            contrato_field.value = ""
            codigo_field.value = ""
            distribuidor_outros_field.value = ""
            insc_estadual_field.value = ""
            contato_field.value = ""
            telefone_distribuidor_field.value = ""
            celular_field.value = ""
            fax_field.value = ""
            endereco_field.value = ""
            cidade_field.value = ""
            uf_field.value = ""
            cep_field.value = ""
            email_field.value = ""
            distribuidor_dropdown.value = None
            page.update()

        def load_distribuidores():
            try:
                conn = sqlite3.connect(db_path)
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT DISTINCT m.descricao 
                    FROM municipios m
                    JOIN atendidos a ON m.municipio_uf = a.municipio_uf
                    JOIN distribuidores d ON a.cnpj_distribuidor = d.cnpj
                    WHERE d.razao_social IS NOT NULL
                    AND m.descricao IS NOT NULL 
                    ORDER BY m.descricao
                """)
                municipios = cursor.fetchall()
                conn.close()

                distribuidor_dropdown.options = [
                    ft.dropdown.Option(text=municipio[0])
                    for municipio in municipios
                ]
                page.update()

            except Exception as e:
                logging.error(f"Erro ao carregar municípios: {str(e)}")
                show_error_message(f"Erro ao carregar municípios: {str(e)}")

        def load_distribuidor_data(e):
            if not distribuidor_dropdown.value:
                return

            try:
                conn = sqlite3.connect(db_path)
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT d.* 
                    FROM municipios m
                    JOIN atendidos a ON m.municipio_uf = a.municipio_uf
                    JOIN distribuidores d ON a.cnpj_distribuidor = d.cnpj
                    WHERE m.descricao = ?
                    AND d.razao_social IS NOT NULL
                """, (distribuidor_dropdown.value,))
                
                distribuidor = cursor.fetchone()
                conn.close()

                if distribuidor:
                    cnpj_field.value = distribuidor[0]
                    razao_social_field.value = distribuidor[1]
                    nome_fantasia_field.value = distribuidor[2]
                    responsavel_field.value = distribuidor[3]
                    telefone_responsavel_field.value = distribuidor[4]
                    contrato_field.value = distribuidor[5]
                    codigo_field.value = distribuidor[6]
                    distribuidor_outros_field.value = distribuidor[7]
                    insc_estadual_field.value = distribuidor[8]
                    contato_field.value = distribuidor[9]
                    telefone_distribuidor_field.value = distribuidor[10]
                    celular_field.value = distribuidor[11]
                    fax_field.value = distribuidor[12]
                    endereco_field.value = distribuidor[13]
                    cidade_field.value = distribuidor[14]
                    uf_field.value = distribuidor[15]
                    cep_field.value = distribuidor[16]
                    email_field.value = distribuidor[17]
                    page.update()

            except Exception as e:
                logging.error(f"Erro ao carregar dados do distribuidor: {str(e)}")
                show_error_message(f"Erro ao carregar dados do distribuidor: {str(e)}")

        def delete_distribuidor(e):
            if not distribuidor_dropdown.value:
                show_error_message("Por favor, selecione um município")
                return

            def confirm_delete(e):
                dlg.open = False
                page.update()

                try:
                    conn = sqlite3.connect(db_path)
                    cursor = conn.cursor()
                    
                    # Primeiro, pegar o CNPJ do distribuidor
                    cursor.execute("""
                        SELECT a.cnpj_distribuidor
                        FROM municipios m
                        JOIN atendidos a ON m.municipio_uf = a.municipio_uf
                        WHERE m.descricao = ?
                    """, (distribuidor_dropdown.value,))
                    
                    cnpj_result = cursor.fetchone()
                    if cnpj_result:
                        cnpj = cnpj_result[0]
                        
                        # Deletar da tabela atendidos primeiro (por causa da chave estrangeira)
                        cursor.execute("""
                            DELETE FROM atendidos 
                            WHERE cnpj_distribuidor = ?
                        """, (cnpj,))
                        
                        # Depois deletar da tabela distribuidores
                        cursor.execute("""
                            DELETE FROM distribuidores 
                            WHERE cnpj = ?
                        """, (cnpj,))
                        
                        conn.commit()
                        conn.close()

                        show_success_message("Distribuidor excluído com sucesso!")
                        clear_fields()
                        load_distribuidores()
                    else:
                        show_error_message("Distribuidor não encontrado")
                        
                except Exception as e:
                    logging.error(f"Erro ao excluir distribuidor: {str(e)}")
                    show_error_message(f"Erro ao excluir distribuidor: {str(e)}")

            def cancel_delete(e):
                dlg.open = False
                page.update()

            # Diálogo de confirmação
            dlg = ft.AlertDialog(
                modal=True,
                title=ft.Text("Confirmar exclusão"),
                content=ft.Text("Tem certeza que deseja excluir este distribuidor?"),
                actions=[
                    ft.TextButton("Sim", on_click=confirm_delete),
                    ft.TextButton("Não", on_click=cancel_delete),
                ],
                actions_alignment=ft.MainAxisAlignment.END,
            )

            page.dialog = dlg
            dlg.open = True
            page.update()

        # Botão de excluir
        delete_button = ft.ElevatedButton(
            "Excluir",
            bgcolor="#2196F3",
            color="white",
            width=200,
            on_click=delete_distribuidor,
        )

        # Botão de limpar
        clear_button = ft.ElevatedButton(
            "Limpar",
            bgcolor="white",
            color="#2196F3",
            width=200,
            on_click=lambda e: clear_fields(),
        )

        # Botões
        buttons_row = ft.Row(
            [
                delete_button,
                clear_button,
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        )

        # Layout dos campos em grid
        fields_grid = ft.Column(
            controls=[
                ft.Row(
                    [distribuidor_dropdown],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                ft.Row(
                    [cnpj_field, razao_social_field, nome_fantasia_field],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                ft.Row(
                    [responsavel_field, telefone_responsavel_field, contrato_field],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                ft.Row(
                    [codigo_field, distribuidor_outros_field, insc_estadual_field],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                ft.Row(
                    [contato_field, telefone_distribuidor_field, celular_field],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                ft.Row(
                    [fax_field, endereco_field, cidade_field],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                ft.Row(
                    [uf_field, cep_field, email_field],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                buttons_row,
                status_text,
            ],
            spacing=20,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )

        # Criar a view
        deletar_view = ft.Card(
            content=ft.Container(
                content=ft.Column(
                    [
                        ft.Text(
                            "Excluir Distribuidor",
                            size=24,
                            weight=ft.FontWeight.BOLD,
                            color="#2196F3",
                            text_align=ft.TextAlign.CENTER,
                        ),
                        fields_grid,
                    ],
                    spacing=20,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                padding=20,
                bgcolor="white",
                height=800,
            ),
            elevation=3,
            margin=20,
        )

        # Carregar dados iniciais
        load_distribuidores()

        return ft.View("/deletar", [deletar_view])

    except Exception as e:
        logging.error(f"Erro ao criar view de exclusão: {str(e)}", exc_info=True)
        return ft.Column(controls=[
            ft.Text("Erro ao carregar a view de exclusão", color="red")
        ])