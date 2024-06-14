# Generated by Django 4.2 on 2024-06-13 17:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
            ],
            options={
                'verbose_name': 'city',
                'verbose_name_plural': 'cities',
                'db_table': 'city',
            },
        ),
        migrations.CreateModel(
            name='Province',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
            ],
            options={
                'verbose_name': 'province',
                'verbose_name_plural': 'provinces',
                'db_table': 'province',
            },
        ),
        migrations.CreateModel(
            name='Site',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='city.city')),
            ],
            options={
                'verbose_name': 'site',
                'verbose_name_plural': 'sites',
                'db_table': 'site',
            },
        ),
        migrations.CreateModel(
            name='RawData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day', models.DateTimeField()),
                ('kpi_1', models.FloatField()),
                ('kpi_2', models.FloatField()),
                ('kpi_3', models.FloatField()),
                ('kpi_4', models.FloatField()),
                ('kpi_5', models.FloatField()),
                ('kpi_6', models.FloatField()),
                ('kpi_7', models.FloatField()),
                ('kpi_8', models.FloatField()),
                ('kpi_9', models.FloatField()),
                ('kpi_10', models.FloatField()),
                ('kpi_11', models.FloatField()),
                ('kpi_12', models.FloatField()),
                ('kpi_13', models.FloatField()),
                ('kpi_14', models.FloatField()),
                ('kpi_15', models.FloatField()),
                ('kpi_16', models.FloatField()),
                ('kpi_17', models.FloatField()),
                ('kpi_18', models.FloatField()),
                ('kpi_19', models.FloatField()),
                ('kpi_20', models.FloatField()),
                ('site', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='city.site')),
            ],
            options={
                'verbose_name': 'raw',
                'verbose_name_plural': 'raws',
                'db_table': 'raw',
            },
        ),
        migrations.AddField(
            model_name='city',
            name='province',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='city.province'),
        ),
        migrations.CreateModel(
            name='AggregateModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('kpi', models.CharField(max_length=8)),
                ('value', models.FloatField()),
                ('method', models.PositiveSmallIntegerField(choices=[(1, 'SUM'), (2, 'AVG'), (3, 'MIN'), (4, 'MAX')])),
                ('city', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='city.city')),
                ('province', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='city.province')),
                ('site', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='city.site')),
            ],
            options={
                'verbose_name': 'Aggregate Model',
                'verbose_name_plural': 'Aggregate Models',
                'db_table': 'aggregate_model',
            },
        ),
    ]