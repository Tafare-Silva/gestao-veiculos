from django import forms
from .models import (
    Veiculo, Despesa, Cliente, Fornecedor, 
    Venda, TipoDespesa, FormaPagamento
)


class VeiculoForm(forms.ModelForm):
    class Meta:
        model = Veiculo
        fields = [
            'marca', 'modelo', 'ano', 'placa', 'renavam', 'cor', 'km', 'chassi',
            'valor_compra', 'valor_venda', 'fornecedor', 'status',
            'data_compra', 'observacoes'
        ]
        widgets = {
            'marca': forms.TextInput(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500',
                'placeholder': 'Ex: Toyota'
            }),
            'modelo': forms.TextInput(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500',
                'placeholder': 'Ex: Corolla'
            }),
            'ano': forms.NumberInput(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500',
                'placeholder': '2020'
            }),
            'placa': forms.TextInput(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500',
                'placeholder': 'ABC-1234'
            }),
            'renavam': forms.TextInput(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500',
                'placeholder': '00000000000 (11 dígitos)',
                'maxlength': '11'
            }),
            'cor': forms.TextInput(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500',
                'placeholder': 'Prata'
            }),
            'km': forms.NumberInput(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500',
                'placeholder': '50000'
            }),
            'chassi': forms.TextInput(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500',
                'placeholder': '9BWZZZ377VT004251'
            }),
            'valor_compra': forms.NumberInput(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500',
                'placeholder': '20000.00',
                'step': '0.01'
            }),
            'valor_venda': forms.NumberInput(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500',
                'placeholder': '30000.00',
                'step': '0.01'
            }),
            'fornecedor': forms.Select(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500'
            }),
            'status': forms.Select(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500'
            }),
            'data_compra': forms.DateInput(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500',
                'type': 'date'
            }),
            'observacoes': forms.Textarea(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500',
                'rows': 3,
                'placeholder': 'Observações gerais sobre o veículo...'
            }),
        }


class DespesaForm(forms.ModelForm):
    class Meta:
        model = Despesa
        fields = ['tipo', 'fornecedor', 'valor', 'descricao', 'data_despesa']
        widgets = {
            'tipo': forms.Select(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500'
            }),
            'fornecedor': forms.Select(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500'
            }),
            'valor': forms.NumberInput(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500',
                'placeholder': '500.00',
                'step': '0.01'
            }),
            'descricao': forms.Textarea(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500',
                'rows': 3,
                'placeholder': 'Descrição detalhada da despesa...'
            }),
            'data_despesa': forms.DateInput(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500',
                'type': 'date'
            }),
        }


class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nome', 'cpf', 'telefone', 'email', 'endereco']
        widgets = {
            'nome': forms.TextInput(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500',
                'placeholder': 'Nome completo'
            }),
            'cpf': forms.TextInput(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500',
                'placeholder': '000.000.000-00'
            }),
            'telefone': forms.TextInput(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500',
                'placeholder': '(00) 00000-0000'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500',
                'placeholder': 'email@exemplo.com'
            }),
            'endereco': forms.Textarea(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500',
                'rows': 3,
                'placeholder': 'Endereço completo'
            }),
        }


class FornecedorForm(forms.ModelForm):
    class Meta:
        model = Fornecedor
        fields = ['nome', 'cnpj_cpf', 'telefone', 'email', 'endereco', 'ativo']
        widgets = {
            'nome': forms.TextInput(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500',
                'placeholder': 'Nome do fornecedor'
            }),
            'cnpj_cpf': forms.TextInput(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500',
                'placeholder': 'CNPJ ou CPF'
            }),
            'telefone': forms.TextInput(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500',
                'placeholder': '(00) 00000-0000'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500',
                'placeholder': 'email@exemplo.com'
            }),
            'endereco': forms.Textarea(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500',
                'rows': 3,
                'placeholder': 'Endereço completo'
            }),
            'ativo': forms.CheckboxInput(attrs={
                'class': 'rounded border-gray-300 text-blue-600 focus:ring-blue-500'
            }),
        }


class VendaForm(forms.ModelForm):
    class Meta:
        model = Venda
        fields = [
            'cliente', 'valor_venda', 'veiculo_entrada', 
            'valor_entrada', 'forma_pagamento', 'data_venda', 'observacoes'
        ]
        widgets = {
            'cliente': forms.Select(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500'
            }),
            'valor_venda': forms.NumberInput(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500',
                'placeholder': '30000.00',
                'step': '0.01'
            }),
            'veiculo_entrada': forms.Select(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500'
            }),
            'valor_entrada': forms.NumberInput(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500',
                'placeholder': '0.00',
                'step': '0.01'
            }),
            'forma_pagamento': forms.Select(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500'
            }),
            'data_venda': forms.DateInput(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500',
                'type': 'date'
            }),
            'observacoes': forms.Textarea(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500',
                'rows': 3,
                'placeholder': 'Observações sobre a venda...'
            }),
        }

    def __init__(self, *args, **kwargs):
        veiculo = kwargs.pop('veiculo', None)
        super().__init__(*args, **kwargs)
        
        # Preenche o valor de venda automaticamente
        if veiculo:
            self.fields['valor_venda'].initial = veiculo.valor_venda
            
        # Filtra apenas veículos disponíveis para entrada
        self.fields['veiculo_entrada'].queryset = Veiculo.objects.filter(
            status='disponivel'
        ).exclude(id=veiculo.id if veiculo else None)
        self.fields['veiculo_entrada'].required = False


class TipoDespesaForm(forms.ModelForm):
    class Meta:
        model = TipoDespesa
        fields = ['nome', 'descricao', 'ativo']
        widgets = {
            'nome': forms.TextInput(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500',
                'placeholder': 'Ex: Mecânica, Funilaria, IPVA'
            }),
            'descricao': forms.Textarea(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500',
                'rows': 3
            }),
            'ativo': forms.CheckboxInput(attrs={
                'class': 'rounded border-gray-300 text-blue-600 focus:ring-blue-500'
            }),
        }


class FormaPagamentoForm(forms.ModelForm):
    class Meta:
        model = FormaPagamento
        fields = ['nome', 'ativo']
        widgets = {
            'nome': forms.TextInput(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500',
                'placeholder': 'Ex: Dinheiro, PIX, Cartão'
            }),
            'ativo': forms.CheckboxInput(attrs={
                'class': 'rounded border-gray-300 text-blue-600 focus:ring-blue-500'
            }),
        }
