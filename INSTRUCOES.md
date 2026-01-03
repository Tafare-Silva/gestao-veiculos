# 🚗 Sistema de Gestão de Veículos - PRONTO PARA USO!

Oi! Preparei um sistema completo de gestão de veículos para você com TODAS as funcionalidades que pediu!

## ✅ O que foi criado:

### 1. **Sistema Completo de Cadastros**
   - ✅ Veículos (marca, modelo, ano, placa, km, chassi, cor)
   - ✅ Valores de compra e venda
   - ✅ Status (Disponível, Vendido, Em Manutenção)
   - ✅ Clientes (nome, CPF, telefone, email, endereço)
   - ✅ Fornecedores (nome, CNPJ/CPF, telefone, email)

### 2. **Gestão de Despesas**
   - ✅ Adicionar despesas para cada veículo
   - ✅ Tipos de despesa configuráveis (Mecânica, Funilaria, IPVA, etc.)
   - ✅ Valor, data e descrição detalhada
   - ✅ Vínculo com fornecedor

### 3. **Sistema de Vendas Completo**
   - ✅ Vender veículo com cliente
   - ✅ **TROCA DE VEÍCULOS**: Aceitar outro veículo como parte do pagamento
   - ✅ Cálculo automático: Valor Venda - Valor Entrada = Valor Final
   - ✅ Múltiplas formas de pagamento
   - ✅ Histórico completo de vendas

### 4. **Dashboard e Relatórios**
   - ✅ Dashboard com visão geral
   - ✅ Total de vendas, despesas e lucro
   - ✅ Últimas vendas realizadas
   - ✅ Veículos disponíveis
   - ✅ **Relatório Geral**: Resumo financeiro completo
   - ✅ **Relatório por Veículo**: Lucro/prejuízo individual
     - Mostra: Compra, Venda, Despesas e Lucro Final

### 5. **Interface Moderna**
   - ✅ Design bonito com Tailwind CSS
   - ✅ Responsivo (funciona em celular)
   - ✅ Navegação intuitiva
   - ✅ Filtros e busca
   - ✅ Mensagens de confirmação

## 📁 Estrutura do Projeto

```
gestao_veiculos/
├── README.md                    # Documentação completa
├── INICIO_RAPIDO.md            # Guia passo a passo
├── requirements.txt             # Dependências
├── manage.py                    # Gerenciador Django
├── criar_dados_iniciais.py     # Script para dados iniciais
├── core/                        # Configurações
│   ├── settings.py             # ⚠️ Configure o banco aqui
│   ├── urls.py
│   └── wsgi.py
└── veiculos/                    # App principal
    ├── models.py               # Todos os modelos
    ├── views.py                # Todas as views
    ├── urls.py                 # Rotas
    ├── forms.py                # Formulários
    ├── admin.py                # Admin Django
    └── templates/              # Templates HTML
        └── veiculos/
            ├── base.html                    # Template base
            ├── dashboard.html               # Dashboard
            ├── veiculo_*.html              # Templates de veículos
            ├── cliente_*.html              # Templates de clientes
            ├── fornecedor_*.html           # Templates de fornecedores
            ├── venda_*.html                # Templates de vendas
            ├── despesa_*.html              # Templates de despesas
            ├── relatorio_*.html            # Templates de relatórios
            └── *_confirm_delete.html       # Confirmações de exclusão
```

## 🚀 Como Instalar e Usar

### Passo 1: Preparar o Ambiente

```bash
cd gestao_veiculos

# Criar ambiente virtual
python -m venv venv

# Ativar (Windows)
venv\Scripts\activate

# Ativar (Linux/Mac)
source venv/bin/activate

# Instalar dependências
pip install -r requirements.txt
```

### Passo 2: Configurar PostgreSQL

**No pgAdmin ou psql:**

```sql
CREATE DATABASE gestao_veiculos;
CREATE USER postgres WITH PASSWORD 'sua_senha';
GRANT ALL PRIVILEGES ON DATABASE gestao_veiculos TO postgres;
```

**Edite `core/settings.py` (linha 62):**

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'gestao_veiculos',
        'USER': 'postgres',          # ← SEU USUÁRIO
        'PASSWORD': 'sua_senha',     # ← SUA SENHA
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### Passo 3: Criar as Tabelas

```bash
python manage.py makemigrations
python manage.py migrate
```

### Passo 4: Dados Iniciais

```bash
python manage.py shell < criar_dados_iniciais.py
```

Isso vai criar:
- Tipos de despesa (Mecânica, Funilaria, IPVA, etc.)
- Formas de pagamento (Dinheiro, PIX, Cartão, etc.)

### Passo 5: Rodar!

```bash
python manage.py runserver
```

**Acesse:** http://localhost:8000

## 💡 Como Usar o Sistema

### 1. Primeiro Uso
1. Vá em **Cadastros → Fornecedores** e cadastre fornecedores
2. Vá em **Cadastros → Clientes** e cadastre clientes
3. Vá em **Veículos → Novo Veículo** e cadastre seus veículos

### 2. Adicionar Despesas
1. Clique em um veículo
2. Clique em "Adicionar Despesa"
3. Escolha o tipo, valor e fornecedor
4. O lucro será recalculado automaticamente!

### 3. Vender um Veículo

**Venda Simples:**
1. Clique em "Vender" no veículo
2. Escolha o cliente
3. Confirme o valor de venda
4. Escolha a forma de pagamento

**Venda com Troca:**
1. Clique em "Vender" no veículo
2. Escolha o cliente
3. **Selecione um veículo de entrada** (outro veículo disponível)
4. Informe o **valor do veículo de entrada**
5. O sistema calcula: Venda - Entrada = Valor Final
6. Cliente paga apenas o Valor Final!

**Exemplo de Troca:**
- Vendendo: Honda Civic por R$ 40.000
- Recebendo: Fiat Uno avaliado em R$ 15.000
- Cliente paga: R$ 25.000 (40.000 - 15.000)

### 4. Ver Relatórios

**Relatório Geral:**
- Total de vendas realizadas
- Total de despesas
- Lucro total do negócio

**Relatório por Veículo:**
- Cada veículo vendido mostra:
  - Quanto comprou
  - Quanto vendeu
  - Quanto gastou em despesas
  - **Lucro/Prejuízo real**

## 🎨 Funcionalidades Extras

### Filtros e Buscas
- Buscar veículos por marca, modelo ou placa
- Filtrar por status (Disponível, Vendido, Em Manutenção)
- Buscar clientes por nome, CPF ou telefone

### Cálculos Automáticos
- **Lucro Previsto**: Venda - Compra - Despesas
- **Lucro Real**: Calculado após a venda
- **Total de Despesas**: Soma automática

### Segurança
- Veículos vendidos não podem ser deletados
- Confirmação antes de excluir qualquer item
- Validação de valores positivos

## 📊 Exemplo de Uso Completo

1. **Cadastrar Fornecedor**: "Auto Peças Silva"
2. **Comprar Veículo**: Toyota Corolla 2018 por R$ 45.000
3. **Adicionar Despesas**:
   - Mecânica: R$ 2.000
   - Funilaria: R$ 1.500
   - IPVA: R$ 800
   - Total: R$ 4.300
4. **Vender Veículo**: Por R$ 55.000 com PIX
5. **Lucro**: R$ 55.000 - R$ 45.000 - R$ 4.300 = **R$ 5.700**

## 🔧 Dicas Importantes

1. **Sempre registre as despesas** para ter lucro real
2. **Use status "Em Manutenção"** para veículos em reparo
3. **Cadastre fornecedores** antes dos veículos
4. **Veículos vendidos ficam no histórico** para relatórios
5. **Consulte o dashboard** para visão geral do negócio

## 🐛 Problemas Comuns

**Erro de conexão com banco:**
- Verifique se o PostgreSQL está rodando
- Confira usuário e senha em `settings.py`

**Módulos não encontrados:**
```bash
pip install -r requirements.txt
```

**Tabelas não criadas:**
```bash
python manage.py makemigrations
python manage.py migrate
```

## 📝 Recursos Técnicos

- **Backend**: Django 5.0
- **Banco**: PostgreSQL
- **Frontend**: Django Templates + Tailwind CSS
- **Idioma**: Português (pt-BR)
- **Timezone**: America/Sao_Paulo

## 🎯 Próximas Melhorias Sugeridas

Se quiser expandir no futuro:
- [ ] Gráficos de vendas por período
- [ ] Exportar relatórios em PDF/Excel
- [ ] Sistema de usuários com permissões
- [ ] Fotos dos veículos
- [ ] Histórico de preços
- [ ] Notificações de manutenção

## 📚 Documentação

- **README.md**: Documentação completa
- **INICIO_RAPIDO.md**: Guia passo a passo
- **Este arquivo**: Visão geral e instruções

## ✨ Conclusão

O sistema está 100% funcional com TODAS as funcionalidades que você pediu:
- ✅ Cadastro de veículos, clientes e fornecedores
- ✅ Gestão de despesas por veículo
- ✅ **Sistema de vendas com troca de veículos**
- ✅ Múltiplas formas de pagamento
- ✅ Relatórios gerais e por veículo
- ✅ Interface bonita com Tailwind

**Está pronto para uso!** 🚀

Qualquer dúvida, é só perguntar!
