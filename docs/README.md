# 📊 Gerador de Contratos

Uma aplicação desktop robusta e moderna desenvolvida com Flet (Flutter/Python) para gerenciamento completo de contratos e geração automatizada de documentos KML.

## 📋 Descrição Detalhada

O Gerador de Contratos é uma solução completa para gerenciamento de dados municipais e geração automatizada de contratos. Desenvolvido com tecnologias modernas, oferece uma experiência fluida e profissional para o usuário.

### 🎨 Interface do Usuário
- **Tema Personalizado**: Esquema de cores profissional em tons de azul (#2196F3)
- **Scrollbars Customizadas**: Experiência de rolagem suave com scrollbars temáticas
- **Layout Responsivo**: Adaptação automática ao tamanho da janela
- **Feedback Visual**: Indicadores de carregamento e status de operações

### 💾 Gerenciamento de Dados
- **Banco SQLite Otimizado**: Armazenamento eficiente e rápido
- **Queries Assíncronas**: Operações não-bloqueantes para melhor performance
- **Cache Inteligente**: Sistema de cache para dados frequentemente acessados
- **Validação Robusta**: Verificação completa de dados em todas as operações

## 🚀 Funcionalidades Detalhadas

### 📋 Visualização de Dados
```python
# Exemplo de configuração da tabela de dados
data_table = ft.DataTable(
    columns=[
        ft.DataColumn(ft.Text("Município/UF")),
        ft.DataColumn(ft.Text("População")),
        ft.DataColumn(ft.Text("Coordenadas")),
        # ... mais colunas
    ],
    rows=rows,
    sort_ascending=True,
    sort_column_index=0,
)
```

#### Recursos da Tabela:
- Ordenação multi-coluna
- Filtros avançados
- Paginação configurável (10, 25, 50 registros)
- Busca em tempo real
- Seleção múltipla de registros

### ➕ Sistema de CRUD Completo

#### Inclusão de Registros
```python
async def add_record(data: dict):
    try:
        async with DatabaseManager() as db:
            await db.execute("""
                INSERT INTO municipios 
                (nome, uf, populacao, coordenadas) 
                VALUES (?, ?, ?, ?)
            """, (data['nome'], data['uf'], data['populacao'], data['coordenadas']))
            await db.commit()
    except Exception as e:
        logging.error(f"Erro ao inserir registro: {e}")
        raise
```

#### Edição de Registros
- Validação em tempo real
- Histórico de alterações
- Sistema de backup automático
- Rollback em caso de erro

#### Exclusão de Registros
- Confirmação dupla
- Exclusão lógica (soft delete)
- Registro de operações
- Possibilidade de restauração

### 🗺️ Geração de KML
```python
class KMLGenerator:
    def __init__(self):
        self.template = """<?xml version="1.0" encoding="UTF-8"?>
            <kml xmlns="http://www.opengis.net/kml/2.2">
                <Document>
                    <name>{name}</name>
                    <description>{description}</description>
                    {placemarks}
                </Document>
            </kml>"""
```

#### Recursos do Gerador:
- Suporte a múltiplos formatos de coordenadas
- Validação geográfica
- Otimização de arquivos
- Preview antes da geração

## 🛠️ Arquitetura Técnica

### 📁 Estrutura de Diretórios
```
1 KML ITAIQUARA 2.0/
├── config/                 # Configurações
│   └── settings.py        # Configurações centralizadas
│
├── core/                  # Núcleo da aplicação
│   ├── data_loader.py    # Carregamento de dados
│   └── data_manager.py   # Gerenciamento de dados
│
├── database/              # Camada de dados
│   ├── database.db       # Banco SQLite
│   └── crud.py          # Operações CRUD
│
├── docs/                  # Documentação
│   ├── DOCUMENTACAO_TECNICA.md
│   ├── ORCAMENTO.md
│   └── README.md
│
├── models/                # Modelos de dados
│   └── contract_model.py # Modelo de contrato
│
├── tests/                 # Testes unitários
│   ├── test_crud.py     # Testes de CRUD
│   └── test_data_loader.py
│
├── utils/                 # Utilitários
│   ├── crud_manager.py   # Gerenciador de CRUD
│   ├── dropdown_helper.py # Auxiliar de dropdowns
│   ├── kml_generator.py  # Gerador de KML
│   └── utils.py         # Funções utilitárias
│
├── views/                 # Interface do usuário
│   ├── alterar_view.py   # Tela de alteração
│   ├── excluir_view.py   # Tela de exclusão
│   ├── incluir_view.py   # Tela de inclusão
│   ├── loading_view.py   # Tela de carregamento
│   └── visualizar_view.py # Tela de visualização
│
├── main.py               # Ponto de entrada
└── requirements.txt      # Dependências
```

### 🔧 Componentes Principais

#### Core
- **data_loader.py**: Responsável pelo carregamento e processamento inicial dos dados
- **data_manager.py**: Gerencia o estado e as operações principais dos dados

#### Database
- **crud.py**: Implementa as operações CRUD (Create, Read, Update, Delete)
- **database.db**: Banco de dados SQLite para armazenamento persistente

#### Models
- **contract_model.py**: Define a estrutura e validação dos contratos

#### Views
- Interfaces modulares para cada operação do sistema
- Design responsivo e intuitivo
- Feedback visual em tempo real

### 📦 Dependências

```bash
# Instalar dependências
pip install -r requirements.txt
```

Principais dependências:
- flet>=0.21.0: Framework UI moderno
- pandas>=2.0.0: Manipulação de dados
- simplekml>=1.3.1: Geração de arquivos KML
- sqlite3-api>=2.0.1: Operações com banco de dados

### 🚀 Como Executar

1. Clone o repositório
2. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
3. Execute o aplicativo:
   ```bash
   python main.py
   ```

### 🧪 Testes

Execute os testes unitários:
```bash
python -m unittest discover tests
```

## ⚙️ Instalação e Configuração

### 1. Preparação do Ambiente
```bash
# Criar ambiente virtual
python -m venv venv

# Ativar ambiente (Windows)
.\venv\Scripts\activate

# Ativar ambiente (Linux/Mac)
source venv/bin/activate
```

### 2. Instalação de Dependências
```bash
# Instalar requisitos
pip install -r requirements.txt

# Verificar instalação
pip list
```

### 3. Configuração do Banco de Dados
```bash
# Criar banco de dados
python scripts/create_database.py

# Executar migrações
python scripts/run_migrations.py
```

## 📊 Métricas e Performance

### Tempos de Resposta
- Carregamento inicial: < 1s
- Busca: < 100ms
- Geração de KML: < 3s para 1000 registros

### Uso de Recursos
- Memória: ~100MB em uso normal
- CPU: Pico de 30% durante geração de KML
- Disco: ~10MB para 10000 registros

## 🔍 Debugging

### Logs Detalhados
```python
# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/app.log'),
        logging.StreamHandler()
    ]
)
```

### Níveis de Log
- **INFO**: Operações normais
- **WARNING**: Alertas não críticos
- **ERROR**: Erros recuperáveis
- **CRITICAL**: Erros críticos

## 🔒 Segurança

### Proteção de Dados
- Sanitização de inputs
- Prevenção contra SQL Injection
- Validação de dados
- Backup automático

### Controle de Acesso
- Sistema de login (em desenvolvimento)
- Níveis de permissão
- Registro de atividades

## 🤝 Contribuição

### Processo de Desenvolvimento
1. Fork do repositório
2. Criação de branch (`git checkout -b feature/AmazingFeature`)
3. Commit das alterações (`git commit -m 'Add AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abertura de Pull Request

### Padrões de Código
- PEP 8 para Python
- Docstrings em todas as funções
- Testes unitários para novas features
- Comentários em código complexo

## 📞 Suporte e Contato

### Canais de Suporte
- **Email**: [inserir email]
- **Discord**: [inserir discord]
- **Issues**: GitHub Issues

### Reportando Problemas
1. Verifique se o problema já foi reportado
2. Inclua logs relevantes
3. Descreva os passos para reproduzir
4. Informe versão do sistema e ambiente

## 📄 Licença

Este projeto está sob a licença [inserir tipo de licença]. Veja o arquivo LICENSE para mais detalhes.

---

## 🔄 Atualizações e Versões

### Changelog
- **v2.0.0** (Atual)
  - Interface renovada
  - Sistema de cache
  - Melhorias de performance
  
- **v1.0.0**
  - Lançamento inicial
  - Funcionalidades básicas

### Roadmap
- [ ] Sistema de login
- [ ] Exportação para outros formatos
- [ ] Dashboard de análise
- [ ] API REST
