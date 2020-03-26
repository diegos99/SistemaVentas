# Generated by Django 3.0.3 on 2020-03-24 06:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ejemplo', '0022_delete_repuesto'),
    ]

    operations = [
        migrations.CreateModel(
            name='repuesto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=400)),
                ('descripcion', models.TextField(max_length=400)),
                ('no_parte', models.IntegerField()),
                ('stock', models.PositiveSmallIntegerField()),
                ('precio_fabricante', models.DecimalField(decimal_places=2, default=0.0, max_digits=6)),
                ('precio_venta', models.DecimalField(decimal_places=2, default=0.0, max_digits=6)),
            ],
        ),
    ]
