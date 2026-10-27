import json
from datetime import date
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db import transaction, IntegrityError
from django.db.models import Sum, Q, Count
from django.http import JsonResponse
from decimal import Decimal
from .models import (
    Veiculo, VeiculoImagem, Despesa, Cliente, Fornecedor, Venda, VendaPagamento,
    VendaVeiculoEntrada, TipoDespesa, FormaPagamento
)
from .forms import (
    VeiculoForm, DespesaForm, ClienteForm, FornecedorForm,
    VendaForm, VendaPagamentoFormSet, VendaVeiculoEntradaFormSet, VeiculoTrocaForm,
    TipoDespesaForm, FormaPagamentoForm, EstornoVendaForm
)
from django.utils import timezone


# ============= CADASTRO RÁPIDO VIA AJAX =============

def fornecedor_ajax(request):
    """Cadastro rápido de fornecedor via AJAX"""
    if request.method == 'POST':
        form = FornecedorForm(request.POST)
        if form.is_valid():
            fornecedor = form.save()
            return JsonResponse({
                'success': True,
                'id': fornecedor.id,
                'nome': fornecedor.nome
            })
        else:
            return JsonResponse({
                'success': False,
                'errors': form.errors
            })
    return JsonResponse({'success': False})


def cliente_ajax(request):
    """Cadastro rápido de cliente via AJAX"""
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            cliente = form.save()
            return JsonResponse({
                'success': True,
                'id': cliente.id,
                'nome': cliente.nome
            })
        else:
            return JsonResponse({
                'success': False,
                'errors': form.errors
            })
    return JsonResponse({'success': False})


def tipo_despesa_ajax(request):
    """Cadastro rápido de tipo de despesa via AJAX"""
    if request.method == 'POST':
        form = TipoDespesaForm(request.POST)
        if form.is_valid():
            tipo = form.save()
            return JsonResponse({
                'success': True,
                'id': tipo.id,
                'nome': tipo.nome
            })
        else:
            return JsonResponse({
                'success': False,
                'errors': form.errors
            })
    return JsonResponse({'success': False})


def veiculo_ajax(request):
    """Cadastro rápido de veículo de troca via AJAX"""
    if request.method == 'POST':
        form = VeiculoTrocaForm(request.POST)
        if form.is_valid():
            veiculo = form.save(commit=False)
            veiculo.placa = veiculo.placa or None
            veiculo.status = 'disponivel'
            veiculo.km = 0
            veiculo.data_compra = date.today()
            veiculo.valor_venda = veiculo.valor_compra
            veiculo.save()
            return JsonResponse({
                'success': True,
                'id': veiculo.id,
                'nome': str(veiculo),
                'valor': float(veiculo.valor_compra or 0),
            })
        return JsonResponse({'success': False, 'errors': form.errors})
    return JsonResponse({'success': False})


def forma_pagamento_ajax(request):
    """Cadastro rápido de forma de pagamento via AJAX"""
    if request.method == 'POST':
        form = FormaPagamentoForm(request.POST)
        if form.is_valid():
            forma = form.save()
            return JsonResponse({
                'success': True,
                'id': forma.id,
                'nome': forma.nome
            })
        else:
            return JsonResponse({
                'success': False,
                'errors': form.errors
            })
    return JsonResponse({'success': False})


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
    vendas = Venda.objects.filter(estornada=False)

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
        'venda_atual': veiculo.venda,
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


_CAMPOS_RECOMPRA = [
    'marca', 'modelo', 'ano', 'placa', 'cor', 'categoria', 'combustivel', 'cambio',
    'portas', 'motor', 'km', 'cor_interior', 'renavam', 'chassi', 'numero_proprietarios',
    'valor_venda', 'fipe',
]


def veiculo_recomprar(request, pk):
    """Recompra de um veículo já vendido: cria um novo registro preservando o histórico do anterior"""
    original = get_object_or_404(Veiculo, pk=pk)

    if original.status not in ('vendido', 'devolvido'):
        messages.error(request, 'Só é possível recomprar um veículo vendido ou devolvido.')
        return redirect('veiculo_detalhe', pk=original.pk)

    if request.method == 'POST':
        form = VeiculoForm(request.POST, request.FILES)
        if form.is_valid():
            veiculo = form.save()
            for idx, imagem in enumerate(request.FILES.getlist('imagens')):
                VeiculoImagem.objects.create(
                    veiculo=veiculo, imagem=imagem, principal=(idx == 0), ordem=idx
                )
            messages.success(request, 'Veículo recomprado e adicionado ao estoque!')
            return redirect('veiculo_detalhe', pk=veiculo.pk)
    else:
        initial = {campo: getattr(original, campo) for campo in _CAMPOS_RECOMPRA}
        initial.update({
            'status': 'disponivel',
            'data_compra': date.today(),
            'observacoes': f'Recompra do veículo #{original.pk}.',
        })
        form = VeiculoForm(initial=initial)

    context = {'form': form, 'titulo': f'Recompra — {original}'}
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
        pagamentos_fs = VendaPagamentoFormSet(request.POST, prefix='pagamentos')
        veiculos_fs = VendaVeiculoEntradaFormSet(request.POST, prefix='veiculos_entrada')
        if form.is_valid() and pagamentos_fs.is_valid() and veiculos_fs.is_valid():
            try:
                with transaction.atomic():
                    venda = form.save(commit=False)
                    venda.veiculo = veiculo
                    venda.save()
                    pagamentos_fs.instance = venda
                    pagamentos_fs.save()
                    veiculos_fs.instance = venda
                    for ve in veiculos_fs.save():
                        ve.veiculo.status = 'disponivel'
                        ve.veiculo.save()
            except IntegrityError:
                messages.error(request, 'Não foi possível registrar a venda. Tente novamente.')
                return redirect('veiculo_detalhe', pk=veiculo.pk)
            messages.success(request, 'Venda realizada com sucesso!')
            return redirect('venda_detalhe', pk=venda.pk)
    else:
        form = VendaForm(veiculo=veiculo)
        pagamentos_fs = VendaPagamentoFormSet(prefix='pagamentos')
        veiculos_fs = VendaVeiculoEntradaFormSet(prefix='veiculos_entrada')

    # Dados para os selects JS
    formas_list = list(FormaPagamento.objects.filter(ativo=True).values('id', 'nome'))
    veiculos_disponiveis = Veiculo.objects.filter(status='disponivel').exclude(pk=veiculo_pk)
    veiculos_list = [
        {'id': v.id, 'nome': str(v), 'valor': float(v.valor_venda or v.valor_compra or 0)}
        for v in veiculos_disponiveis
    ]
    context = {
        'form': form,
        'veiculo': veiculo,
        'titulo': 'Nova Venda',
        'pagamentos_fs': pagamentos_fs,
        'veiculos_fs': veiculos_fs,
        'formas_json': json.dumps(formas_list),
        'veiculos_json': json.dumps(veiculos_list),
        'custo_base_json': json.dumps(float(veiculo.valor_compra) + float(veiculo.total_despesas())),
    }
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


def venda_estornar(request, pk):
    """Estorna uma venda: o veículo volta ao estoque e os veículos da troca são devolvidos"""
    venda = get_object_or_404(Venda.objects.select_related('veiculo', 'cliente'), pk=pk)

    if venda.estornada:
        messages.error(request, 'Esta venda já foi estornada.')
        return redirect('venda_detalhe', pk=venda.pk)

    veiculos_troca = venda.todos_veiculos_entrada()
    bloqueados = [v for v in veiculos_troca if v.status == 'vendido']

    if request.method == 'POST':
        form = EstornoVendaForm(request.POST)
        if bloqueados:
            messages.error(request, 'Há veículos desta troca que já foram vendidos. Estorne essas vendas primeiro.')
        elif form.is_valid():
            with transaction.atomic():
                venda.estornada = True
                venda.data_estorno = timezone.now()
                venda.motivo_estorno = form.cleaned_data['motivo']
                venda.save()

                veiculo = venda.veiculo
                veiculo.status = 'disponivel'
                veiculo.save(update_fields=['status'])

                # Veículos recebidos na troca voltam para o cliente
                for v in veiculos_troca:
                    v.status = 'devolvido'
                    v.save(update_fields=['status'])
            messages.success(request, 'Venda estornada. O veículo voltou para o estoque.')
            return redirect('venda_detalhe', pk=venda.pk)
    else:
        form = EstornoVendaForm()

    context = {
        'venda': venda,
        'form': form,
        'veiculos_troca': veiculos_troca,
        'bloqueados': bloqueados,
    }
    return render(request, 'veiculos/venda_confirm_estorno.html', context)


# ============= RELATÓRIOS =============

def relatorio_geral(request):
    """Relatório geral de vendas e despesas"""
    vendas = Venda.objects.filter(estornada=False).select_related('veiculo', 'cliente')

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
    vendas = Venda.objects.filter(estornada=False, veiculo__status='vendido').select_related(
        'veiculo', 'cliente', 'veiculo_entrada'
    )

    # Aplicar filtros
    if data_inicio:
        vendas = vendas.filter(data_venda__gte=data_inicio)
    if data_fim:
        vendas = vendas.filter(data_venda__lte=data_fim)
    if veiculo_id:
        vendas = vendas.filter(veiculo_id=veiculo_id)
    if cliente_id:
        vendas = vendas.filter(cliente_id=cliente_id)

    resultados = []
    for venda in vendas:
        veiculo = venda.veiculo
        despesas_list = veiculo.despesas.all().select_related('tipo', 'fornecedor')
        despesas_total = veiculo.total_despesas()

        resultados.append({
            'veiculo': veiculo,
            'venda': venda,
            'valor_compra': veiculo.valor_compra,
            'valor_venda': venda.valor_venda,
            'despesas': despesas_total,
            'despesas_list': despesas_list,
            'lucro': venda.valor_venda - veiculo.valor_compra - despesas_total,
            'tem_entrada': bool(venda.todos_veiculos_entrada()),
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


# ============= RELATÓRIO PDF =============

def relatorio_pdf(request):
    """Relatório de resultados imprimível/PDF com filtros de período"""
    data_inicio = request.GET.get('data_inicio')
    data_fim    = request.GET.get('data_fim')

    vendas = Venda.objects.filter(estornada=False).select_related(
        'veiculo', 'cliente', 'forma_pagamento', 'veiculo_entrada'
    ).order_by('data_venda')

    if data_inicio:
        vendas = vendas.filter(data_venda__gte=data_inicio)
    if data_fim:
        vendas = vendas.filter(data_venda__lte=data_fim)

    resultados = []
    total_compra  = Decimal('0.00')
    total_despesa = Decimal('0.00')
    total_venda   = Decimal('0.00')
    total_lucro   = Decimal('0.00')

    for venda in vendas:
        v         = venda.veiculo
        despesas  = v.total_despesas()
        lucro     = venda.valor_venda - v.valor_compra - despesas

        total_compra  += v.valor_compra
        total_despesa += despesas
        total_venda   += venda.valor_venda
        total_lucro   += lucro

        resultados.append({
            'venda':         venda,
            'veiculo':       v,
            'cliente':       venda.cliente,
            'data_venda':    venda.data_venda,
            'valor_compra':  v.valor_compra,
            'despesas':      despesas,
            'valor_venda':   venda.valor_venda,
            'lucro':         lucro,
        })

    context = {
        'resultados':    resultados,
        'data_inicio':   data_inicio,
        'data_fim':      data_fim,
        'total_compra':  total_compra,
        'total_despesa': total_despesa,
        'total_venda':   total_venda,
        'total_lucro':   total_lucro,
        'qtd_vendas':    len(resultados),
    }
    return render(request, 'veiculos/relatorio_pdf.html', context)


# ============= EXTRATO DE VEÍCULO =============

def veiculo_extrato(request, pk):
    """Extrato imprimível de um veículo (histórico financeiro completo)"""
    veiculo = get_object_or_404(Veiculo, pk=pk)
    despesas = veiculo.despesas.all().select_related('tipo', 'fornecedor').order_by('data_despesa')

    total_despesas = veiculo.total_despesas()
    custo_total = veiculo.valor_compra + total_despesas

    venda = veiculo.venda
    lucro = venda.valor_venda - custo_total if venda else None

    context = {
        'veiculo': veiculo,
        'despesas': despesas,
        'total_despesas': total_despesas,
        'custo_total': custo_total,
        'venda': venda,
        'lucro': lucro,
    }
    return render(request, 'veiculos/veiculo_extrato.html', context)


# ============= CONFIGURAÇÕES =============

def tipo_despesa_lista(request):
    tipos = TipoDespesa.objects.all().order_by('nome')
    return render(request, 'veiculos/tipo_despesa_lista.html', {'tipos': tipos})


def tipo_despesa_novo(request):
    if request.method == 'POST':
        form = TipoDespesaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tipo de despesa cadastrado com sucesso!')
            return redirect('tipo_despesa_lista')
    else:
        form = TipoDespesaForm()
    return render(request, 'veiculos/tipo_despesa_form.html', {'form': form, 'titulo': 'Novo Tipo de Despesa'})


def tipo_despesa_editar(request, pk):
    tipo = get_object_or_404(TipoDespesa, pk=pk)
    if request.method == 'POST':
        form = TipoDespesaForm(request.POST, instance=tipo)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tipo de despesa atualizado com sucesso!')
            return redirect('tipo_despesa_lista')
    else:
        form = TipoDespesaForm(instance=tipo)
    return render(request, 'veiculos/tipo_despesa_form.html', {'form': form, 'titulo': 'Editar Tipo de Despesa'})


def tipo_despesa_deletar(request, pk):
    tipo = get_object_or_404(TipoDespesa, pk=pk)
    if request.method == 'POST':
        try:
            tipo.delete()
            messages.success(request, 'Tipo de despesa excluído com sucesso!')
        except Exception:
            messages.error(request, 'Não é possível excluir: existem despesas vinculadas a este tipo.')
        return redirect('tipo_despesa_lista')
    return render(request, 'veiculos/tipo_despesa_confirm_delete.html', {'tipo': tipo})


def forma_pagamento_lista(request):
    formas = FormaPagamento.objects.all().order_by('nome')
    return render(request, 'veiculos/forma_pagamento_lista.html', {'formas': formas})


def forma_pagamento_nova(request):
    if request.method == 'POST':
        form = FormaPagamentoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Forma de pagamento cadastrada com sucesso!')
            return redirect('forma_pagamento_lista')
    else:
        form = FormaPagamentoForm()
    return render(request, 'veiculos/forma_pagamento_form.html', {'form': form, 'titulo': 'Nova Forma de Pagamento'})


def forma_pagamento_editar(request, pk):
    forma = get_object_or_404(FormaPagamento, pk=pk)
    if request.method == 'POST':
        form = FormaPagamentoForm(request.POST, instance=forma)
        if form.is_valid():
            form.save()
            messages.success(request, 'Forma de pagamento atualizada com sucesso!')
            return redirect('forma_pagamento_lista')
    else:
        form = FormaPagamentoForm(instance=forma)
    return render(request, 'veiculos/forma_pagamento_form.html', {'form': form, 'titulo': 'Editar Forma de Pagamento'})


def forma_pagamento_deletar(request, pk):
    forma = get_object_or_404(FormaPagamento, pk=pk)
    if request.method == 'POST':
        try:
            forma.delete()
            messages.success(request, 'Forma de pagamento excluída com sucesso!')
        except Exception:
            messages.error(request, 'Não é possível excluir: existem pagamentos vinculados a esta forma.')
        return redirect('forma_pagamento_lista')
    return render(request, 'veiculos/forma_pagamento_confirm_delete.html', {'forma': forma})
