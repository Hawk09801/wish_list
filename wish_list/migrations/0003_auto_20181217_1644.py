# Generated by Django 2.1.3 on 2018-12-17 16:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wish_list', '0002_auto_20181217_1642'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gifts',
            name='file',
            field=models.FileField(null=True, upload_to='', verbose_name='Dodaj zdjęcie'),
        ),
        migrations.AlterField(
            model_name='gifts',
            name='shop',
            field=models.CharField(max_length=250, null=True, verbose_name='Gdzie można to dostać?'),
        ),
    ]