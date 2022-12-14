# Generated by Django 3.2.13 on 2022-11-17 02:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cheers', '0011_alter_comment_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('price', models.IntegerField()),
                ('ml', models.CharField(max_length=10)),
                ('country', models.CharField(max_length=10)),
                ('image_path', models.CharField(max_length=255)),
                ('content', models.TextField()),
            ],
        ),
    ]
