# Generated by Django 5.1.3 on 2024-11-23 18:08

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Calibri',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
                ('RR', models.CharField(max_length=255, verbose_name='RR')),
                ('stress_num', models.CharField(max_length=255, verbose_name='Stress Number')),
                ('stress_level', models.CharField(max_length=255, verbose_name='Stress Level')),
            ],
        ),
    ]
