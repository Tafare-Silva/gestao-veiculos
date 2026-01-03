from django.contrib import admin
from .models import (
    Fornecedor, Cliente, Veiculo, VeiculoImagem, TipoDespesa, 
    Despesa, FormaPagamento, Venda
)


@admin.register(Fornecedor)
class FornecedorAdmin(admin.ModelAdmin):
    list_display = ['nome', 'cnpj_cpf', 'telefone', 'email', 'ativo']
    list_filter = ['ativo']
    search_fields = ['nome', 'cnpj_cpf', 'email']


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ['nome', 'cpf', 'telefone', 'email', 'data_cadastro']
    search_fields = ['nome', 'cpf', 'email']
    date_hierarchy = 'data_cadastro'


class VeiculoImagemInline(admin.TabularInline):
    model = VeiculoImagem
    extra = 1
    fields = ['imagem', 'descricao', 'principal', 'ordem']


@admin.register(Veiculo)
class VeiculoAdmin(admin.ModelAdmin):
    list_display = ['marca', 'modelo', 'ano', 'placa', 'renavam', 'status', 'valor_compra', 'valor_venda']
    list_filter = ['status', 'marca', 'ano']
    search_fields = ['marca', 'modelo', 'placa', 'chassi', 'renavam']
    date_hierarchy = 'data_compra'
    inlines = [VeiculoImagemInline]


@admin.register(VeiculoImagem)
class VeiculoImagemAdmin(admin.ModelAdmin):
    list_display = ['veiculo', 'descricao', 'principal', 'ordem', 'data_upload']
    list_filter = ['principal', 'data_upload']
    search_fields = ['veiculo__placa', 'descricao']


@admin.register(TipoDespesa)
class TipoDespesaAdmin(admin.ModelAdmin):
    list_display = ['nome', 'ativo']
    list_filter = ['ativo']


@admin.register(Despesa)
class DespesaAdmin(admin.ModelAdmin):
    list_display = ['veiculo', 'tipo', 'valor', 'fornecedor', 'data_despesa']
    list_filter = ['tipo', 'data_despesa']
    search_fields = ['veiculo__placa', 'descricao']
    date_hierarchy = 'data_despesa'


@admin.register(FormaPagamento)
class FormaPagamentoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'ativo']
    list_filter = ['ativo']


@admin.register(Venda)
class VendaAdmin(admin.ModelAdmin):
    list_display = ['veiculo', 'cliente', 'valor_venda', 'valor_entrada', 'valor_final', 'data_venda']
    list_filter = ['forma_pagamento', 'data_venda']
    search_fields = ['veiculo__placa', 'cliente__nome']
    date_hierarchy = 'data_venda'
