# Generated by Django 2.0.7 on 2019-11-10 03:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('blog', '0002_auto_20191109_2249'),
    ]

    operations = [
        migrations.CreateModel(
            name='SeoBlog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('keyword', models.CharField(max_length=450)),
                ('title', models.CharField(blank=True, max_length=450, null=True)),
                ('description', models.TextField(blank=True, max_length=650, null=True)),
                ('published_time', models.DateTimeField(auto_now=True)),
                ('modified_time', models.DateTimeField(auto_now=True)),
                ('blog', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='blog.Blog')),
            ],
        ),
    ]