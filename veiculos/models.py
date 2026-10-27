from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal


# ============= CHOICES GLOBAIS =============

ESTADO_CIVIL_CHOICES = [
    ('', '-- Selecione --'),
    ('solteiro', 'Solteiro(a)'),
    ('casado', 'Casado(a)'),
    ('divorciado', 'Divorciado(a)'),
    ('viuvo', 'Viúvo(a)'),
    ('uniao_estavel', 'União Estável'),
]

UF_CHOICES = [
    ('', '-- UF --'),
    ('AC', 'AC'), ('AL', 'AL'), ('AP', 'AP'), ('AM', 'AM'),
    ('BA', 'BA'), ('CE', 'CE'), ('DF', 'DF'), ('ES', 'ES'),
    ('GO', 'GO'), ('MA', 'MA'), ('MT', 'MT'), ('MS', 'MS'),
    ('MG', 'MG'), ('PA', 'PA'), ('PB', 'PB'), ('PR', 'PR'),
    ('PE', 'PE'), ('PI', 'PI'), ('RJ', 'RJ'), ('RN', 'RN'),
    ('RS', 'RS'), ('RO', 'RO'), ('RR', 'RR'), ('SC', 'SC'),
    ('SP', 'SP'), ('SE', 'SE'), ('TO', 'TO'),
]

COMBUSTIVEL_CHOICES = [
    ('', '-- Selecione --'),
    ('flex', 'Flex'),
    ('gasolina', 'Gasolina'),
    ('alcool', 'Álcool'),
    ('diesel', 'Diesel'),
    ('gnv', 'GNV'),
    ('eletrico', 'Elétrico'),
    ('hibrido', 'Híbrido'),
]

CAMBIO_CHOICES = [
    ('', '-- Selecione --'),
    ('manual', 'Manual'),
    ('automatico', 'Automático'),
    ('cvt', 'CVT'),
    ('automatizado', 'Automatizado'),
]

CATEGORIA_CHOICES = [
    ('', '-- Selecione --'),
    ('hatch', 'Hatch'),
    ('sedan', 'Sedan'),
    ('suv', 'SUV'),
    ('pickup', 'Pickup'),
    ('van', 'Van / Kombi'),
    ('minivan', 'Minivan'),
    ('esportivo', 'Esportivo'),
    ('conversivel', 'Conversível'),
    ('caminhao', 'Caminhão'),
    ('moto', 'Moto'),
    ('outro', 'Outro'),
]


class Fornecedor(models.Model):
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
    # Dados pessoais
    nome = models.CharField(max_length=200, verbose_name='Nome Completo')
    cpf = models.CharField(max_length=14, blank=True, verbose_name='CPF')
    rg = models.CharField(max_length=20, blank=True, verbose_name='RG')
    data_nascimento = models.DateField(null=True, blank=True, verbose_name='Data de Nascimento')
    estado_civil = models.CharField(
        max_length=20, choices=ESTADO_CIVIL_CHOICES, blank=True, verbose_name='Estado Civil'
    )
    profissao = models.CharField(max_length=100, blank=True, verbose_name='Profissão')

    # Documentos
    cnh = models.CharField(max_length=15, blank=True, verbose_name='CNH')

    # Contato
    telefone = models.CharField(max_length=20, blank=True, verbose_name='Telefone')
    email = models.EmailField(blank=True, verbose_name='E-mail')

    # Endereço
    cep = models.CharField(max_length=9, blank=True, verbose_name='CEP')
    cidade = models.CharField(max_length=100, blank=True, verbose_name='Cidade')
    estado_uf = models.CharField(max_length=2, choices=UF_CHOICES, blank=True, verbose_name='Estado (UF)')
    endereco = models.TextField(blank=True, verbose_name='Endereço Completo')

    # Extras
    observacoes = models.TextField(blank=True, verbose_name='Observações')
    data_cadastro = models.DateTimeField(auto_now_add=True, verbose_name='Data de Cadastro')

    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
        ordering = ['nome']

    def __str__(self):
        return self.nome


class Veiculo(models.Model):
    STATUS_CHOICES = [
        ('disponivel', 'Disponível'),
        ('vendido', 'Vendido'),
        ('manutencao', 'Em Manutenção'),
        ('devolvido', 'Devolvido (estorno)'),
    ]

    # Identificação
    marca = models.CharField(max_length=100, verbose_name='Marca')
    modelo = models.CharField(max_length=100, verbose_name='Modelo')
    ano = models.IntegerField(verbose_name='Ano')
    placa = models.CharField(max_length=10, null=True, blank=True, verbose_name='Placa')
    cor = models.CharField(max_length=50, blank=True, verbose_name='Cor')
    categoria = models.CharField(
        max_length=30, choices=CATEGORIA_CHOICES, blank=True, verbose_name='Categoria'
    )

    # Especificações técnicas
    combustivel = models.CharField(
        max_length=20, choices=COMBUSTIVEL_CHOICES, blank=True, verbose_name='Combustível'
    )
    cambio = models.CharField(
        max_length=20, choices=CAMBIO_CHOICES, blank=True, verbose_name='Câmbio'
    )
    portas = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name='Nº de Portas')
    motor = models.CharField(max_length=50, blank=True, verbose_name='Motor')
    km = models.IntegerField(verbose_name='Quilometragem', validators=[MinValueValidator(0)])
    cor_interior = models.CharField(max_length=50, blank=True, verbose_name='Cor Interior')

    # Documentação
    renavam = models.CharField(
        max_length=11, blank=True, verbose_name='RENAVAM',
        help_text='Número do RENAVAM (11 dígitos)'
    )
    chassi = models.CharField(max_length=17, blank=True, verbose_name='Chassi')
    numero_proprietarios = models.PositiveSmallIntegerField(
        null=True, blank=True, default=1, verbose_name='Nº de Proprietários Anteriores'
    )

    # Financeiro
    valor_compra = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name='Valor de Compra',
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    valor_venda = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name='Valor de Venda',
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    fipe = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True, verbose_name='Valor FIPE'
    )

    fornecedor = models.ForeignKey(
        Fornecedor, on_delete=models.SET_NULL, null=True, blank=True,
        verbose_name='Fornecedor / Procedência'
    )

    # Status
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='disponivel', verbose_name='Status'
    )
    data_compra = models.DateField(verbose_name='Data de Compra')
    observacoes = models.TextField(blank=True, verbose_name='Observações')
    data_cadastro = models.DateTimeField(auto_now_add=True, verbose_name='Data de Cadastro')

    class Meta:
        verbose_name = 'Veículo'
        verbose_name_plural = 'Veículos'
        ordering = ['-data_cadastro']
        constraints = [
            # Um veículo vendido pode ser recomprado (novo registro com a mesma placa)
            models.UniqueConstraint(
                fields=['placa'], condition=~models.Q(status__in=['vendido', 'devolvido']),
                name='placa_unica_em_estoque',
                violation_error_message='Já existe um veículo em estoque com esta placa.',
            ),
        ]

    def __str__(self):
        placa = f" ({self.placa})" if self.placa else ""
        return f"{self.marca} {self.modelo} - {self.ano}{placa}"

    def total_despesas(self):
        return self.despesas.aggregate(
            total=models.Sum('valor')
        )['total'] or Decimal('0.00')

    def lucro_previsto(self):
        return self.valor_venda - self.valor_compra - self.total_despesas()

    @property
    def venda(self):
        """Venda ativa (não estornada) do veículo, se estiver vendido."""
        if self.status != 'vendido':
            return None
        return self.vendas.filter(estornada=False).order_by('-data_venda', '-pk').first()

    def lucro_real(self):
        venda = self.venda
        if venda:
            return venda.valor_venda - self.valor_compra - self.total_despesas()
        return None

    def imagem_principal(self):
        img = self.imagens.filter(principal=True).first()
        if not img:
            img = self.imagens.first()
        return img


class TipoDespesa(models.Model):
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
    veiculo = models.ForeignKey(
        Veiculo, on_delete=models.CASCADE, related_name='despesas', verbose_name='Veículo'
    )
    tipo = models.ForeignKey(
        TipoDespesa, on_delete=models.PROTECT, verbose_name='Tipo de Despesa'
    )
    fornecedor = models.ForeignKey(
        Fornecedor, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Fornecedor'
    )
    valor = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name='Valor',
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
    nome = models.CharField(max_length=100, unique=True, verbose_name='Nome')
    ativo = models.BooleanField(default=True, verbose_name='Ativo')

    class Meta:
        verbose_name = 'Forma de Pagamento'
        verbose_name_plural = 'Formas de Pagamento'
        ordering = ['nome']

    def __str__(self):
        return self.nome


class Venda(models.Model):
    veiculo = models.ForeignKey(
        Veiculo, on_delete=models.PROTECT, related_name='vendas', verbose_name='Veículo Vendido'
    )
    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT, verbose_name='Cliente')
    valor_venda = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name='Valor de Venda',
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    veiculo_entrada = models.ForeignKey(
        Veiculo, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='usado_como_entrada', verbose_name='Veículo dado como Entrada'
    )
    valor_entrada = models.DecimalField(
        max_digits=10, decimal_places=2, default=Decimal('0.00'),
        verbose_name='Valor do Veículo de Entrada',
        validators=[MinValueValidator(Decimal('0.00'))]
    )
    forma_pagamento = models.ForeignKey(
        FormaPagamento, on_delete=models.SET_NULL, null=True, blank=True,
        verbose_name='Forma de Pagamento'
    )
    observacoes = models.TextField(blank=True, verbose_name='Observações')
    data_venda = models.DateField(verbose_name='Data da Venda')
    data_cadastro = models.DateTimeField(auto_now_add=True, verbose_name='Data de Cadastro')

    # Estorno
    estornada = models.BooleanField(default=False, verbose_name='Estornada')
    data_estorno = models.DateTimeField(null=True, blank=True, verbose_name='Data do Estorno')
    motivo_estorno = models.TextField(blank=True, verbose_name='Motivo do Estorno')

    class Meta:
        verbose_name = 'Venda'
        verbose_name_plural = 'Vendas'
        ordering = ['-data_venda']

    def __str__(self):
        return f"Venda {self.veiculo} para {self.cliente}"

    @property
    def valor_final(self):
        return self.valor_venda - self.valor_entrada

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.estornada and self.veiculo.status != 'vendido':
            self.veiculo.status = 'vendido'
            self.veiculo.save(update_fields=['status'])

    def todos_veiculos_entrada(self):
        """Veículos recebidos na troca (inclui o campo legado veiculo_entrada)."""
        veiculos = [ve.veiculo for ve in self.veiculos_entrada.select_related('veiculo')]
        if self.veiculo_entrada and self.veiculo_entrada not in veiculos:
            veiculos.append(self.veiculo_entrada)
        return veiculos


class VendaPagamento(models.Model):
    venda = models.ForeignKey(
        Venda, on_delete=models.CASCADE, related_name='pagamentos', verbose_name='Venda'
    )
    forma_pagamento = models.ForeignKey(
        FormaPagamento, on_delete=models.PROTECT, verbose_name='Forma de Pagamento'
    )
    valor = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='Valor (R$)')
    observacao = models.CharField(max_length=200, blank=True, verbose_name='Observação')

    class Meta:
        verbose_name = 'Pagamento da Venda'
        verbose_name_plural = 'Pagamentos da Venda'
        ordering = ['id']

    def __str__(self):
        return f"{self.forma_pagamento} — R$ {self.valor}"


class VendaVeiculoEntrada(models.Model):
    venda = models.ForeignKey(
        Venda, on_delete=models.CASCADE, related_name='veiculos_entrada', verbose_name='Venda'
    )
    veiculo = models.ForeignKey(
        Veiculo, on_delete=models.PROTECT, related_name='entradas', verbose_name='Veículo'
    )
    valor = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='Valor de Avaliação (R$)')

    class Meta:
        verbose_name = 'Veículo de Entrada'
        verbose_name_plural = 'Veículos de Entrada'

    def __str__(self):
        return f"{self.veiculo} — R$ {self.valor}"


class VeiculoImagem(models.Model):
    veiculo = models.ForeignKey(
        Veiculo, on_delete=models.CASCADE, related_name='imagens', verbose_name='Veículo'
    )
    imagem = models.ImageField(upload_to='veiculos/%Y/%m/', verbose_name='Imagem')
    descricao = models.CharField(max_length=200, blank=True, verbose_name='Descrição')
    principal = models.BooleanField(default=False, verbose_name='Imagem Principal')
    ordem = models.IntegerField(default=0, verbose_name='Ordem de Exibição')
    data_upload = models.DateTimeField(auto_now_add=True, verbose_name='Data do Upload')

    class Meta:
        verbose_name = 'Imagem do Veículo'
        verbose_name_plural = 'Imagens dos Veículos'
        ordering = ['-principal', 'ordem', '-data_upload']

    def __str__(self):
        return f"Imagem de {self.veiculo} - {self.descricao or 'Sem descrição'}"

    def save(self, *args, **kwargs):
        if self.principal:
            VeiculoImagem.objects.filter(
                veiculo=self.veiculo, principal=True
            ).update(principal=False)
        super().save(*args, **kwargs)
