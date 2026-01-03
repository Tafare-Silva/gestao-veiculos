# 🚀 Guia de Início Rápido

## Passo 1: Instalar Dependências

```bash
cd gestao_veiculos
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate

pip install -r requirements.txt
```

## Passo 2: Configurar Banco de Dados

### No pgAdmin ou psql, execute:

```sql
CREATE DATABASE gestao_veiculos;
CREATE USER seu_usuario WITH PASSWORD 'sua_senha';
GRANT ALL PRIVILEGES ON DATABASE gestao_veiculos TO seu_usuario;
```

### Edite `core/settings.py` linha 62:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'gestao_veiculos',
        'USER': 'seu_usuario',      # ← ALTERE AQUI
        'PASSWORD': 'sua_senha',     # ← ALTERE AQUI
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

## Passo 3: Criar Tabelas

```bash
python manage.py makemigrations
python manage.py migrate
```

## Passo 4: Popular Dados Iniciais

```bash
python manage.py shell < criar_dados_iniciais.py
```

## Passo 5: Rodar o Servidor

```bash
python manage.py runserver
```

Acesse: **http://localhost:8000**

## 🎯 Próximos Passos

1. **Cadastrar Fornecedores**: Menu → Cadastros → Fornecedores
2. **Cadastrar Clientes**: Menu → Cadastros → Clientes
3. **Cadastrar Veículos**: Menu → Veículos → Novo Veículo
4. **Adicionar Despesas**: Acesse um veículo → Adicionar Despesa
5. **Realizar Vendas**: Acesse um veículo disponível → Vender
6. **Ver Relatórios**: Menu → Relatórios

## 📊 Recursos Principais

### Dashboard
- Visão geral de veículos disponíveis e vendidos
- Total de vendas e lucro
- Últimas vendas realizadas

### Gestão de Veículos
- Cadastro completo de veículos
- Controle de despesas por veículo
- Cálculo automático de lucro previsto
- Status (Disponível, Vendido, Em Manutenção)

### Sistema de Vendas
- Venda de veículos com troca
- Múltiplas formas de pagamento
- Cálculo automático do valor final
- Histórico completo de vendas

### Relatórios
- Relatório geral de vendas e despesas
- Relatório de lucro por veículo
- Filtros e buscas avançadas

## 🔧 Configurações Adicionais

### Criar Superusuário (Opcional)

Para acessar o painel administrativo do Django:

```bash
python manage.py createsuperuser
```

Acesse: http://localhost:8000/admin

### Adicionar Mais Tipos de Despesa

Menu → Configurações → Tipos de Despesa → + Novo Tipo

### Adicionar Mais Formas de Pagamento

Menu → Configurações → Formas de Pagamento → + Nova Forma

## 💡 Dicas de Uso

1. **Sempre cadastre o fornecedor** antes de cadastrar um veículo comprado dele
2. **Registre todas as despesas** para ter cálculos precisos de lucro
3. **Use o status "Em Manutenção"** para veículos que estão em reparo
4. **Veículos vendidos não podem ser editados** para manter histórico consistente
5. **Consulte os relatórios regularmente** para acompanhar o desempenho

## 🐛 Resolução de Problemas

### Erro de conexão com banco de dados
- Verifique se o PostgreSQL está rodando
- Confirme as credenciais em `core/settings.py`
- Teste a conexão no pgAdmin

### Erro ao criar tabelas
- Delete as migrações antigas: `rm veiculos/migrations/00*.py`
- Execute novamente: `python manage.py makemigrations && python manage.py migrate`

### Página não carrega CSS
- Certifique-se de que o Tailwind CDN está acessível
- Limpe o cache do navegador

## 📞 Suporte

Para dúvidas ou problemas:
1. Verifique este guia primeiro
2. Consulte o README.md principal
3. Revise os logs de erro no terminal

## 🎨 Personalização

O sistema usa Tailwind CSS via CDN. Para personalizar cores e estilos, edite o arquivo `veiculos/templates/veiculos/base.html`.

---

**Desenvolvido com Django + PostgreSQL + Tailwind CSS**
