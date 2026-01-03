# Sistema de Gestão de Veículos

Sistema completo para gerenciar compra, venda e despesas de veículos.

## Funcionalidades

- ✅ Cadastro de Veículos (marca, modelo, ano, preço de compra/venda)
- ✅ Cadastro de Despesas por veículo (mecânica, funilaria, impostos, etc)
- ✅ Cadastro de Fornecedores
- ✅ Cadastro de Clientes
- ✅ Sistema de Vendas com troca de veículos
- ✅ Múltiplas formas de pagamento
- ✅ Dashboard de resultados gerais
- ✅ Relatório de lucro por veículo

## Instalação

### 1. Requisitos
- Python 3.10+
- PostgreSQL instalado e rodando

### 2. Criar banco de dados no PostgreSQL

Abra o pgAdmin e execute:

```sql
CREATE DATABASE gestao_veiculos;
CREATE USER seu_usuario WITH PASSWORD 'sua_senha';
ALTER ROLE seu_usuario SET client_encoding TO 'utf8';
ALTER ROLE seu_usuario SET default_transaction_isolation TO 'read committed';
ALTER ROLE seu_usuario SET timezone TO 'America/Sao_Paulo';
GRANT ALL PRIVILEGES ON DATABASE gestao_veiculos TO seu_usuario;
```

### 3. Configurar o projeto

```bash
# Clone ou extraia o projeto
cd gestao_veiculos

# Crie um ambiente virtual
python -m venv venv

# Ative o ambiente virtual
# No Windows:
venv\Scripts\activate
# No Linux/Mac:
source venv/bin/activate

# Instale as dependências
pip install -r requirements.txt
```

### 4. Configurar o banco de dados

Edite o arquivo `core/settings.py` e ajuste as configurações do PostgreSQL:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'gestao_veiculos',
        'USER': 'seu_usuario',
        'PASSWORD': 'sua_senha',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### 5. Criar as tabelas

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Criar superusuário (opcional, para acessar o admin)

```bash
python manage.py createsuperuser
```

### 7. Rodar o servidor

```bash
python manage.py runserver
```

Acesse: http://localhost:8000

## Estrutura do Projeto

```
gestao_veiculos/
├── core/                  # Configurações do Django
├── veiculos/             # App principal
│   ├── models.py         # Modelos (Veículo, Despesa, Cliente, etc)
│   ├── views.py          # Views
│   ├── urls.py           # URLs
│   ├── forms.py          # Formulários
│   └── templates/        # Templates HTML
├── static/               # Arquivos estáticos
├── manage.py
└── requirements.txt
```

## Uso

### Dashboard Principal
- Acesse a página inicial para ver o resumo geral de vendas e despesas

### Cadastros
- **Veículos**: Menu → Veículos → Novo Veículo
- **Clientes**: Menu → Clientes → Novo Cliente
- **Fornecedores**: Menu → Fornecedores → Novo Fornecedor

### Despesas
- Acesse um veículo e clique em "Adicionar Despesa"
- Informe tipo, valor, fornecedor e descrição

### Vendas
- Clique em "Vender" em um veículo disponível
- Informe o cliente e valor de venda
- Opcionalmente, selecione um veículo como parte da entrada
- Escolha a forma de pagamento

### Relatórios
- **Dashboard Geral**: Visualize o total de vendas e despesas
- **Por Veículo**: Veja o lucro/prejuízo de cada veículo vendido

## Tecnologias

- Django 5.0
- PostgreSQL
- Django Templates
- Tailwind CSS (via CDN)
- Python 3.10+

## Suporte

Para dúvidas ou problemas, verifique:
1. Se o PostgreSQL está rodando
2. Se as credenciais do banco estão corretas
3. Se todas as dependências foram instaladas
