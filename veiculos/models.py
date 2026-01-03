from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal


class Fornecedor(models.Model):
    """Fornecedor de serviços/peças para os veículos"""
    nome = models.CharField(max_length=200, verbose_name='Nome')
    cnpj_cpf = models.CharField(max_length=18, blank=True, verbose_name='CNPJ/CPF')
    telefone = models.CharField(max_length=20, blank=True, verbose_name='Telefone')
    email = models.EmailField(blank=True, verbose_name='E-mail')
    endereco = models.TextField(blank=True, verbose_name='Endereço')
    ativo = models.BooleanField(default=True, verbose_name='Ativo')
    data_cadastro = models.DateTimeField(auto_now_add=True, verbose_name='Data de Cadastro')

    class Meta:
        verbose_name = 'Fornecedor'
        verbose_name_plural = 'Fornecedores'
        ordering = ['nome']

    def __str__(self):
        return self.nome


class Cliente(models.Model):
    """Cliente que compra veículos"""
    nome = models.CharField(max_length=200, verbose_name='Nome')
    cpf = models.CharField(max_length=14, blank=True, verbose_name='CPF')
    telefone = models.CharField(max_length=20, verbose_name='Telefone')
    email = models.EmailField(blank=True, verbose_name='E-mail')
    endereco = models.TextField(blank=True, verbose_name='Endereço')
    data_cadastro = models.DateTimeField(auto_now_add=True, verbose_name='Data de Cadastro')

    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
        ordering = ['nome']

    def __str__(self):
        return self.nome


class Veiculo(models.Model):
    """Veículo para compra/venda"""
    STATUS_CHOICES = [
        ('disponivel', 'Disponível'),
        ('vendido', 'Vendido'),
        ('manutencao', 'Em Manutenção'),
    ]

    marca = models.CharField(max_length=100, verbose_name='Marca')
    modelo = models.CharField(max_length=100, verbose_name='Modelo')
    ano = models.IntegerField(verbose_name='Ano')
    placa = models.CharField(max_length=10, unique=True, verbose_name='Placa')
    renavam = models.CharField(max_length=11, blank=True, verbose_name='RENAVAM', help_text='Número do RENAVAM (11 dígitos)')
    cor = models.CharField(max_length=50, blank=True, verbose_name='Cor')
    km = models.IntegerField(verbose_name='Quilometragem', validators=[MinValueValidator(0)])
    chassi = models.CharField(max_length=17, blank=True, verbose_name='Chassi')
    
    valor_compra = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        verbose_name='Valor de Compra',
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    valor_venda = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        verbose_name='Valor de Venda',
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    
    fornecedor = models.ForeignKey(
        Fornecedor, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        verbose_name='Fornecedor/Vendedor'
    )
    
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='disponivel',
        verbose_name='Status'
    )
    
    observacoes = models.TextField(blank=True, verbose_name='Observações')
    data_compra = models.DateField(verbose_name='Data de Compra')
    data_cadastro = models.DateTimeField(auto_now_add=True, verbose_name='Data de Cadastro')

    class Meta:
        verbose_name = 'Veículo'
        verbose_name_plural = 'Veículos'
        ordering = ['-data_cadastro']

    def __str__(self):
        return f"{self.marca} {self.modelo} - {self.ano} ({self.placa})"

    def total_despesas(self):
        """Calcula o total de despesas do veículo"""
        return self.despesas.aggregate(
            total=models.Sum('valor')
        )['total'] or Decimal('0.00')

    def lucro_previsto(self):
        """Calcula o lucro previsto (venda - compra - despesas)"""
        return self.valor_venda - self.valor_compra - self.total_despesas()

    def lucro_real(self):
        """Calcula o lucro real se o veículo foi vendido"""
        if self.status == 'vendido':
            try:
                venda = self.venda
                # Lucro = Valor de venda - Valor de compra - Despesas
                # O valor de entrada (troca) NÃO entra no cálculo
                return venda.valor_venda - self.valor_compra - self.total_despesas()
            except:
                return Decimal('0.00')
        return None

    def imagem_principal(self):
        """Retorna a imagem principal ou a primeira imagem"""
        img = self.imagens.filter(principal=True).first()
        if not img:
            img = self.imagens.first()
        return img


class TipoDespesa(models.Model):
    """Tipos de despesas (mecânica, funilaria, impostos, etc)"""
    nome = models.CharField(max_length=100, unique=True, verbose_name='Nome')
    descricao = models.TextField(blank=True, verbose_name='Descrição')
    ativo = models.BooleanField(default=True, verbose_name='Ativo')

    class Meta:
        verbose_name = 'Tipo de Despesa'
        verbose_name_plural = 'Tipos de Despesas'
        ordering = ['nome']

    def __str__(self):
        return self.nome


class Despesa(models.Model):
    """Despesas relacionadas a um veículo"""
    veiculo = models.ForeignKey(
        Veiculo, 
        on_delete=models.CASCADE, 
        related_name='despesas',
        verbose_name='Veículo'
    )
    tipo = models.ForeignKey(
        TipoDespesa, 
        on_delete=models.PROTECT,
        verbose_name='Tipo de Despesa'
    )
    fornecedor = models.ForeignKey(
        Fornecedor, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        verbose_name='Fornecedor'
    )
    valor = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        verbose_name='Valor',
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    descricao = models.TextField(verbose_name='Descrição')
    data_despesa = models.DateField(verbose_name='Data da Despesa')
    data_cadastro = models.DateTimeField(auto_now_add=True, verbose_name='Data de Cadastro')

    class Meta:
        verbose_name = 'Despesa'
        verbose_name_plural = 'Despesas'
        ordering = ['-data_despesa']

    def __str__(self):
        return f"{self.tipo.nome} - R$ {self.valor} ({self.veiculo})"


class FormaPagamento(models.Model):
    """Formas de pagamento aceitas"""
    nome = models.CharField(max_length=100, unique=True, verbose_name='Nome')
    ativo = models.BooleanField(default=True, verbose_name='Ativo')

    class Meta:
        verbose_name = 'Forma de Pagamento'
        verbose_name_plural = 'Formas de Pagamento'
        ordering = ['nome']

    def __str__(self):
        return self.nome


class Venda(models.Model):
    """Venda de um veículo"""
    veiculo = models.OneToOneField(
        Veiculo, 
        on_delete=models.PROTECT, 
        related_name='venda',
        verbose_name='Veículo Vendido'
    )
    cliente = models.ForeignKey(
        Cliente, 
        on_delete=models.PROTECT,
        verbose_name='Cliente'
    )
    
    valor_venda = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        verbose_name='Valor de Venda',
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    
    # Veículo recebido como parte do pagamento (troca)
    veiculo_entrada = models.ForeignKey(
        Veiculo,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='usado_como_entrada',
        verbose_name='Veículo dado como Entrada'
    )
    valor_entrada = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal('0.00'),
        verbose_name='Valor do Veículo de Entrada',
        validators=[MinValueValidator(Decimal('0.00'))]
    )
    
    forma_pagamento = models.ForeignKey(
        FormaPagamento,
        on_delete=models.PROTECT,
        verbose_name='Forma de Pagamento'
    )
    
    observacoes = models.TextField(blank=True, verbose_name='Observações')
    data_venda = models.DateField(verbose_name='Data da Venda')
    data_cadastro = models.DateTimeField(auto_now_add=True, verbose_name='Data de Cadastro')

    class Meta:
        verbose_name = 'Venda'
        verbose_name_plural = 'Vendas'
        ordering = ['-data_venda']

    def __str__(self):
        return f"Venda {self.veiculo} para {self.cliente}"

    @property
    def valor_final(self):
        """Valor final (venda - entrada)"""
        return self.valor_venda - self.valor_entrada

    def save(self, *args, **kwargs):
        """Ao salvar, marca o veículo como vendido"""
        super().save(*args, **kwargs)
        self.veiculo.status = 'vendido'
        self.veiculo.save()


class VeiculoImagem(models.Model):
    """Imagens de um veículo"""
    veiculo = models.ForeignKey(
        Veiculo, 
        on_delete=models.CASCADE, 
        related_name='imagens',
        verbose_name='Veículo'
    )
    imagem = models.ImageField(
        upload_to='veiculos/%Y/%m/',
        verbose_name='Imagem'
    )
    descricao = models.CharField(
        max_length=200, 
        blank=True, 
        verbose_name='Descrição'
    )
    principal = models.BooleanField(
        default=False, 
        verbose_name='Imagem Principal'
    )
    ordem = models.IntegerField(
        default=0, 
        verbose_name='Ordem de Exibição'
    )
    data_upload = models.DateTimeField(
        auto_now_add=True, 
        verbose_name='Data do Upload'
    )

    class Meta:
        verbose_name = 'Imagem do Veículo'
        verbose_name_plural = 'Imagens dos Veículos'
        ordering = ['-principal', 'ordem', '-data_upload']

    def __str__(self):
        return f"Imagem de {self.veiculo} - {self.descricao or 'Sem descrição'}"

    def save(self, *args, **kwargs):
        """Se marcada como principal, desmarca as outras"""
        if self.principal:
            VeiculoImagem.objects.filter(
                veiculo=self.veiculo, 
                principal=True
            ).update(principal=False)
        super().save(*args, **kwargs)
