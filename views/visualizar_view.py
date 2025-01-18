import flet as ft
import logging
import sqlite3
import os
from utils.kml_generator import KMLGenerator
from views.loading_view import create_loading_view

class DatabaseManager:
    def __init__(self):
        current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.db_path = os.path.join(current_dir, 'database/database.db')
        if not os.path.exists(self.db_path):
            logging.error(f"Banco de dados não encontrado: {self.db_path}")
            raise FileNotFoundError(f"Banco de dados não encontrado: {self.db_path}")
        logging.info(f"Banco de dados encontrado: {self.db_path}")

class CRUDManager:
    def __init__(self, db_path):
        if not os.path.exists(db_path):
            raise Exception(f"Banco de dados não encontrado: {db_path}")
        logging.info(f"Banco de dados encontrado: {db_path}")
        self.db_path = db_path

    def get_page_data(self):
        try:
            logging.info("Conectando ao banco de dados...")
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            logging.info("Executando query...")
            
            query = """
            SELECT DISTINCT
                m.municipio_uf,
                m.municipio,
                m.uf,
                m.populacao,
                m.coordenadas,
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
            ORDER BY m.municipio_uf
            """
            
            logging.info(f"Executando query: {query}")
            cursor.execute(query)
            data = cursor.fetchall()
            
            logging.info("Query executada com sucesso")
            logging.info(f"Dados obtidos: {len(data)} registros")
            
            conn.close()
            return data
            
        except Exception as e:
            logging.error(f"Erro ao executar query: {e}")
            raise e

def create_visualizar_view(page: ft.Page):
    class TableState:
        def __init__(self):
            self.current_page = 1
            self.items_per_page = 10
            self.original_rows = []
            self.total_pages = 1
            self.filtered_rows = []
    
    state = TableState()
    db_manager = DatabaseManager()
    crud_manager = CRUDManager(db_manager.db_path)
    
    # Status text para feedback
    status_text = ft.Text(
        value="",
        color="black",
        size=16,
        text_align=ft.TextAlign.CENTER,
    )

    # DataTable
    data_table = ft.DataTable(
        border=ft.border.all(1, "black"),
        border_radius=8,
        vertical_lines=ft.border.BorderSide(1, "black"),
        horizontal_lines=ft.border.BorderSide(1, "black"),
        heading_row_color=ft.colors.BLACK12,
        heading_row_height=70,
        data_row_color={"hovered": "0x30FF0000"},
        show_checkbox_column=True,
        columns=[
            ft.DataColumn(ft.Text("Município/UF", weight=ft.FontWeight.BOLD, color="black")),
            ft.DataColumn(ft.Text("Município", weight=ft.FontWeight.BOLD, color="black")),
            ft.DataColumn(ft.Text("UF", weight=ft.FontWeight.BOLD, color="black")),
            ft.DataColumn(ft.Text("População", weight=ft.FontWeight.BOLD, color="black")),
            ft.DataColumn(ft.Text("Coordenadas", weight=ft.FontWeight.BOLD, color="black")),
            ft.DataColumn(ft.Text("Unidade", weight=ft.FontWeight.BOLD, color="black")),
            ft.DataColumn(ft.Text("Tipo Unidade", weight=ft.FontWeight.BOLD, color="black")),
            ft.DataColumn(ft.Text("Razão Social", weight=ft.FontWeight.BOLD, color="black")),
            ft.DataColumn(ft.Text("CNPJ", weight=ft.FontWeight.BOLD, color="black")),
            ft.DataColumn(ft.Text("Nome Fantasia", weight=ft.FontWeight.BOLD, color="black")),
            ft.DataColumn(ft.Text("Responsável", weight=ft.FontWeight.BOLD, color="black")),
            ft.DataColumn(ft.Text("Contato Responsável", weight=ft.FontWeight.BOLD, color="black")),
            ft.DataColumn(ft.Text("Contrato", weight=ft.FontWeight.BOLD, color="black")),
            ft.DataColumn(ft.Text("Código", weight=ft.FontWeight.BOLD, color="black")),
            ft.DataColumn(ft.Text("Distribuidor Outros", weight=ft.FontWeight.BOLD, color="black")),
            ft.DataColumn(ft.Text("Insc. Estadual", weight=ft.FontWeight.BOLD, color="black")),
            ft.DataColumn(ft.Text("Contato Distribuidor", weight=ft.FontWeight.BOLD, color="black")),
            ft.DataColumn(ft.Text("Telefone Distribuidor", weight=ft.FontWeight.BOLD, color="black")),
            ft.DataColumn(ft.Text("Celular", weight=ft.FontWeight.BOLD, color="black")),
            ft.DataColumn(ft.Text("Fax", weight=ft.FontWeight.BOLD, color="black")),
            ft.DataColumn(ft.Text("Sede Distribuidor", weight=ft.FontWeight.BOLD, color="black")),
            ft.DataColumn(ft.Text("Cidade", weight=ft.FontWeight.BOLD, color="black")),
            ft.DataColumn(ft.Text("UF Dist.", weight=ft.FontWeight.BOLD, color="black")),
            ft.DataColumn(ft.Text("CEP", weight=ft.FontWeight.BOLD, color="black")),
            ft.DataColumn(ft.Text("Email", weight=ft.FontWeight.BOLD, color="black")),
        ],
        rows=[],
    )

    # Controles de paginação
    page_info = ft.Text("Página 1 de 1", size=11, color="black", weight=ft.FontWeight.W_500)
    prev_button = ft.IconButton(
        icon=ft.icons.ARROW_BACK,
        on_click=lambda _: change_page(-1),
        disabled=True,
        icon_color="black"
    )
    next_button = ft.IconButton(
        icon=ft.icons.ARROW_FORWARD,
        on_click=lambda _: change_page(1),
        disabled=True,
        icon_color="black"
    )
    
    # Campo ir para página
    def on_submit(e):
        go_to_page(None)
    
    goto_page = ft.TextField(
        width=60,
        height=35,
        text_size=11,
        content_padding=5,
        text_align=ft.TextAlign.CENTER,
        keyboard_type=ft.KeyboardType.NUMBER,
        on_submit=on_submit,
        border_color="black",
        cursor_color="black",
        focused_border_color="black",
        focused_color="black",
        bgcolor="white",  # Set background to white
        color="black"    # Set text color to black
    )
    
    def go_to_page(e):
        try:
            page_num = int(goto_page.value)
            if 1 <= page_num <= state.total_pages:
                state.current_page = page_num
                load_page_data()
                goto_page.error_text = None
            else:
                goto_page.error_text = f"1-{state.total_pages}"
        except ValueError:
            goto_page.error_text = "Inválido"
        page.update()
    
    goto_button = ft.IconButton(
        icon=ft.icons.KEYBOARD_RETURN,
        on_click=go_to_page,
        tooltip="Ir para página",
        icon_color="black"
    )

    pagination_row = ft.Container(
        content=ft.Row(
            [
                prev_button,
                page_info,
                next_button,
                ft.Text("Ir para:", size=11, color="black", weight=ft.FontWeight.W_500),
                goto_page,
                goto_button
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        ),
        bgcolor=None,
        padding=10
    )

    def update_pagination_info():
        total_items = len(data_table.all_rows)
        state.total_pages = (total_items + state.items_per_page - 1) // state.items_per_page
        page_info.value = f"Página {state.current_page} de {state.total_pages}"
        prev_button.disabled = state.current_page <= 1
        next_button.disabled = state.current_page >= state.total_pages

    def change_page(delta):
        state.current_page += delta
        load_page_data()
        page.update()

    def load_page_data():
        start_idx = (state.current_page - 1) * state.items_per_page
        end_idx = start_idx + state.items_per_page
        
        # Atualizar linhas da tabela
        data_table.rows = state.filtered_rows[start_idx:end_idx]
        
        # Atualizar informações de paginação
        state.total_pages = (len(state.filtered_rows) + state.items_per_page - 1) // state.items_per_page
        page_info.value = f"Página {state.current_page} de {state.total_pages}"
        
        # Atualizar estado dos botões
        prev_button.disabled = state.current_page <= 1
        next_button.disabled = state.current_page >= state.total_pages
        
        # Limpar campo ir para página
        goto_page.value = ""
        goto_page.error_text = None

    search_field = ft.TextField(
        label="Buscar",
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
        on_change=lambda e: filter_table(e.control.value if e.control.value else ""),
    )
    setattr(page, 'search_field', search_field)

    clear_button = ft.ElevatedButton(
        text="Limpar Filtros",
        style=ft.ButtonStyle(
            bgcolor={"": "#2196F3"},
            color={"": "white"},
        ),
        on_click=lambda _: clear_filters(),
    )

    def clear_filters():
        if hasattr(page, 'search_field'):
            page.search_field.value = ""
            state.filtered_rows = state.original_rows.copy()
            state.current_page = 1
            load_page_data()
            page.update()

    def filter_table(search_term):
        if not search_term:
            state.filtered_rows = state.original_rows.copy()
            state.current_page = 1
            load_page_data()
            page.update()
            return

        filtered_rows = []
        search_term = search_term.upper()
        for row in state.original_rows:
            row_text = ""
            for cell in row.cells:
                if isinstance(cell.content, ft.Container):
                    row_text += str(cell.content.content.tooltip).upper() + " "
                else:
                    row_text += str(cell.content.value).upper() + " "
            if row_text.startswith(search_term):
                filtered_rows.append(row)

        state.filtered_rows = filtered_rows
        state.current_page = 1
        load_page_data()
        page.update()

    def generate_kml(e):
        try:
            # Criar uma lista para armazenar os dados das linhas
            data_list = []
            
            # Iterar sobre todas as linhas da tabela
            for row in data_table.all_rows:
                row_data = {}
                # Extrair os dados das células
                row_data['MUNICIPIO_UF'] = row.cells[0].content.value
                row_data['MUNICIPIO'] = row.cells[1].content.value
                row_data['UF'] = row.cells[2].content.value
                row_data['POPULACAO'] = row.cells[3].content.value
                # Para as coordenadas, precisamos acessar o Text dentro do Container
                row_data['COORDENADAS'] = row.cells[4].content.content.tooltip
                row_data['UNIDADE'] = row.cells[5].content.value
                row_data['TIPO UNIDADE'] = row.cells[6].content.value
                row_data['RAZAO SOCIAL'] = row.cells[7].content.value
                row_data['CNPJ'] = row.cells[8].content.value
                row_data['NOME_FANTASIA'] = row.cells[9].content.value
                row_data['RESPONSAVEL'] = row.cells[10].content.value
                row_data['CONTATO RESPONSAVEL'] = row.cells[11].content.value
                row_data['CONTRATO'] = row.cells[12].content.value
                row_data['CODIGO'] = row.cells[13].content.value
                row_data['DISTRIBUIDOR_OUTROS'] = row.cells[14].content.value
                row_data['INSC_ESTADUAL'] = row.cells[15].content.value
                row_data['CONTATO DISTRIBUIDOR'] = row.cells[16].content.value
                row_data['TELEFONE_DISTRIBUIDOR'] = row.cells[17].content.value
                row_data['CELULAR'] = row.cells[18].content.value
                row_data['FAX'] = row.cells[19].content.value
                row_data['SEDE DISTRIBUIDOR'] = row.cells[20].content.value
                row_data['CIDADE'] = row.cells[21].content.value
                row_data['UF_DISTRIBUIDOR'] = row.cells[22].content.value
                row_data['CEP'] = row.cells[23].content.value
                row_data['EMAIL'] = row.cells[24].content.value
                data_list.append(row_data)
            
            # Criar DataFrame com os dados
            import pandas as pd
            df = pd.DataFrame(data_list)
            
            # Instanciar KMLGenerator com o DataFrame
            generator = KMLGenerator(df)
            
            # Gerar o arquivo KML
            generator.gerar_kml_unificado()
            
            status_text.value = "Arquivo KML gerado com sucesso!"
            page.update()
            
        except Exception as e:
            logging.error(f"Erro ao gerar KML: {str(e)}")
            status_text.value = f"Erro ao gerar KML: {str(e)}"
            page.update()

    generate_kml_button = ft.ElevatedButton(
        "Gerar KML",
        on_click=generate_kml,
        style=ft.ButtonStyle(
            bgcolor={"": ft.colors.GREEN},
            color={"": ft.colors.WHITE},
        ),
    )

    def truncate_text(text, max_length=50):
        """Trunca o texto se ele for maior que max_length"""
        if not text:
            return ""
        text = str(text)
        if len(text) > max_length:
            return text[:max_length] + "..."
        return text

    def load_table_data():
        try:
            logging.info("Iniciando carregamento dos dados...")
            data = crud_manager.get_page_data()
            logging.info(f"Dados obtidos: {len(data) if data else 0} registros")
            
            rows = []
            for row in data:
                # Converter população para inteiro e formatar
                try:
                    if row[3]:
                        # Remove pontos existentes e converte para inteiro
                        pop_str = str(row[3]).replace('.', '')
                        pop_int = int(pop_str)
                        populacao = f"{pop_int:,d}".replace(',', '.')
                    else:
                        populacao = "0"
                except (ValueError, TypeError):
                    populacao = "0"
                
                rows.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(truncate_text(str(row[0] or ""), 20), color="black", weight=ft.FontWeight.W_500, size=11), show_edit_icon=False),  # municipio_uf
                            ft.DataCell(ft.Text(truncate_text(str(row[1] or ""), 20), color="black", weight=ft.FontWeight.W_500, size=11), show_edit_icon=False),  # municipio
                            ft.DataCell(ft.Text(truncate_text(str(row[2] or ""), 20), color="black", weight=ft.FontWeight.W_500, size=11), show_edit_icon=False),  # uf
                            ft.DataCell(ft.Text(truncate_text(str(populacao), 20), color="black", weight=ft.FontWeight.W_500, size=11), show_edit_icon=False),     # populacao
                            ft.DataCell(
                                ft.Container(
                                    content=ft.Text(
                                        truncate_text(str(row[4] or ""), 30),
                                        color="black",
                                        weight=ft.FontWeight.W_500,
                                        size=11,
                                        tooltip=str(row[4] or ""),
                                    ),
                                    width=350,
                                ),
                                show_edit_icon=False
                            ),  # coordenadas
                            ft.DataCell(ft.Text(truncate_text(str(row[5] or ""), 20), color="black", weight=ft.FontWeight.W_500, size=11), show_edit_icon=False),  # unidade
                            ft.DataCell(ft.Text(truncate_text(str(row[6] or ""), 20), color="black", weight=ft.FontWeight.W_500, size=11), show_edit_icon=False),  # tipo_unidade
                            ft.DataCell(ft.Text(truncate_text(str(row[7] or ""), 20), color="black", weight=ft.FontWeight.W_500, size=11), show_edit_icon=False),  # razao_social_atendido
                            ft.DataCell(ft.Text(truncate_text(str(row[8] or ""), 20), color="black", weight=ft.FontWeight.W_500, size=11), show_edit_icon=False),  # cnpj
                            ft.DataCell(ft.Text(truncate_text(str(row[9] or ""), 20), color="black", weight=ft.FontWeight.W_500, size=11), show_edit_icon=False),  # nome_fantasia
                            ft.DataCell(ft.Text(truncate_text(str(row[10] or ""), 20), color="black", weight=ft.FontWeight.W_500, size=11), show_edit_icon=False), # responsavel
                            ft.DataCell(ft.Text(truncate_text(str(row[11] or ""), 20), color="black", weight=ft.FontWeight.W_500, size=11), show_edit_icon=False), # telefone_responsavel
                            ft.DataCell(ft.Text(truncate_text(str(row[12] or ""), 20), color="black", weight=ft.FontWeight.W_500, size=11), show_edit_icon=False), # contrato
                            ft.DataCell(ft.Text(truncate_text(str(row[13] or ""), 20), color="black", weight=ft.FontWeight.W_500, size=11), show_edit_icon=False), # codigo
                            ft.DataCell(ft.Text(truncate_text(str(row[14] or ""), 20), color="black", weight=ft.FontWeight.W_500, size=11), show_edit_icon=False), # distribuidor_outros
                            ft.DataCell(ft.Text(truncate_text(str(row[15] or ""), 20), color="black", weight=ft.FontWeight.W_500, size=11), show_edit_icon=False), # insc_estadual
                            ft.DataCell(ft.Text(truncate_text(str(row[16] or ""), 20), color="black", weight=ft.FontWeight.W_500, size=11), show_edit_icon=False), # contato
                            ft.DataCell(ft.Text(truncate_text(str(row[17] or ""), 20), color="black", weight=ft.FontWeight.W_500, size=11), show_edit_icon=False), # telefone_distribuidor
                            ft.DataCell(ft.Text(truncate_text(str(row[18] or ""), 20), color="black", weight=ft.FontWeight.W_500, size=11), show_edit_icon=False), # celular
                            ft.DataCell(ft.Text(truncate_text(str(row[19] or ""), 20), color="black", weight=ft.FontWeight.W_500, size=11), show_edit_icon=False), # fax
                            ft.DataCell(ft.Text(truncate_text(str(row[20] or ""), 20), color="black", weight=ft.FontWeight.W_500, size=11), show_edit_icon=False), # endereco
                            ft.DataCell(ft.Text(truncate_text(str(row[21] or ""), 20), color="black", weight=ft.FontWeight.W_500, size=11), show_edit_icon=False), # cidade
                            ft.DataCell(ft.Text(truncate_text(str(row[22] or ""), 20), color="black", weight=ft.FontWeight.W_500, size=11), show_edit_icon=False), # uf_distribuidor
                            ft.DataCell(ft.Text(truncate_text(str(row[23] or ""), 20), color="black", weight=ft.FontWeight.W_500, size=11), show_edit_icon=False), # cep
                            ft.DataCell(ft.Text(truncate_text(str(row[24] or ""), 20), color="black", weight=ft.FontWeight.W_500, size=11), show_edit_icon=False), # email
                        ]
                    )
                )
            
            state.original_rows = rows.copy()
            state.filtered_rows = rows.copy()
            data_table.rows = rows[:state.items_per_page]
            data_table.all_rows = rows
            state.current_page = 1
            update_pagination_info()
            
        except Exception as e:
            logging.error(f"Erro ao carregar dados: {str(e)}")
            status_text.value = f"Erro ao carregar dados: {str(e)}"

    # Criar o layout principal começando com loading
    main_container = ft.Container(
        content=create_loading_view(),
        padding=20,
        expand=True,
    )

    def load_table_data():
        try:
            logging.info("Iniciando carregamento dos dados...")
            data = crud_manager.get_page_data()
            logging.info(f"Dados obtidos: {len(data) if data else 0} registros")
            
            rows = []
            for row in data:
                # Converter população para inteiro e formatar
                try:
                    if row[3]:
                        # Remove pontos existentes e converte para inteiro
                        pop_str = str(row[3]).replace('.', '')
                        pop_int = int(pop_str)
                        populacao = f"{pop_int:,d}".replace(',', '.')
                    else:
                        populacao = "0"
                except (ValueError, TypeError):
                    populacao = "0"
                
                rows.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(truncate_text(str(row[0] or ""), 20), color="black", weight=ft.FontWeight.W_500, size=11), show_edit_icon=False),  # municipio_uf
                            ft.DataCell(ft.Text(truncate_text(str(row[1] or ""), 20), color="black", weight=ft.FontWeight.W_500, size=11), show_edit_icon=False),  # municipio
                            ft.DataCell(ft.Text(truncate_text(str(row[2] or ""), 20), color="black", weight=ft.FontWeight.W_500, size=11), show_edit_icon=False),  # uf
                            ft.DataCell(ft.Text(truncate_text(str(populacao), 20), color="black", weight=ft.FontWeight.W_500, size=11), show_edit_icon=False),     # populacao
                            ft.DataCell(
                                ft.Container(
                                    content=ft.Text(
                                        truncate_text(str(row[4] or ""), 30),
                                        color="black",
                                        weight=ft.FontWeight.W_500,
                                        size=11,
                                        tooltip=str(row[4] or ""),
                                    ),
                                    width=350,
                                ),
                                show_edit_icon=False
                            ),  # coordenadas
                            ft.DataCell(ft.Text(truncate_text(str(row[5] or ""), 20), color="black", weight=ft.FontWeight.W_500, size=11), show_edit_icon=False),  # unidade
                            ft.DataCell(ft.Text(truncate_text(str(row[6] or ""), 20), color="black", weight=ft.FontWeight.W_500, size=11), show_edit_icon=False),  # tipo_unidade
                            ft.DataCell(ft.Text(truncate_text(str(row[7] or ""), 20), color="black", weight=ft.FontWeight.W_500, size=11), show_edit_icon=False),  # razao_social_atendido
                            ft.DataCell(ft.Text(truncate_text(str(row[8] or ""), 20), color="black", weight=ft.FontWeight.W_500, size=11), show_edit_icon=False),  # cnpj
                            ft.DataCell(ft.Text(truncate_text(str(row[9] or ""), 20), color="black", weight=ft.FontWeight.W_500, size=11), show_edit_icon=False),  # nome_fantasia
                            ft.DataCell(ft.Text(truncate_text(str(row[10] or ""), 20), color="black", weight=ft.FontWeight.W_500, size=11), show_edit_icon=False), # responsavel
                            ft.DataCell(ft.Text(truncate_text(str(row[11] or ""), 20), color="black", weight=ft.FontWeight.W_500, size=11), show_edit_icon=False), # telefone_responsavel
                            ft.DataCell(ft.Text(truncate_text(str(row[12] or ""), 20), color="black", weight=ft.FontWeight.W_500, size=11), show_edit_icon=False), # contrato
                            ft.DataCell(ft.Text(truncate_text(str(row[13] or ""), 20), color="black", weight=ft.FontWeight.W_500, size=11), show_edit_icon=False), # codigo
                            ft.DataCell(ft.Text(truncate_text(str(row[14] or ""), 20), color="black", weight=ft.FontWeight.W_500, size=11), show_edit_icon=False), # distribuidor_outros
                            ft.DataCell(ft.Text(truncate_text(str(row[15] or ""), 20), color="black", weight=ft.FontWeight.W_500, size=11), show_edit_icon=False), # insc_estadual
                            ft.DataCell(ft.Text(truncate_text(str(row[16] or ""), 20), color="black", weight=ft.FontWeight.W_500, size=11), show_edit_icon=False), # contato
                            ft.DataCell(ft.Text(truncate_text(str(row[17] or ""), 20), color="black", weight=ft.FontWeight.W_500, size=11), show_edit_icon=False), # telefone_distribuidor
                            ft.DataCell(ft.Text(truncate_text(str(row[18] or ""), 20), color="black", weight=ft.FontWeight.W_500, size=11), show_edit_icon=False), # celular
                            ft.DataCell(ft.Text(truncate_text(str(row[19] or ""), 20), color="black", weight=ft.FontWeight.W_500, size=11), show_edit_icon=False), # fax
                            ft.DataCell(ft.Text(truncate_text(str(row[20] or ""), 20), color="black", weight=ft.FontWeight.W_500, size=11), show_edit_icon=False), # endereco
                            ft.DataCell(ft.Text(truncate_text(str(row[21] or ""), 20), color="black", weight=ft.FontWeight.W_500, size=11), show_edit_icon=False), # cidade
                            ft.DataCell(ft.Text(truncate_text(str(row[22] or ""), 20), color="black", weight=ft.FontWeight.W_500, size=11), show_edit_icon=False), # uf_distribuidor
                            ft.DataCell(ft.Text(truncate_text(str(row[23] or ""), 20), color="black", weight=ft.FontWeight.W_500, size=11), show_edit_icon=False), # cep
                            ft.DataCell(ft.Text(truncate_text(str(row[24] or ""), 20), color="black", weight=ft.FontWeight.W_500, size=11), show_edit_icon=False), # email
                        ]
                    )
                )
            
            state.original_rows = rows.copy()
            state.filtered_rows = rows.copy()
            data_table.rows = rows[:state.items_per_page]
            data_table.all_rows = rows
            state.current_page = 1
            update_pagination_info()
            
            # Atualizar container com os dados
            main_container.content = ft.Column(
                [
                    ft.Container(
                        content=ft.Text(
                            "Dados dos Municípios Atendidos",
                            size=24,
                            weight=ft.FontWeight.BOLD,
                            color="#2196F3",
                            text_align=ft.TextAlign.CENTER,
                        ),
                        alignment=ft.alignment.center,
                    ),
                    ft.Row(
                        [search_field, clear_button, generate_kml_button],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    ft.Container(
                        content=ft.Column(
                            [
                                ft.Container(
                                    content=ft.Row(
                                        [data_table],
                                        scroll=ft.ScrollMode.AUTO,
                                        alignment=ft.MainAxisAlignment.CENTER,
                                    ),
                                    padding=10,
                                    border_radius=8,
                                    expand=True,
                                    height=700,
                                ),
                                pagination_row,
                                status_text,
                            ],
                            spacing=10,
                            expand=True,
                        ),
                        expand=True,
                        bgcolor=None,
                        height=750,
                    ),
                ],
                expand=True,
            )
            page.update()
            
        except Exception as e:
            logging.error(f"Erro ao carregar dados: {str(e)}")
            status_text.value = f"Erro ao carregar dados: {str(e)}"

    # Carregar dados iniciais
    load_table_data()

    return ft.Column(controls=[main_container])
