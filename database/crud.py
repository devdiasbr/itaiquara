import sqlite3
from typing import Dict, List, Optional
import os
from pathlib import Path
from models.contract_model import Contract

class DatabaseManager:
    def __init__(self):
        self.db_path = Path(__file__).parent / 'database.db'

    def get_connection(self) -> sqlite3.Connection:
        """Cria uma conexão com o banco de dados"""
        return sqlite3.connect(self.db_path)

    def init_db(self):
        """Inicializa o banco de dados com as tabelas necessárias"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS contracts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    municipio TEXT NOT NULL,
                    uf TEXT NOT NULL,
                    populacao INTEGER NOT NULL,
                    latitude REAL NOT NULL,
                    longitude REAL NOT NULL,
                    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            conn.commit()

class ContractCRUD:
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager

    def create(self, contract: Contract) -> int:
        """Cria um novo contrato"""
        with self.db_manager.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO contracts (municipio, uf, populacao, latitude, longitude)
                VALUES (?, ?, ?, ?, ?)
            ''', (
                contract.municipio,
                contract.uf,
                contract.populacao,
                contract.latitude,
                contract.longitude
            ))
            conn.commit()
            return cursor.lastrowid

    def read(self, contract_id: Optional[int] = None) -> List[Contract]:
        """Lê contratos. Se contract_id for fornecido, retorna apenas um contrato"""
        with self.db_manager.get_connection() as conn:
            cursor = conn.cursor()
            if contract_id is not None:
                cursor.execute('SELECT * FROM contracts WHERE id = ?', (contract_id,))
                row = cursor.fetchone()
                return [Contract.from_dict(dict(zip(
                    ['id', 'municipio', 'uf', 'populacao', 'latitude', 'longitude', 'data_criacao'],
                    row
                )))] if row else []
            
            cursor.execute('SELECT * FROM contracts')
            rows = cursor.fetchall()
            return [Contract.from_dict(dict(zip(
                ['id', 'municipio', 'uf', 'populacao', 'latitude', 'longitude', 'data_criacao'],
                row
            ))) for row in rows]

    def update(self, contract_id: int, data: Dict) -> bool:
        """Atualiza um contrato"""
        valid_fields = {'municipio', 'uf', 'populacao', 'latitude', 'longitude'}
        update_fields = {k: v for k, v in data.items() if k in valid_fields}
        
        if not update_fields:
            return False

        query = 'UPDATE contracts SET ' + ', '.join(f'{k} = ?' for k in update_fields.keys())
        query += ' WHERE id = ?'
        
        with self.db_manager.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (*update_fields.values(), contract_id))
            conn.commit()
            return cursor.rowcount > 0

    def delete(self, contract_id: int) -> bool:
        """Deleta um contrato"""
        with self.db_manager.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM contracts WHERE id = ?', (contract_id,))
            conn.commit()
            return cursor.rowcount > 0
