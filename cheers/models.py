from django.db import models
from django.contrib.auth.models import AbstractUser
from .validators import validate_no_special_characters
# Create your models here.

class User(AbstractUser):
    nickname = models.CharField(
        max_length=10, 
        unique=True, 
        null=True,
        validators=[validate_no_special_characters],
        error_messages={'unique': '이미 사용중인 닉네임입니다.'},
    )
    
    def __str__(self):
        return self.email


class Recipe(models.Model):
    title = models.CharField(max_length=30)
    content = models.TextField()
    image1 = models.ImageField(upload_to="recipe_pics")
    image2 = models.ImageField(upload_to="recipe_pics", blank=True)
    image3 = models.ImageField(upload_to="recipe_pics", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title