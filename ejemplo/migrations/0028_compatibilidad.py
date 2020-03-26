# Generated by Django 3.0.3 on 2020-03-24 23:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ejemplo', '0027_vehiculo'),
    ]

    operations = [
        migrations.CreateModel(
            name='compatibilidad',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('repuesto', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='ejemplo.repuesto')),
                ('vehiculo', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='ejemplo.vehiculo')),
            ],
        ),
    ]
