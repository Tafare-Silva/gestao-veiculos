"""
Script para popular o banco de dados com dados iniciais
Execute: python manage.py shell < criar_dados_iniciais.py
"""

from veiculos.models import TipoDespesa, FormaPagamento

# Criar tipos de despesa
tipos_despesa = [
    {'nome': 'Mecânica', 'descricao': 'Reparos mecânicos gerais'},
    {'nome': 'Funilaria', 'descricao': 'Reparos de lataria e pintura'},
    {'nome': 'IPVA', 'descricao': 'Imposto sobre Propriedade de Veículos Automotores'},
    {'nome': 'Licenciamento', 'descricao': 'Taxa anual de licenciamento'},
    {'nome': 'Seguro', 'descricao': 'Seguro do veículo'},
    {'nome': 'Documentação', 'descricao': 'Transferência e documentos'},
    {'nome': 'Pneus', 'descricao': 'Troca e manutenção de pneus'},
    {'nome': 'Elétrica', 'descricao': 'Sistema elétrico do veículo'},
    {'nome': 'Ar Condicionado', 'descricao': 'Manutenção do ar condicionado'},
    {'nome': 'Lavagem/Limpeza', 'descricao': 'Lavagem e limpeza detalhada'},
    {'nome': 'Outros', 'descricao': 'Outras despesas diversas'},
]

print("Criando tipos de despesa...")
for tipo_data in tipos_despesa:
    tipo, created = TipoDespesa.objects.get_or_create(
        nome=tipo_data['nome'],
        defaults={'descricao': tipo_data['descricao']}
    )
    if created:
        print(f"  ✓ {tipo.nome}")
    else:
        print(f"  - {tipo.nome} (já existe)")

# Criar formas de pagamento
formas_pagamento = [
    'Dinheiro',
    'PIX',
    'Cartão de Crédito',
    'Cartão de Débito',
    'Transferência Bancária',
    'Boleto',
    'Cheque',
    'Financiamento',
    'Consórcio',
]

print("\nCriando formas de pagamento...")
for forma_nome in formas_pagamento:
    forma, created = FormaPagamento.objects.get_or_create(nome=forma_nome)
    if created:
        print(f"  ✓ {forma.nome}")
    else:
        print(f"  - {forma.nome} (já existe)")

print("\n✅ Dados iniciais criados com sucesso!")
