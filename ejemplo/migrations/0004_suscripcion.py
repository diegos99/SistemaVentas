# Generated by Django 3.0.3 on 2020-03-16 20:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ejemplo', '0003_delete_cliente'),
    ]

    operations = [
        migrations.CreateModel(
            name='suscripcion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('estado', models.CharField(max_length=40)),
                ('fecha_expiracion', models.DateField()),
                ('fecha_creacion', models.DateField()),
            ],
        ),
    ]
