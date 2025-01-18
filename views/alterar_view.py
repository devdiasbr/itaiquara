import flet as ft
import logging
import os
import sqlite3
from utils.dropdown_helper import create_dropdown

def create_alterar_view(page: ft.Page):
    try:
        # Configurar caminho do banco de dados
        current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        db_path = os.path.join(current_dir, 'database/database.db')
        
        # Status text para feedback
        status_text = ft.Text(
            value="",
            color="black",
            size=16,
            text_align=ft.TextAlign.CENTER,
        )

        # Campos do formulário
        nome_fantasia_field = ft.TextField(
            label="Nome Fantasia",
            width=300,
            bgcolor="white",
            border_color="#2196F3",
            focused_border_color="#FF0000",
            focused_color="#000000",
            color="#000000",
            label_style=ft.TextStyle(color="#000000"),
            read_only=False
        )
        
        unidade_field = ft.TextField(
            label="Unidade",
            width=300,
            bgcolor="white",
            border_color="#2196F3",
            focused_border_color="#FF0000",
            focused_color="#000000",
            color="#000000",
            label_style=ft.TextStyle(color="#000000"),
        )
        
        tipo_unidade_field = ft.TextField(
            label="Tipo Unidade",
            width=300,
            bgcolor="white",
            border_color="#2196F3",
            focused_border_color="#FF0000",
            focused_color="#000000",
            color="#000000",
            label_style=ft.TextStyle(color="#000000"),
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
            read_only=False
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
            read_only=False
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
            read_only=False
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
            read_only=False
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
            read_only=False
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
            read_only=False
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
            read_only=False
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
            read_only=False
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
            read_only=False
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
            read_only=False
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
            read_only=False
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
            read_only=False
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
            read_only=False
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
            read_only=False
        )

        def get_razoes_sociais():
            try:
                conn = sqlite3.connect(db_path)
                cursor = conn.cursor()
                cursor.execute("SELECT razao_social FROM distribuidores ORDER BY razao_social")
                result = cursor.fetchall()
                conn.close()
                return [row[0] for row in result]
            except Exception as e:
                logging.error(f"Erro ao buscar razões sociais: {e}")
                return []

        def get_distribuidor(razao_social):
            try:
                conn = sqlite3.connect(db_path)
                cursor = conn.cursor()
                
                cursor.execute("""
                    SELECT DISTINCT
                        m.municipio_uf,
                        m.municipio,
                        m.uf,
                        m.populacao,
                        a.unidade,
                        a.tipo_unidade,
                        a.razao_social_atendido,
                        d.cnpj,
                        d.razao_social,
                        d.nome_fantasia,
                        d.responsavel,
                        d.telefone_responsavel,
                        d.contrato,
                        d.codigo,
                        d.distribuidor_outros,
                        d.insc_estadual,
                        d.contato,
                        d.telefone_distribuidor,
                        d.celular,
                        d.fax,
                        d.endereco,
                        d.cidade,
                        d.uf as uf_distribuidor,
                        d.cep,
                        d.email
                    FROM distribuidores d
                    LEFT JOIN atendidos a ON d.cnpj = a.cnpj_distribuidor
                    LEFT JOIN municipios m ON a.municipio_uf = m.municipio_uf
                    WHERE d.razao_social = ?
                """, (razao_social,))
                
                result = cursor.fetchone()
                
                if result:
                    columns = [description[0] for description in cursor.description]
                    distribuidor = dict(zip(columns, result))
                    conn.close()
                    return True, distribuidor
                else:
                    conn.close()
                    return False, "Distribuidor não encontrado"
            except Exception as e:
                logging.error(f"Erro ao buscar distribuidor: {e}")
                return False, f"Erro ao buscar distribuidor: {e}"

        def update_distribuidor(razao_social, data):
            try:
                conn = sqlite3.connect(db_path)
                cursor = conn.cursor()
                
                # Remover campos que não devem ser atualizados
                update_data = data.copy()
                update_data.pop('cnpj', None)  # Remove CNPJ dos campos a serem atualizados
                update_data.pop('razao_social', None)  # Remove razao_social também pois é usado na condição WHERE
                
                # Criar a query de update apenas com os campos que têm valor
                update_fields = []
                values = []
                for field, value in update_data.items():
                    if value is not None and value.strip() != "":
                        update_fields.append(f"{field} = ?")
                        values.append(value)
                
                if not update_fields:
                    conn.close()
                    return False, "Nenhum campo para atualizar"
                
                # Adicionar a razão social para a cláusula WHERE
                values.append(razao_social)
                
                # Construir e executar a query
                query = f"""
                    UPDATE distribuidores 
                    SET {', '.join(update_fields)}
                    WHERE razao_social = ?
                """
                
                cursor.execute(query, values)
                conn.commit()
                conn.close()
                
                return True, "Dados atualizados com sucesso!"
                
            except sqlite3.IntegrityError as e:
                conn.close()
                logging.error(f"Erro de integridade ao atualizar distribuidor: {e}")
                return False, "Não é possível atualizar o CNPJ pois ele já existe para outro distribuidor"
            except Exception as e:
                conn.close()
                logging.error(f"Erro ao atualizar distribuidor: {e}")
                return False, f"Erro ao atualizar dados: {str(e)}"

        def clear_fields():
            """Limpa todos os campos do formulário"""
            for field in [
                nome_fantasia_field, unidade_field, tipo_unidade_field,
                responsavel_field, telefone_responsavel_field, contrato_field,
                codigo_field, distribuidor_outros_field, insc_estadual_field,
                contato_field, telefone_distribuidor_field, celular_field,
                fax_field, endereco_field, cidade_field,
                uf_field, cep_field, email_field
            ]:
                field.value = ""
                field.update()

        def load_data(razao_social):
            if razao_social:
                success, result = get_distribuidor(razao_social)
                if success:
                    nome_fantasia_field.value = result.get('nome_fantasia', '')
                    unidade_field.value = result.get('unidade', '')
                    tipo_unidade_field.value = result.get('tipo_unidade', '')
                    responsavel_field.value = result.get('responsavel', '')
                    telefone_responsavel_field.value = result.get('telefone_responsavel', '')
                    contrato_field.value = result.get('contrato', '')
                    codigo_field.value = result.get('codigo', '')
                    distribuidor_outros_field.value = result.get('distribuidor_outros', '')
                    insc_estadual_field.value = result.get('insc_estadual', '')
                    contato_field.value = result.get('contato', '')
                    telefone_distribuidor_field.value = result.get('telefone_distribuidor', '')
                    celular_field.value = result.get('celular', '')
                    fax_field.value = result.get('fax', '')
                    endereco_field.value = result.get('endereco', '')
                    cidade_field.value = result.get('cidade', '')
                    uf_field.value = result.get('uf_distribuidor', '')
                    cep_field.value = result.get('cep', '')
                    email_field.value = result.get('email', '')
                    page.update()

        def on_update_click(e):
            """Atualiza os dados do distribuidor"""
            razao_social = razao_social_dropdown.value
            if not razao_social:
                status_text.value = "Por favor, selecione uma Razão Social!"
                status_text.color = "red"
                page.update()
                return

            # Diálogo de confirmação
            dlg = ft.AlertDialog(
                modal=True,
                title=ft.Text("Confirmar alteração"),
                content=ft.Text("Tem certeza que deseja alterar este distribuidor?"),
                actions=[
                    ft.TextButton("Sim", on_click=confirm_update),
                    ft.TextButton("Não", on_click=lambda e: close_dialog(dlg)),
                ],
                actions_alignment=ft.MainAxisAlignment.END,
            )

            page.dialog = dlg
            dlg.open = True
            page.update()

        def close_dialog(dlg):
            dlg.open = False
            page.update()

        def confirm_update(e):
            page.dialog.open = False
            page.update()

            razao_social = razao_social_dropdown.value
            distribuidor_data = {
                'razao_social': razao_social,
                'nome_fantasia': nome_fantasia_field.value,
                'unidade': unidade_field.value,
                'tipo_unidade': tipo_unidade_field.value,
                'responsavel': responsavel_field.value,
                'telefone_responsavel': telefone_responsavel_field.value,
                'contrato': contrato_field.value,
                'codigo': codigo_field.value,
                'distribuidor_outros': distribuidor_outros_field.value,
                'insc_estadual': insc_estadual_field.value,
                'contato': contato_field.value,
                'telefone_distribuidor': telefone_distribuidor_field.value,
                'celular': celular_field.value,
                'fax': fax_field.value,
                'endereco': endereco_field.value,
                'cidade': cidade_field.value,
                'uf': uf_field.value,
                'cep': cep_field.value,
                'email': email_field.value,
            }
            
            # Verificar se todos os campos estão vazios
            if all(not value for value in distribuidor_data.values() if value is not None):
                status_text.value = "Por favor, preencha pelo menos um campo antes de atualizar!"
                status_text.color = "red"
                page.update()
                return
            
            success, message = update_distribuidor(razao_social, distribuidor_data)
            if success:
                status_text.value = "Dados atualizados com sucesso!"
                status_text.color = "green"
            else:
                status_text.value = f"Erro ao atualizar dados: {message}"
                status_text.color = "red"
            page.update()

        def on_razao_social_selected(e):
            razao_social = razao_social_dropdown.value
            if razao_social:
                load_data(razao_social)
                status_text.value = "Dados carregados! Faça as alterações necessárias e clique em Atualizar."
                status_text.color = "green"
            else:
                status_text.value = "Por favor, selecione uma Razão Social!"
                status_text.color = "red"
            page.update()

        # Dropdown de razões sociais
        razao_social_dropdown = create_dropdown(
            label="Distribuidor",
            hint_text="Selecione o distribuidor",
            width=400,
            on_change=on_razao_social_selected
        )

        def carregar_razoes_sociais():
            try:
                conn = sqlite3.connect(db_path)
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT DISTINCT razao_social 
                    FROM distribuidores 
                    ORDER BY razao_social
                """)
                items = [row[0] for row in cursor.fetchall()]
                razao_social_dropdown.options = [ft.dropdown.Option(text=item) for item in items]
                page.update()
            except Exception as e:
                logging.error(f"Erro ao carregar razões sociais: {str(e)}")
                show_error_message("Erro ao carregar lista de distribuidores")

        carregar_razoes_sociais()

        # Dropdown de unidades
        unidade_dropdown = ft.Dropdown(
            label="Unidade",
            options=[
                ft.dropdown.Option("Açúcar"),
                ft.dropdown.Option("Etanol"),
            ],
            width=400,  # Largura padrão
            height=55,
            filled=True,
            bgcolor="white",
            border_color="#2196F3",
            focused_border_color="#FF0000",
            focused_color="#000000",
            label_style=ft.TextStyle(color="#000000", weight=ft.FontWeight.BOLD),
            text_style=ft.TextStyle(color="#000000", size=16, weight=ft.FontWeight.BOLD),
            content_padding=10,
            alignment=ft.alignment.center,
        )

        # Dropdown de tipos de unidade
        tipo_unidade_dropdown = ft.Dropdown(
            label="Tipo de Unidade",
            options=[
                ft.dropdown.Option("Distribuidor"),
                ft.dropdown.Option("Usina"),
                ft.dropdown.Option("Revenda"),
            ],
            width=400,  # Largura padrão
            height=55,
            filled=True,
            bgcolor="white",
            border_color="#2196F3",
            focused_border_color="#FF0000",
            focused_color="#000000",
            label_style=ft.TextStyle(color="#000000", weight=ft.FontWeight.BOLD),
            text_style=ft.TextStyle(color="#000000", size=16, weight=ft.FontWeight.BOLD),
            content_padding=10,
            alignment=ft.alignment.center,
        )

        # Botões
        buttons_row = ft.Row(
            [
                ft.ElevatedButton(
                    "Atualizar",
                    bgcolor="#2196F3",
                    color="white",
                    width=200,
                    on_click=on_update_click,
                ),
                ft.ElevatedButton(
                    "Limpar",
                    bgcolor="white",
                    color="#2196F3",
                    width=200,
                    on_click=lambda e: clear_fields(),
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        )

        # Layout dos campos em grid
        fields_grid = ft.Column(
            controls=[
                ft.Row(
                    [razao_social_dropdown],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                ft.Row(
                    [nome_fantasia_field, unidade_field, tipo_unidade_field],
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

        # Container principal
        alterar_view = ft.Card(
            content=ft.Container(
                content=ft.Column(
                    [
                        ft.Text(
                            "Alterar Distribuidor",
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
                expand=True,
            ),
            elevation=3,
            margin=20,
        )

        return ft.View("/alterar", [alterar_view])

    except Exception as e:
        logging.error(f"Erro ao criar view de alteração: {str(e)}", exc_info=True)
        return ft.Column(controls=[
            ft.Text("Erro ao carregar a view de alteração", color="red")

        ])
