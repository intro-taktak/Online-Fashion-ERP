# Generated by Django 2.2.4 on 2021-03-12 04:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('erp', '0003_registeredprogramscheckins_tag'),
    ]

    operations = [
        migrations.CreateModel(
            name='devNotice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=300)),
                ('content', models.TextField()),
                ('writer', models.CharField(max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='devNoticeCheckIns',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('p_id', models.CharField(max_length=300)),
                ('title', models.CharField(max_length=300)),
                ('writer', models.CharField(max_length=100)),
                ('content', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('tag', models.CharField(max_length=100)),
            ],
        ),
    ]
