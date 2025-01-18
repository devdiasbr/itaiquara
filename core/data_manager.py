import sqlite3
import logging
import os
from typing import List, Dict, Tuple, Optional

class DataManager:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DataManager, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
            
        self._initialized = True
        self.current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.db_path = os.path.join(self.current_dir, 'database', 'database.db')
        
        # Cache de dados
        self._descricoes: List[str] = []
        self._municipios_data: Dict[str, Dict] = {}
        
        # Carregar dados iniciais
        self.refresh_data()
    
    def refresh_data(self) -> None:
        """Recarrega todos os dados do banco"""
        try:
            self._descricoes = self._load_descricoes()
            self._municipios_data = self._load_municipios_data()
        except Exception as e:
            logging.error(f"Erro ao recarregar dados: {e}")
    
    def _load_descricoes(self) -> List[str]:
        """Carrega todas as descrições do banco"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT descricao FROM municipios WHERE descricao IS NOT NULL ORDER BY descricao")
            result = cursor.fetchall()
            conn.close()
            return [row[0] for row in result if row[0]]
        except Exception as e:
            logging.error(f"Erro ao carregar descrições: {e}")
            return []
    
    def _load_municipios_data(self) -> Dict[str, Dict]:
        """Carrega dados de todos os municípios"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT m.*, d.*
                FROM municipios m
                LEFT JOIN distribuidores d ON m.municipio_uf = d.razao_social
                WHERE m.descricao IS NOT NULL
            """)
            
            columns = [description[0] for description in cursor.description]
            result = {}
            
            for row in cursor.fetchall():
                data = dict(zip(columns, row))
                if data['descricao']:  # Usar descrição como chave
                    result[data['descricao']] = data
            
            conn.close()
            return result
        except Exception as e:
            logging.error(f"Erro ao carregar dados dos municípios: {e}")
            return {}
    
    def get_descricoes(self) -> List[str]:
        """Retorna lista de descrições do cache"""
        return sorted(self._descricoes)
    
    def get_municipio_by_descricao(self, descricao: str) -> Tuple[bool, Dict]:
        """Retorna dados do município pela descrição do cache"""
        if descricao in self._municipios_data:
            return True, self._municipios_data[descricao]
        return False, {"error": "Município não encontrado"}
    
    def create_distribuidor(self, data: Dict) -> Tuple[bool, str]:
        """Cria novo distribuidor e atualiza o cache"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
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
            
            conn.commit()
            conn.close()
            
            # Atualizar cache
            self.refresh_data()
            
            return True, "Distribuidor cadastrado com sucesso!"
        except Exception as e:
            logging.error(f"Erro ao criar distribuidor: {e}")
            return False, f"Erro ao criar distribuidor: {e}"
    
    def delete_distribuidor(self, municipio_uf: str) -> Tuple[bool, str]:
        """Remove distribuidor e atualiza o cache"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("DELETE FROM distribuidores WHERE razao_social = ?", (municipio_uf,))
            
            if cursor.rowcount == 0:
                conn.close()
                return False, "Distribuidor não encontrado"
            
            conn.commit()
            conn.close()
            
            # Atualizar cache
            self.refresh_data()
            
            return True, "Distribuidor removido com sucesso!"
        except Exception as e:
            logging.error(f"Erro ao remover distribuidor: {e}")
            return False, f"Erro ao remover distribuidor: {e}"
    
    def update_distribuidor(self, old_razao_social: str, data: Dict) -> Tuple[bool, str]:
        """Atualiza distribuidor e o cache"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                UPDATE distribuidores SET
                    cnpj = ?, razao_social = ?, nome_fantasia = ?, responsavel = ?,
                    telefone_responsavel = ?, contrato = ?, codigo = ?, distribuidor_outros = ?,
                    insc_estadual = ?, contato = ?, telefone_distribuidor = ?, celular = ?,
                    fax = ?, endereco = ?, cidade = ?, uf = ?, cep = ?, email = ?
                WHERE razao_social = ?
            """, (
                data['cnpj'], data['razao_social'], data['nome_fantasia'],
                data['responsavel'], data['telefone_responsavel'], data['contrato'],
                data['codigo'], data['distribuidor_outros'], data['insc_estadual'],
                data['contato'], data['telefone_distribuidor'], data['celular'],
                data['fax'], data['endereco'], data['cidade'], data['uf'],
                data['cep'], data['email'], old_razao_social
            ))
            
            if cursor.rowcount == 0:
                conn.close()
                return False, "Distribuidor não encontrado"
            
            conn.commit()
            conn.close()
            
            # Atualizar cache
            self.refresh_data()
            
            return True, "Distribuidor atualizado com sucesso!"
        except Exception as e:
            logging.error(f"Erro ao atualizar distribuidor: {e}")
            return False, f"Erro ao atualizar distribuidor: {e}"
