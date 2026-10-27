from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('veiculos', '0003_alter_cliente_telefone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='venda',
            name='forma_pagamento',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to='veiculos.formapagamento',
                verbose_name='Forma de Pagamento',
            ),
        ),
        migrations.CreateModel(
            name='VendaPagamento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('valor', models.DecimalField(decimal_places=2, max_digits=12, verbose_name='Valor (R$)')),
                ('observacao', models.CharField(blank=True, max_length=200, verbose_name='Observação')),
                ('forma_pagamento', models.ForeignKey(
                    on_delete=django.db.models.deletion.PROTECT,
                    to='veiculos.formapagamento',
                    verbose_name='Forma de Pagamento',
                )),
                ('venda', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='pagamentos',
                    to='veiculos.venda',
                    verbose_name='Venda',
                )),
            ],
            options={
                'verbose_name': 'Pagamento da Venda',
                'verbose_name_plural': 'Pagamentos da Venda',
                'ordering': ['id'],
            },
        ),
    ]
