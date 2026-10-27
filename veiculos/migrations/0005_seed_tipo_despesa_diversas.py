from django.db import migrations


def seed_tipos(apps, schema_editor):
    TipoDespesa = apps.get_model('veiculos', 'TipoDespesa')
    TipoDespesa.objects.get_or_create(nome='Diversas', defaults={'ativo': True})


class Migration(migrations.Migration):

    dependencies = [
        ('veiculos', '0004_vendapagamento_alter_venda_forma_pagamento'),
    ]

    operations = [
        migrations.RunPython(seed_tipos, migrations.RunPython.noop),
    ]
