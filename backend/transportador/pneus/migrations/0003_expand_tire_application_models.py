import decimal

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('pneus', '0002_application_empresa_application_filial_and_more'),
        ('frota', '0005_historicokm_empresa_historicokm_filial_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='tire',
            name='data_compra',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='tire',
            name='proxima_inspecao',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='tire',
            name='profundidade_sulco_minimo',
            field=models.DecimalField(blank=True, decimal_places=2, help_text='Profundidade mínima aceitável do sulco (mm)', max_digits=4, null=True),
        ),
        migrations.AddField(
            model_name='tire',
            name='profundidade_sulco_novo',
            field=models.DecimalField(blank=True, decimal_places=2, help_text='Profundidade do sulco quando novo (mm)', max_digits=4, null=True),
        ),
        migrations.AddField(
            model_name='tire',
            name='ultima_inspecao',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='application',
            name='criado_em',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='application',
            name='data_desmontagem',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='application',
            name='data_montagem',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='application',
            name='km_desmontagem',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='application',
            name='km_montagem',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='application',
            name='observacoes',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='application',
            name='pneu',
            field=models.ForeignKey(blank=True, null=True, on_delete=models.CASCADE, related_name='aplicacoes', to='pneus.tire'),
        ),
        migrations.AddField(
            model_name='application',
            name='posicao',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AddField(
            model_name='application',
            name='veiculo',
            field=models.ForeignKey(blank=True, null=True, on_delete=models.SET_NULL, related_name='aplicacoes_pneu', to='frota.vehicle'),
        ),
        migrations.AlterField(
            model_name='application',
            name='medida',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AlterField(
            model_name='medicaopneu',
            name='sulco_central',
            field=models.DecimalField(blank=True, decimal_places=2, help_text='Sulco central em mm', max_digits=4, null=True),
        ),
        migrations.AlterField(
            model_name='medicaopneu',
            name='sulco_externo',
            field=models.DecimalField(blank=True, decimal_places=2, help_text='Sulco externo em mm', max_digits=4, null=True),
        ),
        migrations.AlterField(
            model_name='medicaopneu',
            name='sulco_interno',
            field=models.DecimalField(blank=True, decimal_places=2, help_text='Sulco interno em mm', max_digits=4, null=True),
        ),
        migrations.AddField(
            model_name='medicaopneu',
            name='sulco',
            field=models.DecimalField(decimal_places=2, default=decimal.Decimal('0.0'), help_text='Sulco médio em mm', max_digits=4),
            preserve_default=False,
        ),
    ]
