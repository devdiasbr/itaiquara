import pandas as pd
import os
import sqlite3
from pathlib import Path
import logging

def check_duplicates(df, sheet_name):
    """
    Verifica e mostra duplicatas em uma coluna específica
    """
    if sheet_name == 'DISTRIBUIDORES':
        duplicates = df[df['RAZAO SOCIAL'].duplicated(keep=False)]
        if not duplicates.empty:
            print("\nRazões Sociais duplicadas encontradas:")
            for _, row in duplicates.sort_values('RAZAO SOCIAL').iterrows():
                print(f"Razão Social: {row['RAZAO SOCIAL']}")
                print(f"CNPJ: {row['CNPJ']}")
                print(f"Nome Fantasia: {row['NOME FANTASIA']}")
                print("-" * 50)

def load_excel_sheets():
    """
    Carrega todas as abas do arquivo Excel BASE_DADOS.xlsx em DataFrames separados
    Returns:
        dict: Dicionário com nome da aba como chave e DataFrame como valor
    """
    # Caminho absoluto para o arquivo Excel
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, 'BASE_DADOS.xlsx')
    
    try:
        # Lê todas as abas do Excel
        excel_file = pd.ExcelFile(file_path)
        
        # Dicionário para armazenar os DataFrames
        dataframes = {}
        
        # Carrega cada aba em um DataFrame separado
        for sheet_name in excel_file.sheet_names:
            print(f"\nCarregando aba: {sheet_name}")
            df = pd.read_excel(excel_file, sheet_name=sheet_name)
            
            # Remove linhas completamente vazias
            df = df.dropna(how='all')
            
            # Verifica duplicatas
            check_duplicates(df, sheet_name)
            
            dataframes[sheet_name] = df
            print(f"Shape da aba {sheet_name}: {df.shape}")
            print(f"Colunas: {df.columns.tolist()}")
            
        return dataframes
    
    except Exception as e:
        print(f"Erro ao carregar o arquivo: {str(e)}")
        return None

def create_sqlite_database(dataframes):
    """
    Cria um banco de dados SQLite com os DataFrames e suas relações
    Args:
        dataframes (dict): Dicionário com nome da aba como chave e DataFrame como valor
    """
    try:
        # Criar pasta database se não existir
        db_dir = Path(__file__).parent / 'database'
        db_dir.mkdir(exist_ok=True)
        db_path = db_dir / 'database.db'
        
        # Remove o banco de dados se já existir
        if db_path.exists():
            db_path.unlink()
            print(f"Banco de dados anterior removido: {db_path}")
        
        # Cria conexão com o banco de dados
        conn = sqlite3.connect(db_path)
        print(f"Banco de dados criado: {db_path}")
        
        # Criar tabelas com chaves primárias apropriadas
        cursor = conn.cursor()
        
        # 1. Criar tabela municipios
        print("\nCriando tabela municipios...")
        cursor.execute("""
            CREATE TABLE municipios (
                municipio_uf TEXT PRIMARY KEY,
                municipio TEXT NOT NULL,
                uf TEXT NOT NULL,
                populacao TEXT,
                coordenadas TEXT,
                descricao TEXT
            )
        """)
        
        # 2. Criar tabela distribuidores
        print("Criando tabela distribuidores...")
        cursor.execute("""
            CREATE TABLE distribuidores (
                cnpj TEXT PRIMARY KEY,
                razao_social TEXT NOT NULL,
                responsavel TEXT,
                telefone_responsavel TEXT,
                contrato TEXT,
                codigo TEXT,
                distribuidor_outros TEXT,
                nome_fantasia TEXT,
                insc_estadual TEXT,
                contato TEXT,
                telefone_distribuidor TEXT,
                celular TEXT,
                fax TEXT,
                endereco TEXT,
                cidade TEXT,
                uf TEXT,
                cep TEXT,
                email TEXT
            )
        """)
        
        # 3. Criar tabela atendidos
        print("Criando tabela atendidos...")
        cursor.execute("""
            CREATE TABLE atendidos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                municipio_uf TEXT,
                unidade TEXT,
                tipo_unidade TEXT,
                razao_social_atendido TEXT,
                cnpj_distribuidor TEXT,
                FOREIGN KEY (municipio_uf) REFERENCES municipios(municipio_uf),
                FOREIGN KEY (cnpj_distribuidor) REFERENCES distribuidores(cnpj)
            )
        """)
        
        # Inserir dados nas tabelas
        print("\nInserindo dados nas tabelas...")
        
        # 1. Inserir municípios
        df_municipios = dataframes['MUNICIPIOS']
        for _, row in df_municipios.iterrows():
            # Garantir que coordenadas não seja None
            coordenadas = row['COORDENADAS'] if pd.notna(row['COORDENADAS']) else ''
            cursor.execute("""
                INSERT INTO municipios (municipio_uf, municipio, uf, populacao, coordenadas, descricao)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (row['MUNICIPIO_UF'], row['MUNICIPIO'], row['UF'], row['POPULACAO'], coordenadas, row['DESCRICAO']))
        
        # 2. Inserir distribuidores
        df_dist = dataframes['DISTRIBUIDORES']
        for _, row in df_dist.iterrows():
            cursor.execute("""
                INSERT INTO distribuidores (
                    cnpj, razao_social, responsavel, telefone_responsavel, contrato, codigo,
                    distribuidor_outros, nome_fantasia, insc_estadual,
                    contato, telefone_distribuidor, celular, fax, endereco, cidade,
                    uf, cep, email
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                row['CNPJ'], row['RAZAO SOCIAL'], row['RESPONSAVEL'], row['TELEFONE RESPONSAVEL'], 
                row['CONTRATO'], row['CÓDIGO'], row['DISTRIBUIDOR / OUTROS'],
                row['NOME FANTASIA'], row['INSC. ESTADUAL'],
                row['CONTATO'], row['TELEFONE DISTRIBUIDOR'], row['CELULAR'], row['FAX'],
                row['ENDEREÇO'], row['CIDADE '], row['UF'], row['CEP'], row['E-MAIL']
            ))
        
        # 3. Inserir atendidos
        df_atendidos = dataframes['MUNICIPIOS_ATENDIDOS']
        for _, row in df_atendidos.iterrows():
            # Buscar o CNPJ do distribuidor pela razão social
            cursor.execute("SELECT cnpj FROM distribuidores WHERE razao_social = ?", (row['RAZAO SOCIAL'],))
            result = cursor.fetchone()
            cnpj_distribuidor = result[0] if result else None
            
            if cnpj_distribuidor:
                # Determinar o tipo de unidade baseado na unidade
                tipo_unidade = 'REGIONAL' if 'REGIONAL' in str(row['UNIDADE']).upper() else 'FILIAL'
                
                cursor.execute("""
                    INSERT INTO atendidos (municipio_uf, unidade, tipo_unidade, razao_social_atendido, cnpj_distribuidor)
                    VALUES (?, ?, ?, ?, ?)
                """, (row['MUNICIPIO_UF'], row['UNIDADE'], tipo_unidade, row['RAZAO SOCIAL'], cnpj_distribuidor))
        
        # Commit das alterações
        conn.commit()
        print("\nDados inseridos com sucesso!")
        
    except Exception as e:
        print(f"Erro ao criar banco de dados: {str(e)}")
        conn.rollback()
    finally:
        conn.close()
        print("\nConexão com o banco de dados fechada")

def get_db_path():
    """Retorna o caminho do banco de dados"""
    return Path(__file__).parent / 'database' / 'database.db'

def load_data():
    """
    Carrega os dados do banco de dados e retorna um DataFrame
    """
    try:
        # Conectar ao banco de dados
        conn = sqlite3.connect(get_db_path())
        
        # Executar a query
        query = """
            SELECT 
                m.municipio_uf as 'MUNICIPIO_UF',
                m.municipio as 'MUNICIPIO',
                m.uf as 'UF',
                m.populacao as 'POPULACAO',
                m.coordenadas as 'COORDENADAS',
                a.unidade as 'UNIDADE',
                a.tipo_unidade as 'TIPO UNIDADE',
                d.razao_social as 'RAZAO SOCIAL',
                d.cnpj as 'CNPJ',
                d.nome_fantasia as 'NOME_FANTASIA',
                d.responsavel as 'RESPONSAVEL',
                d.telefone_responsavel as 'CONTATO RESPONSAVEL',
                d.contrato as 'CONTRATO',
                d.codigo as 'CODIGO',
                d.distribuidor_outros as 'DISTRIBUIDOR_OUTROS',
                d.insc_estadual as 'INSC_ESTADUAL',
                d.contato as 'CONTATO DISTRIBUIDOR',
                d.telefone_distribuidor as 'TELEFONE_DISTRIBUIDOR',
                d.celular as 'CELULAR',
                d.fax as 'FAX',
                d.endereco as 'SEDE DISTRIBUIDOR',
                d.cidade as 'CIDADE',
                d.uf as 'UF_DISTRIBUIDOR',
                d.cep as 'CEP',
                d.email as 'EMAIL'
            FROM municipios m
            LEFT JOIN atendidos a ON m.municipio_uf = a.municipio_uf
            LEFT JOIN distribuidores d ON a.cnpj_distribuidor = d.cnpj
            ORDER BY m.municipio_uf
        """
        
        # Carregar os dados em um DataFrame
        df = pd.read_sql_query(query, conn)
        
        # Preencher valores nulos
        df['TIPO UNIDADE'] = df['TIPO UNIDADE'].fillna('EM BRANCO')
        df['UNIDADE'] = df['UNIDADE'].fillna('EM BRANCO')
        df['RAZAO SOCIAL'] = df['RAZAO SOCIAL'].fillna('EM BRANCO')
        
        # Fechar a conexão
        conn.close()
        
        logging.info(f"Dados obtidos: {len(df)} registros")
        return df
        
    except Exception as e:
        logging.error(f"Erro ao carregar dados: {str(e)}")
        raise

def carregar_dados_unificados():
    """
    Carrega os dados unificados das tabelas municipios, atendidos e distribuidores
    """
    # Query SQL para unificar os dados
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
    
    try:
        # Conectar ao banco de dados
        conn = sqlite3.connect(get_db_path())
        
        # Carregar os dados em um DataFrame
        df = pd.read_sql_query(query, conn)
        
        # Debug: verificar dados das coordenadas
        logging.info("Amostra de coordenadas:")
        sample_coords = df['coordenadas'].head()
        for i, coord in enumerate(sample_coords):
            logging.info(f"Coordenada {i}: {coord}")
        
        # Ajustar os nomes das colunas para o formato esperado pelo gerador KML
        df = df.rename(columns={
            'razao_social': 'RAZAO SOCIAL',
            'tipo_unidade': 'TIPO UNIDADE',
            'unidade': 'UNIDADE',
            'municipio': 'MUNICIPIO',
            'uf': 'UF',
            'populacao': 'POPULACAO',
            'coordenadas': 'COORDENADAS',
            'telefone_distribuidor': 'CONTATO DISTRIBUIDOR',
            'responsavel': 'RESPONSAVEL',
            'telefone_responsavel': 'CONTATO RESPONSAVEL',
            'endereco': 'SEDE DISTRIBUIDOR'
        })
        
        return df
        
    except Exception as e:
        print(f"Erro ao carregar dados: {str(e)}")
        return None
    finally:
        conn.close()

if __name__ == "__main__":
    # Carrega os DataFrames
    print("Carregando dados do Excel...")
    dfs = load_excel_sheets()
    
    if dfs:
        print("\nCriando banco de dados SQLite com relações...")
        create_sqlite_database(dfs)
        print("\nCarregando dados unificados...")
        df_unificado = carregar_dados_unificados()
        
        if df_unificado is not None:
            print("\nMunicípios e suas coordenadas:")
            print(df_unificado[['MUNICIPIO', 'COORDENADAS']].head(10))