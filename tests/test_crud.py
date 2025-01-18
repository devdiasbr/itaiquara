import unittest
import sys
from pathlib import Path
import os

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from database.crud import DatabaseManager, ContractCRUD
from models.contract_model import Contract

class TestContractCRUD(unittest.TestCase):
    def setUp(self):
        self.db_manager = DatabaseManager()
        self.crud = ContractCRUD(self.db_manager)
        self.db_manager.init_db()
        
        # Dados de teste
        self.test_contract = Contract(
            municipio="Teste Cidade",
            uf="TS",
            populacao=100000,
            latitude=-23.5505,
            longitude=-46.6333
        )

    def test_create_contract(self):
        contract_id = self.crud.create(self.test_contract)
        self.assertIsNotNone(contract_id)
        
        # Verificar se foi criado
        contracts = self.crud.read(contract_id)
        self.assertEqual(len(contracts), 1)
        self.assertEqual(contracts[0].municipio, self.test_contract.municipio)

    def test_update_contract(self):
        # Criar contrato
        contract_id = self.crud.create(self.test_contract)
        
        # Atualizar
        update_data = {"populacao": 150000}
        success = self.crud.update(contract_id, update_data)
        self.assertTrue(success)
        
        # Verificar atualização
        contracts = self.crud.read(contract_id)
        self.assertEqual(contracts[0].populacao, 150000)

    def test_delete_contract(self):
        # Criar contrato
        contract_id = self.crud.create(self.test_contract)
        
        # Deletar
        success = self.crud.delete(contract_id)
        self.assertTrue(success)
        
        # Verificar se foi deletado
        contracts = self.crud.read(contract_id)
        self.assertEqual(len(contracts), 0)

if __name__ == '__main__':
    unittest.main()
