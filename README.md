# 🚗 Sistema de Gestão de Veículos

![Python](https://img.shields.io/badge/python-3.11+-blue.svg)
![Django](https://img.shields.io/badge/django-5.0-green.svg)
![PostgreSQL](https://img.shields.io/badge/postgresql-latest-blue.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

Sistema completo para gerenciamento de compra, venda e controle financeiro de veículos. Ideal para revendedoras, stands e profissionais autônomos do ramo automotivo.

![Screenshot do Sistema](docs/screenshots/dashboard.png)

## ✨ Funcionalidades

### 📊 Dashboard Inteligente
- Visão geral do negócio em tempo real
- Filtros por período (hoje, semana, mês, ano)
- Indicadores de vendas, despesas e lucro
- Últimas vendas e veículos disponíveis

### 🚙 Gestão de Veículos
- **Cadastro completo** com RENAVAM, placa, chassi
- **Galeria de fotos** com upload múltiplo
- Controle de status (disponível, vendido, manutenção)
- Histórico de despesas por veículo
- Cálculo automático de lucro real

### 💰 Controle Financeiro
- Registro de todas as despesas por veículo
- Tipos de despesa configuráveis
- Relatórios detalhados de lucro/prejuízo
- Análise por veículo individual
- Filtros avançados por período, veículo e cliente

### 🤝 Gestão de Clientes e Fornecedores
- Cadastro completo de clientes
- Histórico de compras por cliente
- Gerenciamento de fornecedores
- Rastreamento de origem dos veículos

### 🔄 Sistema de Vendas
- **Suporte a veículo de troca** (entrada)
- Cálculo automático de valores
- Múltiplas formas de pagamento
- Detalhamento completo da venda

### 📈 Relatórios Completos
- Relatório geral consolidado
- Relatório individual por veículo
- Detalhamento expansível (+/-)
- Exportação de dados
- Filtros avançados

### 📱 100% Responsivo
- Interface adaptada para celular, tablet e desktop
- Menu hamburger mobile
- Cards otimizados para touch
- Experiência fluida em qualquer dispositivo

## 🖼️ Screenshots

<details>
<summary>Ver Screenshots</summary>

### Dashboard
![Dashboard](docs/screenshots/dashboard.png)

### Cadastro de Veículo com Galeria
![Cadastro](docs/screenshots/cadastro-veiculo.png)

### Relatório Detalhado
![Relatório](docs/screenshots/relatorio.png)

### Versão Mobile
![Mobile](docs/screenshots/mobile.png)

</details>

## 🚀 Começando

### Pré-requisitos

- Python 3.11 ou superior
- PostgreSQL 12 ou superior
- pip (gerenciador de pacotes Python)

### Instalação Rápida

```bash
# 1. Clone o repositório
git clone https://github.com/seu-usuario/gestao-veiculos.git
cd gestao-veiculos

# 2. Crie um ambiente virtual
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate

# 3. Instale as dependências
pip install -r requirements.txt

# 4. Configure o banco de dados PostgreSQL
# Crie um banco chamado 'gestao_veiculos'
createdb gestao_veiculos

# 5. Configure as variáveis de ambiente
# Copie o arquivo .env.example para .env e configure
cp .env.example .env

# 6. Execute as migrações
python manage.py migrate

# 7. Crie um superusuário
python manage.py createsuperuser

# 8. Crie a pasta para uploads
mkdir media

# 9. Inicie o servidor
python manage.py runserver
```

Acesse: http://localhost:8000

## ⚙️ Configuração

### Banco de Dados

Edite o arquivo `core/settings.py` ou use variáveis de ambiente:

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

### Variáveis de Ambiente (.env)

```env
DEBUG=True
SECRET_KEY=sua-chave-secreta-aqui
DATABASE_NAME=gestao_veiculos
DATABASE_USER=postgres
DATABASE_PASSWORD=sua_senha
DATABASE_HOST=localhost
DATABASE_PORT=5432
```

## 📖 Documentação

- [Guia de Início Rápido](INICIO_RAPIDO.md)
- [Instruções Detalhadas](INSTRUCOES.md)
- [Como usar Imagens e RENAVAM](docs/IMAGENS_RENAVAM.md)
- [API DETRAN (Futuro)](docs/API_INTEGRACAO.md)

## 🛠️ Tecnologias Utilizadas

- **Backend:** Django 5.0
- **Banco de Dados:** PostgreSQL
- **Frontend:** TailwindCSS 3
- **Upload de Imagens:** Pillow
- **Linguagem:** Python 3.11+

## 📂 Estrutura do Projeto

```
gestao_veiculos/
├── core/                      # Configurações do Django
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── veiculos/                  # App principal
│   ├── models.py             # Modelos (Veiculo, Venda, etc)
│   ├── views.py              # Lógica de negócio
│   ├── forms.py              # Formulários
│   ├── urls.py               # Rotas
│   ├── admin.py              # Painel administrativo
│   └── templates/            # Templates HTML
│       └── veiculos/
│           ├── base.html     # Template base
│           ├── dashboard.html
│           ├── veiculo_*.html
│           └── ...
├── media/                     # Uploads (imagens dos veículos)
├── static/                    # Arquivos estáticos
├── requirements.txt           # Dependências Python
├── manage.py                 # CLI do Django
└── README.md                 # Este arquivo
```

## 🎯 Roadmap

- [x] Sistema básico de veículos
- [x] Controle de despesas
- [x] Sistema de vendas
- [x] Relatórios financeiros
- [x] Upload de imagens
- [x] Campo RENAVAM
- [x] Interface responsiva
- [ ] Integração com API DETRAN
- [ ] Exportação para Excel/PDF
- [ ] Gráficos interativos
- [ ] Sistema de backup automático
- [ ] API REST
- [ ] App Mobile nativo

## 🤝 Contribuindo

Contribuições são bem-vindas! Por favor, siga estes passos:

1. Faça um Fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/MinhaFeature`)
3. Commit suas mudanças (`git commit -m 'Adiciona MinhaFeature'`)
4. Push para a branch (`git push origin feature/MinhaFeature`)
5. Abra um Pull Request

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## 👤 Autor

**Seu Nome**

- GitHub: [@seu-usuario](https://github.com/seu-usuario)
- LinkedIn: [Seu Nome](https://linkedin.com/in/seu-perfil)

## 🙏 Agradecimentos

- Django Framework
- TailwindCSS
- Comunidade Open Source

## 📧 Contato

Para dúvidas ou sugestões, abra uma [issue](https://github.com/seu-usuario/gestao-veiculos/issues) ou envie um email para: seu-email@exemplo.com

---

⭐ Se este projeto te ajudou, considere dar uma estrela!

**Feito com ❤️ e Python**
