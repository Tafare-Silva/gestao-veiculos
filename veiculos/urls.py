from django.urls import path
from . import views

urlpatterns = [
    # Dashboard
    path('', views.dashboard, name='dashboard'),
    
    # Veículos
    path('veiculos/', views.veiculo_lista, name='veiculo_lista'),
    path('veiculos/novo/', views.veiculo_novo, name='veiculo_novo'),
    path('veiculos/<int:pk>/', views.veiculo_detalhe, name='veiculo_detalhe'),
    path('veiculos/<int:pk>/editar/', views.veiculo_editar, name='veiculo_editar'),
    path('veiculos/<int:pk>/deletar/', views.veiculo_deletar, name='veiculo_deletar'),
    
    # Imagens dos Veículos
    path('veiculos/imagem/<int:pk>/deletar/', views.veiculo_imagem_deletar, name='veiculo_imagem_deletar'),
    path('veiculos/imagem/<int:pk>/principal/', views.veiculo_imagem_principal, name='veiculo_imagem_principal'),
    
    # Despesas
    path('veiculos/<int:veiculo_pk>/despesa/nova/', views.despesa_nova, name='despesa_nova'),
    path('despesas/<int:pk>/editar/', views.despesa_editar, name='despesa_editar'),
    path('despesas/<int:pk>/deletar/', views.despesa_deletar, name='despesa_deletar'),
    
    # Clientes
    path('clientes/', views.cliente_lista, name='cliente_lista'),
    path('clientes/novo/', views.cliente_novo, name='cliente_novo'),
    path('clientes/<int:pk>/editar/', views.cliente_editar, name='cliente_editar'),
    path('clientes/<int:pk>/deletar/', views.cliente_deletar, name='cliente_deletar'),
    
    # Fornecedores
    path('fornecedores/', views.fornecedor_lista, name='fornecedor_lista'),
    path('fornecedores/novo/', views.fornecedor_novo, name='fornecedor_novo'),
    path('fornecedores/<int:pk>/editar/', views.fornecedor_editar, name='fornecedor_editar'),
    path('fornecedores/<int:pk>/deletar/', views.fornecedor_deletar, name='fornecedor_deletar'),
    
    # Vendas
    path('veiculos/<int:veiculo_pk>/vender/', views.venda_nova, name='venda_nova'),
    path('vendas/', views.venda_lista, name='venda_lista'),
    path('vendas/<int:pk>/', views.venda_detalhe, name='venda_detalhe'),
    
    # Relatórios
    path('relatorios/geral/', views.relatorio_geral, name='relatorio_geral'),
    path('relatorios/por-veiculo/', views.relatorio_por_veiculo, name='relatorio_por_veiculo'),
    
    # Configurações
    path('tipos-despesa/', views.tipo_despesa_lista, name='tipo_despesa_lista'),
    path('tipos-despesa/novo/', views.tipo_despesa_novo, name='tipo_despesa_novo'),
    path('formas-pagamento/', views.forma_pagamento_lista, name='forma_pagamento_lista'),
    path('formas-pagamento/nova/', views.forma_pagamento_nova, name='forma_pagamento_nova'),
]
