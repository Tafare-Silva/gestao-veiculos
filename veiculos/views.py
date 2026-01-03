from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Sum, Q, Count
from decimal import Decimal
from .models import (
    Veiculo, VeiculoImagem, Despesa, Cliente, Fornecedor, Venda,
    TipoDespesa, FormaPagamento
)
from .forms import (
    VeiculoForm, DespesaForm, ClienteForm, FornecedorForm,
    VendaForm, TipoDespesaForm, FormaPagamentoForm
)


# ============= DASHBOARD =============

def dashboard(request):
    """Dashboard principal com resumo geral"""
    from datetime import datetime, timedelta
    
    # Filtros de período
    data_inicio = request.GET.get('data_inicio')
    data_fim = request.GET.get('data_fim')
    periodo_rapido = request.GET.get('periodo')
    
    # Períodos rápidos
    hoje = datetime.now().date()
    if periodo_rapido == 'hoje':
        data_inicio = hoje
        data_fim = hoje
    elif periodo_rapido == 'semana':
        data_inicio = hoje - timedelta(days=7)
        data_fim = hoje
    elif periodo_rapido == 'mes':
        data_inicio = hoje.replace(day=1)
        data_fim = hoje
    elif periodo_rapido == 'ano':
        data_inicio = hoje.replace(month=1, day=1)
        data_fim = hoje
    
    # Query base de vendas
    vendas = Venda.objects.all()
    
    # Aplicar filtros de data
    if data_inicio:
        vendas = vendas.filter(data_venda__gte=data_inicio)
    if data_fim:
        vendas = vendas.filter(data_venda__lte=data_fim)
    
    total_veiculos_disponiveis = Veiculo.objects.filter(status='disponivel').count()
    total_veiculos_vendidos = Veiculo.objects.filter(status='vendido').count()
    
    # Total de vendas
    total_vendas = vendas.aggregate(
        total=Sum('valor_venda')
    )['total'] or Decimal('0.00')
    
    # Total de despesas (filtrado por período se aplicável)
    despesas = Despesa.objects.all()
    if data_inicio:
        despesas = despesas.filter(data_despesa__gte=data_inicio)
    if data_fim:
        despesas = despesas.filter(data_despesa__lte=data_fim)
    
    total_despesas = despesas.aggregate(
        total=Sum('valor')
    )['total'] or Decimal('0.00')
    
    # Lucro total (apenas veículos vendidos no período)
    veiculos_vendidos_ids = vendas.values_list('veiculo_id', flat=True)
    veiculos_vendidos = Veiculo.objects.filter(id__in=veiculos_vendidos_ids)
    lucro_total = Decimal('0.00')
    
    for veiculo in veiculos_vendidos:
        if hasattr(veiculo, 'venda'):
            lucro = veiculo.lucro_real()
            if lucro:
                lucro_total += lucro
    
    # Últimas vendas (do período ou geral)
    ultimas_vendas = vendas.select_related('veiculo', 'cliente').order_by('-data_venda')[:5]
    
    # Veículos disponíveis
    veiculos_disponiveis = Veiculo.objects.filter(status='disponivel').order_by('-data_cadastro')[:5]
    
    context = {
        'total_veiculos_disponiveis': total_veiculos_disponiveis,
        'total_veiculos_vendidos': total_veiculos_vendidos,
        'total_vendas': total_vendas,
        'total_despesas': total_despesas,
        'lucro_total': lucro_total,
        'ultimas_vendas': ultimas_vendas,
        'veiculos_disponiveis': veiculos_disponiveis,
        'data_inicio': data_inicio,
        'data_fim': data_fim,
        'periodo_rapido': periodo_rapido,
    }
    
    return render(request, 'veiculos/dashboard.html', context)


# ============= VEÍCULOS =============

def veiculo_lista(request):
    """Lista todos os veículos"""
    veiculos = Veiculo.objects.all().select_related('fornecedor').order_by('-data_cadastro')
    
    # Filtros
    status = request.GET.get('status')
    if status:
        veiculos = veiculos.filter(status=status)
    
    busca = request.GET.get('busca')
    if busca:
        veiculos = veiculos.filter(
            Q(marca__icontains=busca) |
            Q(modelo__icontains=busca) |
            Q(placa__icontains=busca)
        )
    
    context = {'veiculos': veiculos}
    return render(request, 'veiculos/veiculo_lista.html', context)


def veiculo_detalhe(request, pk):
    """Detalhes de um veículo"""
    veiculo = get_object_or_404(Veiculo, pk=pk)
    despesas = veiculo.despesas.all().select_related('tipo', 'fornecedor')
    
    context = {
        'veiculo': veiculo,
        'despesas': despesas,
    }
    return render(request, 'veiculos/veiculo_detalhe.html', context)


def veiculo_novo(request):
    """Criar novo veículo"""
    if request.method == 'POST':
        form = VeiculoForm(request.POST, request.FILES)
        if form.is_valid():
            veiculo = form.save()
            
            # Processar imagens enviadas
            imagens = request.FILES.getlist('imagens')
            for idx, imagem in enumerate(imagens):
                VeiculoImagem.objects.create(
                    veiculo=veiculo,
                    imagem=imagem,
                    principal=(idx == 0),  # Primeira imagem é principal
                    ordem=idx
                )
            
            messages.success(request, 'Veículo cadastrado com sucesso!')
            return redirect('veiculo_detalhe', pk=veiculo.pk)
    else:
        form = VeiculoForm()
    
    context = {'form': form, 'titulo': 'Novo Veículo'}
    return render(request, 'veiculos/veiculo_form.html', context)


def veiculo_editar(request, pk):
    """Editar veículo"""
    veiculo = get_object_or_404(Veiculo, pk=pk)
    
    if request.method == 'POST':
        form = VeiculoForm(request.POST, request.FILES, instance=veiculo)
        if form.is_valid():
            form.save()
            
            # Processar novas imagens
            imagens = request.FILES.getlist('imagens')
            for idx, imagem in enumerate(imagens):
                ordem_atual = veiculo.imagens.count() + idx
                VeiculoImagem.objects.create(
                    veiculo=veiculo,
                    imagem=imagem,
                    ordem=ordem_atual
                )
            
            messages.success(request, 'Veículo atualizado com sucesso!')
            return redirect('veiculo_detalhe', pk=veiculo.pk)
    else:
        form = VeiculoForm(instance=veiculo)
    
    imagens = veiculo.imagens.all()
    context = {'form': form, 'titulo': 'Editar Veículo', 'veiculo': veiculo, 'imagens': imagens}
    return render(request, 'veiculos/veiculo_form.html', context)


def veiculo_deletar(request, pk):
    """Deletar veículo"""
    veiculo = get_object_or_404(Veiculo, pk=pk)
    
    if request.method == 'POST':
        veiculo.delete()
        messages.success(request, 'Veículo deletado com sucesso!')
        return redirect('veiculo_lista')
    
    context = {'veiculo': veiculo}
    return render(request, 'veiculos/veiculo_confirm_delete.html', context)


def veiculo_imagem_deletar(request, pk):
    """Deletar uma imagem do veículo"""
    imagem = get_object_or_404(VeiculoImagem, pk=pk)
    veiculo_pk = imagem.veiculo.pk
    
    if request.method == 'POST':
        imagem.delete()
        messages.success(request, 'Imagem removida com sucesso!')
        return redirect('veiculo_editar', pk=veiculo_pk)
    
    return redirect('veiculo_editar', pk=veiculo_pk)


def veiculo_imagem_principal(request, pk):
    """Marcar uma imagem como principal"""
    imagem = get_object_or_404(VeiculoImagem, pk=pk)
    veiculo_pk = imagem.veiculo.pk
    
    # Desmarcar todas as outras
    VeiculoImagem.objects.filter(veiculo=imagem.veiculo).update(principal=False)
    
    # Marcar esta como principal
    imagem.principal = True
    imagem.save()
    
    messages.success(request, 'Imagem principal atualizada!')
    return redirect('veiculo_editar', pk=veiculo_pk)


# ============= DESPESAS =============

def despesa_nova(request, veiculo_pk):
    """Adicionar despesa a um veículo"""
    veiculo = get_object_or_404(Veiculo, pk=veiculo_pk)
    
    if request.method == 'POST':
        form = DespesaForm(request.POST)
        if form.is_valid():
            despesa = form.save(commit=False)
            despesa.veiculo = veiculo
            despesa.save()
            messages.success(request, 'Despesa adicionada com sucesso!')
            return redirect('veiculo_detalhe', pk=veiculo.pk)
    else:
        form = DespesaForm()
    
    context = {'form': form, 'veiculo': veiculo, 'titulo': 'Nova Despesa'}
    return render(request, 'veiculos/despesa_form.html', context)


def despesa_editar(request, pk):
    """Editar despesa"""
    despesa = get_object_or_404(Despesa, pk=pk)
    
    if request.method == 'POST':
        form = DespesaForm(request.POST, instance=despesa)
        if form.is_valid():
            form.save()
            messages.success(request, 'Despesa atualizada com sucesso!')
            return redirect('veiculo_detalhe', pk=despesa.veiculo.pk)
    else:
        form = DespesaForm(instance=despesa)
    
    context = {'form': form, 'despesa': despesa, 'titulo': 'Editar Despesa'}
    return render(request, 'veiculos/despesa_form.html', context)


def despesa_deletar(request, pk):
    """Deletar despesa"""
    despesa = get_object_or_404(Despesa, pk=pk)
    veiculo_pk = despesa.veiculo.pk
    
    if request.method == 'POST':
        despesa.delete()
        messages.success(request, 'Despesa deletada com sucesso!')
        return redirect('veiculo_detalhe', pk=veiculo_pk)
    
    context = {'despesa': despesa}
    return render(request, 'veiculos/despesa_confirm_delete.html', context)


# ============= CLIENTES =============

def cliente_lista(request):
    """Lista todos os clientes"""
    clientes = Cliente.objects.all().order_by('nome')
    
    busca = request.GET.get('busca')
    if busca:
        clientes = clientes.filter(
            Q(nome__icontains=busca) |
            Q(cpf__icontains=busca) |
            Q(telefone__icontains=busca)
        )
    
    context = {'clientes': clientes}
    return render(request, 'veiculos/cliente_lista.html', context)


def cliente_novo(request):
    """Criar novo cliente"""
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            cliente = form.save()
            messages.success(request, 'Cliente cadastrado com sucesso!')
            return redirect('cliente_lista')
    else:
        form = ClienteForm()
    
    context = {'form': form, 'titulo': 'Novo Cliente'}
    return render(request, 'veiculos/cliente_form.html', context)


def cliente_editar(request, pk):
    """Editar cliente"""
    cliente = get_object_or_404(Cliente, pk=pk)
    
    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cliente atualizado com sucesso!')
            return redirect('cliente_lista')
    else:
        form = ClienteForm(instance=cliente)
    
    context = {'form': form, 'titulo': 'Editar Cliente', 'cliente': cliente}
    return render(request, 'veiculos/cliente_form.html', context)


def cliente_deletar(request, pk):
    """Deletar cliente"""
    cliente = get_object_or_404(Cliente, pk=pk)
    
    if request.method == 'POST':
        cliente.delete()
        messages.success(request, 'Cliente deletado com sucesso!')
        return redirect('cliente_lista')
    
    context = {'cliente': cliente}
    return render(request, 'veiculos/cliente_confirm_delete.html', context)


# ============= FORNECEDORES =============

def fornecedor_lista(request):
    """Lista todos os fornecedores"""
    fornecedores = Fornecedor.objects.all().order_by('nome')
    
    busca = request.GET.get('busca')
    if busca:
        fornecedores = fornecedores.filter(
            Q(nome__icontains=busca) |
            Q(cnpj_cpf__icontains=busca)
        )
    
    context = {'fornecedores': fornecedores}
    return render(request, 'veiculos/fornecedor_lista.html', context)


def fornecedor_novo(request):
    """Criar novo fornecedor"""
    if request.method == 'POST':
        form = FornecedorForm(request.POST)
        if form.is_valid():
            fornecedor = form.save()
            messages.success(request, 'Fornecedor cadastrado com sucesso!')
            return redirect('fornecedor_lista')
    else:
        form = FornecedorForm()
    
    context = {'form': form, 'titulo': 'Novo Fornecedor'}
    return render(request, 'veiculos/fornecedor_form.html', context)


def fornecedor_editar(request, pk):
    """Editar fornecedor"""
    fornecedor = get_object_or_404(Fornecedor, pk=pk)
    
    if request.method == 'POST':
        form = FornecedorForm(request.POST, instance=fornecedor)
        if form.is_valid():
            form.save()
            messages.success(request, 'Fornecedor atualizado com sucesso!')
            return redirect('fornecedor_lista')
    else:
        form = FornecedorForm(instance=fornecedor)
    
    context = {'form': form, 'titulo': 'Editar Fornecedor', 'fornecedor': fornecedor}
    return render(request, 'veiculos/fornecedor_form.html', context)


def fornecedor_deletar(request, pk):
    """Deletar fornecedor"""
    fornecedor = get_object_or_404(Fornecedor, pk=pk)
    
    if request.method == 'POST':
        fornecedor.delete()
        messages.success(request, 'Fornecedor deletado com sucesso!')
        return redirect('fornecedor_lista')
    
    context = {'fornecedor': fornecedor}
    return render(request, 'veiculos/fornecedor_confirm_delete.html', context)


# ============= VENDAS =============

def venda_nova(request, veiculo_pk):
    """Realizar venda de um veículo"""
    veiculo = get_object_or_404(Veiculo, pk=veiculo_pk)
    
    if veiculo.status == 'vendido':
        messages.error(request, 'Este veículo já foi vendido!')
        return redirect('veiculo_detalhe', pk=veiculo.pk)
    
    if request.method == 'POST':
        form = VendaForm(request.POST, veiculo=veiculo)
        if form.is_valid():
            venda = form.save(commit=False)
            venda.veiculo = veiculo
            venda.save()
            
            # Se houver veículo de entrada, marca ele como vendido também
            # pois ele saiu do cliente e entrou no nosso estoque
            if venda.veiculo_entrada:
                veiculo_entrada = venda.veiculo_entrada
                veiculo_entrada.status = 'disponivel'  # Fica disponível no nosso estoque
                veiculo_entrada.save()
            
            messages.success(request, 'Venda realizada com sucesso!')
            return redirect('venda_detalhe', pk=venda.pk)
    else:
        form = VendaForm(veiculo=veiculo)
    
    context = {'form': form, 'veiculo': veiculo, 'titulo': 'Nova Venda'}
    return render(request, 'veiculos/venda_form.html', context)


def venda_lista(request):
    """Lista todas as vendas"""
    vendas = Venda.objects.all().select_related('veiculo', 'cliente').order_by('-data_venda')
    
    context = {'vendas': vendas}
    return render(request, 'veiculos/venda_lista.html', context)


def venda_detalhe(request, pk):
    """Detalhes de uma venda"""
    venda = get_object_or_404(Venda, pk=pk)
    
    context = {'venda': venda}
    return render(request, 'veiculos/venda_detalhe.html', context)


# ============= RELATÓRIOS =============

def relatorio_geral(request):
    """Relatório geral de vendas e despesas"""
    vendas = Venda.objects.all().select_related('veiculo', 'cliente')
    
    total_vendas = vendas.aggregate(
        total=Sum('valor_venda')
    )['total'] or Decimal('0.00')
    
    total_entradas = vendas.aggregate(
        total=Sum('valor_entrada')
    )['total'] or Decimal('0.00')
    
    total_despesas = Despesa.objects.aggregate(
        total=Sum('valor')
    )['total'] or Decimal('0.00')
    
    # Calcular lucro total
    veiculos_vendidos = Veiculo.objects.filter(status='vendido')
    lucro_total = Decimal('0.00')
    
    for veiculo in veiculos_vendidos:
        lucro = veiculo.lucro_real()
        if lucro:
            lucro_total += lucro
    
    context = {
        'total_vendas': total_vendas,
        'total_entradas': total_entradas,
        'total_despesas': total_despesas,
        'lucro_total': lucro_total,
        'vendas': vendas,
    }
    
    return render(request, 'veiculos/relatorio_geral.html', context)


def relatorio_por_veiculo(request):
    """Relatório de lucro por veículo com filtros"""
    # Filtros
    data_inicio = request.GET.get('data_inicio')
    data_fim = request.GET.get('data_fim')
    veiculo_id = request.GET.get('veiculo')
    cliente_id = request.GET.get('cliente')
    
    # Query base
    veiculos_vendidos = Veiculo.objects.filter(status='vendido').select_related('venda', 'venda__cliente', 'venda__veiculo_entrada')
    
    # Aplicar filtros
    if data_inicio:
        veiculos_vendidos = veiculos_vendidos.filter(venda__data_venda__gte=data_inicio)
    if data_fim:
        veiculos_vendidos = veiculos_vendidos.filter(venda__data_venda__lte=data_fim)
    if veiculo_id:
        veiculos_vendidos = veiculos_vendidos.filter(id=veiculo_id)
    if cliente_id:
        veiculos_vendidos = veiculos_vendidos.filter(venda__cliente_id=cliente_id)
    
    resultados = []
    for veiculo in veiculos_vendidos:
        despesas_list = veiculo.despesas.all().select_related('tipo', 'fornecedor')
        despesas_total = veiculo.total_despesas()
        lucro = veiculo.lucro_real()
        
        resultados.append({
            'veiculo': veiculo,
            'venda': veiculo.venda,
            'valor_compra': veiculo.valor_compra,
            'valor_venda': veiculo.venda.valor_venda if hasattr(veiculo, 'venda') else Decimal('0.00'),
            'despesas': despesas_total,
            'despesas_list': despesas_list,
            'lucro': lucro,
            'tem_entrada': veiculo.venda.veiculo_entrada is not None if hasattr(veiculo, 'venda') else False,
        })
    
    # Listas para os filtros
    todos_veiculos_vendidos = Veiculo.objects.filter(status='vendido').order_by('marca', 'modelo')
    todos_clientes = Cliente.objects.all().order_by('nome')
    
    context = {
        'resultados': resultados,
        'todos_veiculos': todos_veiculos_vendidos,
        'todos_clientes': todos_clientes,
        'data_inicio': data_inicio,
        'data_fim': data_fim,
        'veiculo_selecionado': veiculo_id,
        'cliente_selecionado': cliente_id,
    }
    return render(request, 'veiculos/relatorio_por_veiculo.html', context)


# ============= CONFIGURAÇÕES =============

def tipo_despesa_lista(request):
    """Lista tipos de despesa"""
    tipos = TipoDespesa.objects.all().order_by('nome')
    context = {'tipos': tipos}
    return render(request, 'veiculos/tipo_despesa_lista.html', context)


def tipo_despesa_novo(request):
    """Criar novo tipo de despesa"""
    if request.method == 'POST':
        form = TipoDespesaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tipo de despesa cadastrado com sucesso!')
            return redirect('tipo_despesa_lista')
    else:
        form = TipoDespesaForm()
    
    context = {'form': form, 'titulo': 'Novo Tipo de Despesa'}
    return render(request, 'veiculos/tipo_despesa_form.html', context)


def forma_pagamento_lista(request):
    """Lista formas de pagamento"""
    formas = FormaPagamento.objects.all().order_by('nome')
    context = {'formas': formas}
    return render(request, 'veiculos/forma_pagamento_lista.html', context)


def forma_pagamento_nova(request):
    """Criar nova forma de pagamento"""
    if request.method == 'POST':
        form = FormaPagamentoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Forma de pagamento cadastrada com sucesso!')
            return redirect('forma_pagamento_lista')
    else:
        form = FormaPagamentoForm()
    
    context = {'form': form, 'titulo': 'Nova Forma de Pagamento'}
    return render(request, 'veiculos/forma_pagamento_form.html', context)
