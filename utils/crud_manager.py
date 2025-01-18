import sqlite3
import logging
import os

class CRUDManager:
    def __init__(self, db_path=None):
        if db_path is None:
            self.db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'database', 'database.db')
        else:
            self.db_path = db_path
            
        if not os.path.exists(self.db_path):
            raise FileNotFoundError(f"Banco de dados não encontrado: {self.db_path}")
        logging.info(f"Banco de dados encontrado: {self.db_path}")
        
    def add_municipality(self, data):
        """Adiciona um novo município ao banco de dados"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Primeiro, adicionar o município
            municipio_query = """
            INSERT INTO municipios (municipio_uf, municipio, uf, populacao)
            VALUES (?, ?, ?, ?)
            """
            cursor.execute(municipio_query, (
                data['municipio_uf'],
                data['municipio'],
                data['uf'],
                data['populacao']
            ))
            
            # Depois, adicionar a relação com o distribuidor
            atendido_query = """
            INSERT INTO municipios_atendidos (municipio_uf, unidade, razao_social)
            VALUES (?, ?, ?)
            """
            cursor.execute(atendido_query, (
                data['municipio_uf'],
                data['unidade'],
                data['distribuidor']
            ))
            
            conn.commit()
            conn.close()
            logging.info(f"Município adicionado com sucesso: {data['municipio_uf']}")
            return True
            
        except Exception as e:
            logging.error(f"Erro ao adicionar município: {e}")
            return False
            
    def get_all_municipalities(self):
        """Retorna todos os municípios do banco de dados"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            query = """
            SELECT m.municipio_uf, m.municipio, m.uf, m.populacao, 
                   ma.unidade, ma.razao_social
            FROM municipios m
            LEFT JOIN municipios_atendidos ma ON m.municipio_uf = ma.municipio_uf
            """
            
            cursor.execute(query)
            results = cursor.fetchall()
            conn.close()
            
            return results
            
        except Exception as e:
            logging.error(f"Erro ao buscar municípios: {e}")
            return []
            
    def get_municipality(self, municipio_uf):
        """Retorna os dados de um município específico"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            query = """
            SELECT m.municipio_uf, m.municipio, m.uf, m.populacao, 
                   ma.unidade, ma.razao_social
            FROM municipios m
            LEFT JOIN municipios_atendidos ma ON m.municipio_uf = ma.municipio_uf
            WHERE m.municipio_uf = ?
            """
            
            cursor.execute(query, (municipio_uf,))
            result = cursor.fetchone()
            conn.close()
            
            return result
            
        except Exception as e:
            logging.error(f"Erro ao buscar município {municipio_uf}: {e}")
            return None
            
    def update_municipality(self, data):
        """Atualiza os dados de um município"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Atualizar dados na tabela municipios
            municipio_query = """
            UPDATE municipios 
            SET municipio = ?, uf = ?, populacao = ?
            WHERE municipio_uf = ?
            """
            cursor.execute(municipio_query, (
                data['municipio'],
                data['uf'],
                data['populacao'],
                data['municipio_uf']
            ))
            
            # Atualizar dados na tabela municipios_atendidos
            atendido_query = """
            UPDATE municipios_atendidos 
            SET unidade = ?, razao_social = ?
            WHERE municipio_uf = ?
            """
            cursor.execute(atendido_query, (
                data['unidade'],
                data['distribuidor'],
                data['municipio_uf']
            ))
            
            conn.commit()
            conn.close()
            logging.info(f"Município atualizado com sucesso: {data['municipio_uf']}")
            return True
            
        except Exception as e:
            logging.error(f"Erro ao atualizar município: {e}")
            return False
            
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
