"""
Funções utilitárias para o projeto
"""
import os
import hashlib
import colorsys
import pandas as pd
from pathlib import Path

import sqlite3
import pandas as pd
from pathlib import Path

def carregar_dados_unificados():
    """
    Carrega os dados unificados do banco de dados
    """
    try:
        # Conectar ao banco de dados
        conn = sqlite3.connect('database/database.db')
        
        # Executar query
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
        df = pd.read_sql_query(query, conn)
        
        # Renomear colunas
        df = df.rename(columns={
            'razao_social': 'RAZAO SOCIAL',
            'tipo_unidade': 'TIPO UNIDADE',
            'unidade': 'UNIDADE',
            'contato': 'CONTATO DISTRIBUIDOR',
            'responsavel': 'RESPONSAVEL',
            'telefone_responsavel': 'CONTATO RESPONSAVEL',
            'endereco': 'SEDE DISTRIBUIDOR',
            'coordenadas': 'COORDENADAS'
        })
        
        # Fechar conexão
        conn.close()
        
        return df
        
    except Exception as e:
        print(f"Erro ao carregar dados: {str(e)}")
        return None

def get_downloads_path():
    """Retorna o caminho da pasta Downloads"""
    return str(Path.home() / "Downloads")

def format_value(value, is_population=False):
    """
    Formata um valor para exibição
    """
    
    if is_population:
        try:
            value = int(str(value).replace('.', ''))
            return "{:,}".format(value).replace(',', '.')
        except:
            return str(value)
    
    return str(value)

def criar_pasta_kml(base_path=None):
    """
    Cria a pasta para salvar os arquivos KML
    
    Args:
        base_path (str, optional): Caminho base onde criar a pasta KML. 
            Se não fornecido, usa a pasta Downloads.
    """
    # Obter o caminho da pasta Downloads se base_path não fornecido
    if base_path is None:
        base_path = str(Path.home() / "Downloads")
    
    # Criar pasta KML se não existir
    output_dir = os.path.join(base_path, "KML")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    return output_dir

def gerar_cor_unica(texto):
    """
    Gera uma cor única baseada no texto
    """
    # Usar hash para gerar um número único para cada texto
    hash_obj = hashlib.md5(texto.encode())
    hash_hex = hash_obj.hexdigest()
    
    # Converter os primeiros 6 caracteres do hash para um número entre 0 e 1
    hue = int(hash_hex[:6], 16) / 0xFFFFFF
    
    # Converter HSV para RGB
    rgb = colorsys.hsv_to_rgb(hue, 0.7, 0.8)  # Saturação e valor fixos
    
    # Converter RGB para formato KML (aabbggrr)
    r = int(rgb[0] * 255)
    g = int(rgb[1] * 255)
    b = int(rgb[2] * 255)
    a = 200  # Alpha fixo em ~78%
    
    return f'{a:02x}{b:02x}{g:02x}{r:02x}'

def get_color_for_unit(unit_name, unit_type):
    """Gera uma cor única para a unidade baseada no nome"""
    # Usar hash para gerar um número único para cada nome
    hash_obj = hashlib.md5(unit_name.encode())
    hash_int = int(hash_obj.hexdigest(), 16)
    
    # Ajustar a cor base de acordo com o tipo de unidade
    if unit_type == 'Regional':
        hue = (hash_int % 100) / 100.0  # Variação no tom
        saturation = 0.8  # Alta saturação
        value = 0.8  # Brilho moderado
    elif unit_type == 'Filial':
        hue = ((hash_int + 50) % 100) / 100.0  # Tom diferente
        saturation = 0.6  # Saturação média
        value = 0.9  # Brilho alto
    else:  # Em Branco
        hue = 0  # Sem tom
        saturation = 0  # Sem saturação
        value = 0.7  # Brilho médio
    
    # Converter HSV para RGB
    rgb = colorsys.hsv_to_rgb(hue, saturation, value)
    
    # Converter RGB para ABGR (formato do KML)
    abgr = f'{int(rgb[2]*255):02x}{int(rgb[1]*255):02x}{int(rgb[0]*255):02x}'
    
    return abgr