# Generated by Django 3.2.13 on 2022-11-15 05:47

import cheers.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cheers', '0002_user_nickname'),
    ]

    operations = [
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=30)),
                ('content', models.TextField()),
                ('image1', models.ImageField(upload_to='recipe_pics')),
                ('image2', models.ImageField(blank=True, upload_to='recipe_pics')),
                ('image3', models.ImageField(blank=True, upload_to='recipe_pics')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.AlterField(
            model_name='user',
            name='nickname',
            field=models.CharField(error_messages={'unique': '이미 사용중인 닉네임입니다.'}, max_length=10, null=True, unique=True, validators=[cheers.validators.validate_no_special_characters]),
        ),
    ]
