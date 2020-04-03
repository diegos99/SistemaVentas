# Generated by Django 3.0.3 on 2020-03-28 03:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ejemplo', '0028_compatibilidad'),
    ]

    operations = [
        migrations.CreateModel(
            name='administrador',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('apellido', models.CharField(max_length=100)),
                ('username', models.CharField(max_length=100)),
                ('telefono', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='tipopago',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pago', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='vendedor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('apellido', models.CharField(max_length=100)),
                ('username', models.CharField(max_length=100)),
                ('telefono', models.IntegerField()),
                ('administrador', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='ejemplo.administrador')),
            ],
        ),
    ]
