import json as _json
from django import forms
from django.forms import inlineformset_factory
from .models import (
    Veiculo, Despesa, Cliente, Fornecedor,
    Venda, VendaPagamento, VendaVeiculoEntrada, TipoDespesa, FormaPagamento,
    COMBUSTIVEL_CHOICES, CAMBIO_CHOICES, CATEGORIA_CHOICES,
    ESTADO_CIVIL_CHOICES, UF_CHOICES,
)

# Classes CSS reutilizáveis
_INPUT = (
    'block w-full rounded-lg border border-gray-200 bg-gray-50 px-4 py-2.5 text-sm '
    'text-gray-900 placeholder-gray-400 focus:bg-white focus:border-blue-500 '
    'focus:ring-2 focus:ring-blue-500/20 transition-colors'
)
_SELECT = (
    'block w-full rounded-lg border border-gray-200 bg-gray-50 px-4 py-2.5 text-sm '
    'text-gray-900 focus:bg-white focus:border-blue-500 '
    'focus:ring-2 focus:ring-blue-500/20 transition-colors'
)
_TEXTAREA = (
    'block w-full rounded-lg border border-gray-200 bg-gray-50 px-4 py-2.5 text-sm '
    'text-gray-900 placeholder-gray-400 focus:bg-white focus:border-blue-500 '
    'focus:ring-2 focus:ring-blue-500/20 transition-colors resize-none'
)
_CHECKBOX = 'rounded border-gray-300 text-blue-600 focus:ring-blue-500'
_DATE = (
    'block w-full rounded-lg border border-gray-200 bg-gray-50 px-4 py-2.5 text-sm '
    'text-gray-900 focus:bg-white focus:border-blue-500 '
    'focus:ring-2 focus:ring-blue-500/20 transition-colors'
)


class VeiculoForm(forms.ModelForm):
    class Meta:
        model = Veiculo
        fields = [
            # Identificação
            'marca', 'modelo', 'ano', 'placa', 'cor', 'categoria',
            # Especificações
            'combustivel', 'cambio', 'portas', 'motor', 'km', 'cor_interior',
            # Documentação
            'renavam', 'chassi', 'numero_proprietarios',
            # Financeiro
            'valor_compra', 'valor_venda', 'fipe', 'fornecedor', 'data_compra',
            # Status
            'status', 'observacoes',
        ]
        widgets = {
            'marca': forms.TextInput(attrs={'class': _INPUT, 'placeholder': 'Ex: Toyota, Honda, Ford'}),
            'modelo': forms.TextInput(attrs={'class': _INPUT, 'placeholder': 'Ex: Corolla, Civic, Ka'}),
            'ano': forms.NumberInput(attrs={'class': _INPUT, 'placeholder': '2020', 'min': '1900', 'max': '2030'}),
            'placa': forms.TextInput(attrs={'class': _INPUT, 'placeholder': 'ABC-1234 ou ABC1D23', 'style': 'text-transform:uppercase'}),
            'cor': forms.TextInput(attrs={'class': _INPUT, 'placeholder': 'Ex: Prata, Branco, Preto'}),
            'categoria': forms.Select(attrs={'class': _SELECT}, choices=CATEGORIA_CHOICES),
            'combustivel': forms.Select(attrs={'class': _SELECT}, choices=COMBUSTIVEL_CHOICES),
            'cambio': forms.Select(attrs={'class': _SELECT}, choices=CAMBIO_CHOICES),
            'portas': forms.NumberInput(attrs={'class': _INPUT, 'placeholder': '4', 'min': '1', 'max': '8'}),
            'motor': forms.TextInput(attrs={'class': _INPUT, 'placeholder': 'Ex: 1.6 16V Flex'}),
            'km': forms.NumberInput(attrs={'class': _INPUT, 'placeholder': '50000', 'min': '0'}),
            'cor_interior': forms.TextInput(attrs={'class': _INPUT, 'placeholder': 'Ex: Bege, Preto'}),
            'renavam': forms.TextInput(attrs={'class': _INPUT, 'placeholder': '00000000000', 'maxlength': '11'}),
            'chassi': forms.TextInput(attrs={'class': _INPUT, 'placeholder': '9BWZZZ377VT004251', 'style': 'text-transform:uppercase'}),
            'numero_proprietarios': forms.NumberInput(attrs={'class': _INPUT, 'placeholder': '1', 'min': '0'}),
            'valor_compra': forms.NumberInput(attrs={'class': _INPUT, 'placeholder': '0,00', 'step': '0.01', 'min': '0'}),
            'valor_venda': forms.NumberInput(attrs={'class': _INPUT, 'placeholder': '0,00', 'step': '0.01', 'min': '0'}),
            'fipe': forms.NumberInput(attrs={'class': _INPUT, 'placeholder': '0,00', 'step': '0.01', 'min': '0'}),
            'fornecedor': forms.Select(attrs={'class': _SELECT}),
            'data_compra': forms.DateInput(attrs={'class': _DATE, 'type': 'date'}),
            'status': forms.Select(attrs={'class': _SELECT}),
            'observacoes': forms.Textarea(attrs={'class': _TEXTAREA, 'rows': 4, 'placeholder': 'Observações gerais sobre o veículo...'}),
        }


class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = [
            # Dados pessoais
            'nome', 'cpf', 'rg', 'data_nascimento', 'estado_civil', 'profissao',
            # Documentos
            'cnh',
            # Contato
            'telefone', 'email',
            # Endereço
            'cep', 'cidade', 'estado_uf', 'endereco',
            # Extra
            'observacoes',
        ]
        widgets = {
            'nome': forms.TextInput(attrs={'class': _INPUT, 'placeholder': 'Nome completo'}),
            'cpf': forms.TextInput(attrs={'class': _INPUT, 'placeholder': '000.000.000-00'}),
            'rg': forms.TextInput(attrs={'class': _INPUT, 'placeholder': '00.000.000-0'}),
            'data_nascimento': forms.DateInput(attrs={'class': _DATE, 'type': 'date'}),
            'estado_civil': forms.Select(attrs={'class': _SELECT}, choices=ESTADO_CIVIL_CHOICES),
            'profissao': forms.TextInput(attrs={'class': _INPUT, 'placeholder': 'Ex: Empresário, Autônomo'}),
            'cnh': forms.TextInput(attrs={'class': _INPUT, 'placeholder': '00000000000'}),
            'telefone': forms.TextInput(attrs={'class': _INPUT, 'placeholder': '(00) 00000-0000'}),
            'email': forms.EmailInput(attrs={'class': _INPUT, 'placeholder': 'email@exemplo.com'}),
            'cep': forms.TextInput(attrs={'class': _INPUT, 'placeholder': '00000-000', 'maxlength': '9', 'id': 'id_cep'}),
            'cidade': forms.TextInput(attrs={'class': _INPUT, 'placeholder': 'Cidade', 'id': 'id_cidade'}),
            'estado_uf': forms.Select(attrs={'class': _SELECT}, choices=UF_CHOICES),
            'endereco': forms.Textarea(attrs={'class': _TEXTAREA, 'rows': 2, 'placeholder': 'Rua, número, bairro...'}),
            'observacoes': forms.Textarea(attrs={'class': _TEXTAREA, 'rows': 3, 'placeholder': 'Observações sobre o cliente...'}),
        }


class FornecedorForm(forms.ModelForm):
    class Meta:
        model = Fornecedor
        fields = ['nome', 'cnpj_cpf', 'telefone', 'email', 'endereco', 'ativo']
        widgets = {
            'nome': forms.TextInput(attrs={'class': _INPUT, 'placeholder': 'Nome do fornecedor'}),
            'cnpj_cpf': forms.TextInput(attrs={'class': _INPUT, 'placeholder': 'CNPJ ou CPF'}),
            'telefone': forms.TextInput(attrs={'class': _INPUT, 'placeholder': '(00) 00000-0000'}),
            'email': forms.EmailInput(attrs={'class': _INPUT, 'placeholder': 'email@exemplo.com'}),
            'endereco': forms.Textarea(attrs={'class': _TEXTAREA, 'rows': 3, 'placeholder': 'Endereço completo'}),
            'ativo': forms.CheckboxInput(attrs={'class': _CHECKBOX}),
        }


class DespesaForm(forms.ModelForm):
    class Meta:
        model = Despesa
        fields = ['tipo', 'fornecedor', 'valor', 'descricao', 'data_despesa']
        widgets = {
            'tipo': forms.Select(attrs={'class': _SELECT}),
            'fornecedor': forms.Select(attrs={'class': _SELECT}),
            'valor': forms.NumberInput(attrs={'class': _INPUT, 'placeholder': '0,00', 'step': '0.01', 'min': '0'}),
            'descricao': forms.Textarea(attrs={'class': _TEXTAREA, 'rows': 3, 'placeholder': 'Descrição detalhada da despesa...'}),
            'data_despesa': forms.DateInput(attrs={'class': _DATE, 'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['fornecedor'].required = False
        self.fields['fornecedor'].empty_label = '-- Nenhum --'


class VendaForm(forms.ModelForm):
    class Meta:
        model = Venda
        fields = ['cliente', 'valor_venda', 'data_venda', 'observacoes']
        widgets = {
            'cliente': forms.Select(attrs={'class': _SELECT}),
            'valor_venda': forms.NumberInput(attrs={'class': _INPUT, 'placeholder': '0,00', 'step': '0.01'}),
            'data_venda': forms.DateInput(attrs={'class': _DATE, 'type': 'date'}),
            'observacoes': forms.Textarea(attrs={'class': _TEXTAREA, 'rows': 3, 'placeholder': 'Observações sobre a venda...'}),
        }

    def __init__(self, *args, **kwargs):
        veiculo = kwargs.pop('veiculo', None)
        super().__init__(*args, **kwargs)
        if veiculo:
            self.fields['valor_venda'].initial = veiculo.valor_venda


class VeiculoTrocaForm(forms.ModelForm):
    class Meta:
        model = Veiculo
        fields = ['marca', 'modelo', 'ano', 'placa', 'cor', 'valor_compra']
        widgets = {
            'marca': forms.TextInput(attrs={'class': _INPUT, 'placeholder': 'Ex: Toyota'}),
            'modelo': forms.TextInput(attrs={'class': _INPUT, 'placeholder': 'Ex: Corolla'}),
            'ano': forms.NumberInput(attrs={'class': _INPUT, 'placeholder': '2020', 'min': '1900', 'max': '2030'}),
            'placa': forms.TextInput(attrs={'class': _INPUT, 'placeholder': 'ABC-1234', 'style': 'text-transform:uppercase'}),
            'cor': forms.TextInput(attrs={'class': _INPUT, 'placeholder': 'Ex: Prata, Branco'}),
            'valor_compra': forms.NumberInput(attrs={'class': _INPUT, 'placeholder': 'Valor de avaliação (R$)', 'step': '0.01', 'min': '0'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['placa'].required = False
        self.fields['cor'].required = False


VendaPagamentoFormSet = inlineformset_factory(
    Venda, VendaPagamento,
    fields=['forma_pagamento', 'valor', 'observacao'],
    extra=0, can_delete=True, min_num=0, validate_min=False,
    widgets={
        'forma_pagamento': forms.Select(attrs={'class': _SELECT}),
        'valor': forms.NumberInput(attrs={'class': _INPUT, 'step': '0.01', 'min': '0', 'placeholder': '0,00'}),
        'observacao': forms.TextInput(attrs={'class': _INPUT, 'placeholder': 'Observação (opcional)'}),
    }
)

VendaVeiculoEntradaFormSet = inlineformset_factory(
    Venda, VendaVeiculoEntrada,
    fields=['veiculo', 'valor'],
    extra=0, can_delete=True, min_num=0, validate_min=False,
    widgets={
        'veiculo': forms.Select(attrs={'class': _SELECT}),
        'valor': forms.NumberInput(attrs={'class': _INPUT, 'step': '0.01', 'min': '0', 'placeholder': '0,00'}),
    }
)


class TipoDespesaForm(forms.ModelForm):
    class Meta:
        model = TipoDespesa
        fields = ['nome', 'descricao', 'ativo']
        widgets = {
            'nome': forms.TextInput(attrs={'class': _INPUT, 'placeholder': 'Ex: Mecânica, Funilaria, IPVA'}),
            'descricao': forms.Textarea(attrs={'class': _TEXTAREA, 'rows': 3}),
            'ativo': forms.CheckboxInput(attrs={'class': _CHECKBOX}),
        }


class FormaPagamentoForm(forms.ModelForm):
    class Meta:
        model = FormaPagamento
        fields = ['nome', 'ativo']
        widgets = {
            'nome': forms.TextInput(attrs={'class': _INPUT, 'placeholder': 'Ex: Dinheiro, PIX, Cartão'}),
            'ativo': forms.CheckboxInput(attrs={'class': _CHECKBOX}),
        }


class EstornoVendaForm(forms.Form):
    motivo = forms.CharField(
        label='Motivo do estorno',
        widget=forms.Textarea(attrs={'class': _TEXTAREA, 'rows': 3, 'placeholder': 'Ex: cliente desistiu da compra'}),
    )
