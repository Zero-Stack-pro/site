# Generated by Django 4.2.10 on 2025-06-13 17:56

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Название')),
                ('slug', models.SlugField(max_length=200, unique=True, verbose_name='URL')),
                ('description', models.TextField(verbose_name='Описание')),
                ('features', models.JSONField(verbose_name='Возможности')),
                ('specifications', models.JSONField(verbose_name='Технические характеристики')),
                ('use_cases', models.JSONField(verbose_name='Применение')),
                ('benefits', models.JSONField(verbose_name='Преимущества')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Дата обновления')),
            ],
            options={
                'verbose_name': 'Продукт',
                'verbose_name_plural': 'Продукты',
                'ordering': ['-created_at'],
            },
        ),
    ]
