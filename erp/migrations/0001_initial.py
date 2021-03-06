# Generated by Django 2.2.4 on 2021-03-08 07:36

from django.db import migrations, models
import erp.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Files',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('board', models.CharField(max_length=300)),
                ('p_id', models.CharField(max_length=300)),
                ('file', models.FileField(upload_to=erp.models.upload_to)),
            ],
        ),
        migrations.CreateModel(
            name='Menus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('m_id', models.CharField(max_length=300)),
                ('parent', models.CharField(max_length=500)),
                ('menu_name', models.CharField(max_length=400)),
                ('parent_url', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='RegisteredPrograms',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=300)),
                ('category', models.CharField(max_length=400)),
                ('progress', models.CharField(max_length=100)),
                ('rating', models.CharField(max_length=50)),
                ('url', models.CharField(max_length=100)),
                ('content', models.TextField()),
                ('manual', models.TextField()),
                ('writer', models.CharField(max_length=100)),
                ('parent_id', models.CharField(max_length=100)),
                ('order', models.IntegerField(default=1)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='RegisteredProgramsCheckIns',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('p_id', models.CharField(max_length=300)),
                ('title', models.CharField(max_length=300)),
                ('writer', models.CharField(max_length=100)),
                ('content', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
