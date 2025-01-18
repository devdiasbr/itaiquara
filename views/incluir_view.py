import flet as ft
import logging
import os
import sqlite3
from utils.dropdown_helper import create_dropdown

def create_incluir_view(page: ft.Page):
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

        # Campos do formulário
        cnpj_field = ft.TextField(
            label="CNPJ",
            width=300,
            bgcolor="white",
            border_color="#2196F3",
            focused_border_color="#FF0000",
            focused_color="#000000",
            color="#000000",
            label_style=ft.TextStyle(color="#000000"),
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
        )

        def get_descricoes():
            """Busca todas as descrições de municípios"""
            try:
                conn = sqlite3.connect(db_path)
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT DISTINCT m.descricao 
                    FROM municipios m
                    LEFT JOIN atendidos a ON m.municipio_uf = a.municipio_uf
                    LEFT JOIN distribuidores d ON a.cnpj_distribuidor = d.cnpj
                    WHERE (d.razao_social IS NULL OR d.cnpj IS NULL)
                    AND m.descricao IS NOT NULL 
                    ORDER BY m.descricao
                """)
                result = cursor.fetchall()
                conn.close()
                return [row[0] for row in result]
            except Exception as e:
                logging.error(f"Erro ao buscar descrições: {str(e)}")
                return []

        def get_municipio_by_descricao(descricao):
            """Busca dados do município pela descrição"""
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
                    FROM municipios m
                    LEFT JOIN atendidos a ON m.municipio_uf = a.municipio_uf
                    LEFT JOIN distribuidores d ON a.cnpj_distribuidor = d.cnpj
                    WHERE m.descricao = ?
                """, (descricao,))
                result = cursor.fetchone()
                
                if result:
                    columns = [description[0] for description in cursor.description]
                    municipio_data = dict(zip(columns, result))
                    conn.close()
                    return True, municipio_data
                else:
                    conn.close()
                    return False, "Município não encontrado"
            except Exception as e:
                logging.error(f"Erro ao buscar município: {e}")
                return False, f"Erro ao buscar município: {e}"

        def create_distribuidor(data, municipio_data):
            try:
                conn = sqlite3.connect(db_path)
                cursor = conn.cursor()
                
                # Verificar se o CNPJ já existe para este município
                cursor.execute("""
                    SELECT d.cnpj 
                    FROM distribuidores d
                    JOIN atendidos a ON d.cnpj = a.cnpj_distribuidor
                    WHERE d.cnpj = ? AND a.municipio_uf = ?
                """, (data['cnpj'], municipio_data['municipio_uf']))
                
                if cursor.fetchone():
                    conn.close()
                    return False, "Este distribuidor já está cadastrado para este município"
                
                # Verificar se o CNPJ já existe em distribuidores
                cursor.execute("SELECT cnpj FROM distribuidores WHERE cnpj = ?", (data['cnpj'],))
                distribuidor_existe = cursor.fetchone()
                
                if not distribuidor_existe:
                    # Se o distribuidor não existe, inserir na tabela distribuidores
                    cursor.execute("""
                        INSERT INTO distribuidores (
                            cnpj, razao_social, nome_fantasia, responsavel, 
                            telefone_responsavel, contrato, codigo, distribuidor_outros,
                            insc_estadual, contato, telefone_distribuidor, celular,
                            fax, endereco, cidade, uf, cep, email
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (
                        data['cnpj'], data['razao_social'], data['nome_fantasia'],
                        data['responsavel'], data['telefone_responsavel'], data['contrato'],
                        data['codigo'], data['distribuidor_outros'], data['insc_estadual'],
                        data['contato'], data['telefone_distribuidor'], data['celular'],
                        data['fax'], data['endereco'], data['cidade'], data['uf'],
                        data['cep'], data['email']
                    ))

                # Inserir na tabela atendidos
                tipo_unidade = 'REGIONAL' if 'REGIONAL' in str(unidade_field.value).upper() else 'FILIAL'
                cursor.execute("""
                    INSERT INTO atendidos (
                        municipio_uf, unidade, tipo_unidade, razao_social_atendido, cnpj_distribuidor
                    ) VALUES (?, ?, ?, ?, ?)
                """, (
                    municipio_data['municipio_uf'], unidade_field.value, tipo_unidade,
                    data['razao_social'], data['cnpj']
                ))
                
                conn.commit()
                conn.close()
                return True, "Distribuidor cadastrado com sucesso!"
            except Exception as e:
                logging.error(f"Erro ao criar distribuidor: {e}")
                return False, f"Erro ao criar distribuidor: {e}"

        def clear_fields():
            """Limpa todos os campos do formulário"""
            for field in [
                cnpj_field, razao_social_field, nome_fantasia_field, unidade_field, tipo_unidade_field,
                responsavel_field, telefone_responsavel_field, contrato_field,
                codigo_field, distribuidor_outros_field, insc_estadual_field,
                contato_field, telefone_distribuidor_field, celular_field,
                fax_field, endereco_field, cidade_field,
                uf_field, cep_field, email_field
            ]:
                field.value = ""
                field.update()

        def on_save_click(e):
            """Salva os dados do novo distribuidor"""
            if not descricao_searchbox.value:
                status_text.value = "Por favor, selecione um município"
                status_text.color = "red"
                page.update()
                return

            # Diálogo de confirmação
            dlg = ft.AlertDialog(
                modal=True,
                title=ft.Text("Confirmar inclusão"),
                content=ft.Text("Tem certeza que deseja incluir este distribuidor?"),
                actions=[
                    ft.TextButton("Sim", on_click=confirm_save),
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

        def confirm_save(e):
            page.dialog.open = False
            page.update()

            distribuidor_data = {
                'cnpj': cnpj_field.value,
                'razao_social': razao_social_field.value,
                'nome_fantasia': nome_fantasia_field.value,
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
            
            success, municipio_data = get_municipio_by_descricao(descricao_searchbox.value)
            if not success:
                status_text.value = municipio_data
                status_text.color = "red"
                page.update()
                return
            
            success, message = create_distribuidor(distribuidor_data, municipio_data)
            if success:
                status_text.value = message
                status_text.color = "green"
                clear_fields()
            else:
                status_text.value = message
                status_text.color = "red"
            page.update()

        def on_descricao_selected(e):
            descricao = descricao_searchbox.value
            if descricao:
                success, result = get_municipio_by_descricao(descricao)
                if success:
                    cnpj_field.value = result.get('cnpj_atendido', '')
                    razao_social_field.value = result.get('razao_social_atendido', '')
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
                    
                    status_text.value = "Dados carregados! Faça as alterações necessárias e clique em Salvar."
                    status_text.color = "green"
                else:
                    status_text.value = result
                    status_text.color = "red"
                page.update()

        def get_razoes_sociais():
            """Retorna lista de razões sociais dos distribuidores"""
            try:
                conn = sqlite3.connect(db_path)
                cursor = conn.cursor()
                cursor.execute("SELECT razao_social FROM distribuidores")
                razoes = [row[0] for row in cursor.fetchall() if row[0]]
                conn.close()
                return razoes
            except Exception as e:
                logging.error(f"Erro ao buscar razões sociais: {str(e)}")
                return []

        def get_distribuidor_by_razao_social(razao_social):
            """Busca dados do distribuidor pela razão social"""
            try:
                conn = sqlite3.connect(db_path)
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT DISTINCT
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
                        d.uf,
                        d.cep,
                        d.email,
                        a.unidade,
                        a.tipo_unidade
                    FROM distribuidores d
                    LEFT JOIN atendidos a ON d.cnpj = a.cnpj_distribuidor
                    WHERE d.razao_social = ?
                """, (razao_social,))
                
                result = cursor.fetchone()
                if result:
                    # Mapear os resultados para um dicionário
                    columns = [col[0] for col in cursor.description]
                    distribuidor = dict(zip(columns, result))
                    conn.close()
                    return True, distribuidor
                conn.close()
                return False, "Distribuidor não encontrado"
            except Exception as e:
                logging.error(f"Erro ao buscar distribuidor: {str(e)}")
                return False, str(e)

        razoes_sociais_dropdown = ft.Dropdown(
            label="Selecione um Distribuidor Existente",
            options=[ft.dropdown.Option(razao) for razao in sorted(get_razoes_sociais())],
            width=400,
            height=55,
            filled=True,
            bgcolor="white",
            border_color="#2196F3",
            focused_border_color="#FF0000",
            focused_color="#000000",
            label_style=ft.TextStyle(color="#000000", weight=ft.FontWeight.BOLD),
            text_style=ft.TextStyle(color="black", size=11, weight=ft.FontWeight.BOLD),
            content_padding=10,
            alignment=ft.alignment.center,
            on_change=lambda e: load_data(e.data) if e.data else None,
        )

        def load_data(razao_social):
            """Carrega os dados do distribuidor selecionado"""
            if razao_social:
                success, result = get_distribuidor_by_razao_social(razao_social)
                if success:
                    cnpj_field.value = result.get('cnpj', '')
                    razao_social_field.value = result.get('razao_social', '')
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
                    uf_field.value = result.get('uf', '')
                    cep_field.value = result.get('cep', '')
                    email_field.value = result.get('email', '')
                    status_text.value = "Dados carregados! Faça as alterações necessárias e clique em Salvar."
                    status_text.color = "green"
                else:
                    status_text.value = "Erro ao carregar dados do distribuidor!"
                    status_text.color = "red"
                page.update()

        descricao_searchbox = ft.TextField(
            label="Município",
            hint_text="Digite para buscar o município",
            hint_style=ft.TextStyle(color="#000000"),
            width=400,
            height=55,
            bgcolor="white",
            border_color="#2196F3",
            focused_border_color="#FF0000",
            color="#000000",
            label_style=ft.TextStyle(color="#000000", weight=ft.FontWeight.BOLD),
            text_style=ft.TextStyle(color="#000000", size=11, weight=ft.FontWeight.BOLD),
            on_change=lambda e: filtrar_municipios(e.control.value.upper() if e.control.value else ""),
            capitalization=ft.TextCapitalization.CHARACTERS  # Força maiúsculas ao digitar
        )

        def handle_text_change(self, text):
            if text:
                text = text.upper()
            filtrar_municipios(text)

        resultados_lista = ft.ListView(
            height=120,  # Altura de 120
            width=800,
            spacing=2,
            padding=10,
            visible=False
        )

        lista_container = ft.Container(
            content=resultados_lista,
            bgcolor="white",
            border=ft.border.all(1, "#2196F3"),
            border_radius=5,
            padding=5,
            width=800,
            visible=False
        )

        def show_error_message(message):
            """Mostra mensagem de erro usando o snack_bar"""
            page.snack_bar = ft.SnackBar(
                content=ft.Text(message),
                bgcolor=ft.colors.RED_400
            )
            page.snack_bar.open = True
            page.update()

        def filtrar_municipios(texto_busca):
            try:
                conn = sqlite3.connect(db_path)
                cursor = conn.cursor()
                
                # Se não houver texto de busca, oculta a lista
                if not texto_busca:
                    resultados_lista.visible = False
                    lista_container.visible = False
                    page.update()
                    return

                # Se houver texto, mostra a lista e filtra
                resultados_lista.visible = True
                lista_container.visible = True
                
                query = """
                    SELECT DISTINCT m.descricao 
                    FROM municipios m
                    WHERE m.descricao LIKE ?
                    ORDER BY m.descricao
                """
                cursor.execute(query, (f"{texto_busca.upper()}%",))
                
                items = cursor.fetchall()
                
                # Limpa a lista
                resultados_lista.controls.clear()
                
                # Agrupa itens em linhas de 3
                row = []
                for item in items:
                    row.append(
                        ft.Container(
                            content=ft.Text(
                                item[0].upper(),
                                size=12,
                                weight=ft.FontWeight.BOLD,
                                color="#000000"
                            ),
                            padding=10,
                            bgcolor="white",
                            border=ft.border.all(1, "#2196F3"),
                            border_radius=5,
                            on_click=lambda _, x=item[0]: selecionar_municipio(x),
                            width=250
                        )
                    )
                    
                    # Quando tiver 3 itens, cria uma linha
                    if len(row) == 3:
                        resultados_lista.controls.append(
                            ft.Row(
                                controls=row,
                                spacing=10,
                                alignment=ft.MainAxisAlignment.START
                            )
                        )
                        row = []
                
                # Se sobrar itens, cria a última linha
                if row:
                    resultados_lista.controls.append(
                        ft.Row(
                            controls=row,
                            spacing=10,
                            alignment=ft.MainAxisAlignment.START
                        )
                    )
                
                page.update()
                
            except Exception as e:
                logging.error(f"Erro ao filtrar municípios: {str(e)}")
                show_error_message("Erro ao buscar municípios")

        def selecionar_municipio(municipio):
            descricao_searchbox.value = municipio.upper()
            page.update()

        # Carrega a lista inicial de municípios
        filtrar_municipios("")

        # Layout dos campos em grid
        fields_grid = ft.Column(
            controls=[
                ft.Row(
                    [descricao_searchbox, razoes_sociais_dropdown],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                lista_container,
                ft.Row(
                    [cnpj_field, razao_social_field, nome_fantasia_field],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                ft.Row(
                    [unidade_field, tipo_unidade_field, responsavel_field],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                ft.Row(
                    [telefone_responsavel_field, contrato_field, codigo_field],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                ft.Row(
                    [distribuidor_outros_field, insc_estadual_field, contato_field],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                ft.Row(
                    [telefone_distribuidor_field, celular_field, fax_field],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                ft.Row(
                    [endereco_field, cidade_field, uf_field],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                ft.Row(
                    [cep_field, email_field],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                ft.Row(
                    [
                        ft.ElevatedButton(
                            "Salvar",
                            style=ft.ButtonStyle(
                                bgcolor={"": ft.colors.BLUE},
                                color={"": ft.colors.WHITE},
                                shape={"": ft.RoundedRectangleBorder(radius=20)},
                            ),
                            width=200,
                            on_click=lambda _: on_save_click(None)
                        ),
                        ft.ElevatedButton(
                            "Limpar",
                            style=ft.ButtonStyle(
                                bgcolor={"": ft.colors.WHITE},
                                color={"": ft.colors.BLUE},
                                shape={"": ft.RoundedRectangleBorder(radius=20)},
                                side={"": ft.BorderSide(1, ft.colors.BLUE)},
                            ),
                            width=200,
                            on_click=lambda _: clear_fields()
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=20,
                ),
                ft.Row(
                    [status_text],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
            ],
            spacing=20,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )

        # Criar a view
        incluir_view = ft.Card(
            content=ft.Container(
                content=ft.Column(
                    [
                        ft.Text(
                            "Incluir Distribuidor",
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

        return ft.View("/incluir", [incluir_view])

    except Exception as e:
        logging.error(f"Erro ao criar view de inclusão: {str(e)}", exc_info=True)
        return ft.Column(controls=[
            ft.Text("Erro ao carregar a view de inclusão", color="red")
        ])