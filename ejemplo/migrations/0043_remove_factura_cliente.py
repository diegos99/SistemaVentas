# Generated by Django 3.0.3 on 2020-04-05 02:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ejemplo', '0042_factura_cliente'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='factura',
            name='cliente',
        ),
    ]
