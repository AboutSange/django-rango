# Generated by Django 2.0.8 on 2018-08-16 11:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rango', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name_plural': 'Categories'},
        ),
        migrations.RenameField(
            model_name='page',
            old_name='catagory',
            new_name='category',
        ),
    ]
