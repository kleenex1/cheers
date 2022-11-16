from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from .validators import validate_no_special_characters
# Create your models here.

class User(AbstractUser):
    nickname = models.CharField(
        max_length=10, 
        unique=True, 
        null=True,
        validators=[validate_no_special_characters],
        error_messages={"unique": "이미 사용중인 닉네임입니다."},
    )
    
    profile_pic = models.ImageField(default="default_profile.png", upload_to="profile_pics")
    introduce = models.CharField(max_length=80, blank=True)

    following = models.ManyToManyField("self", symmetrical=False, blank=True, related_name="followers")
    
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

    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="recipes")
    
    # GenericFoeingKey는 related_name을 설정할 수 없어서 GenericRelation을 불러와서 쓴다.
    # Recipe.likes 로 접근가능
    likes = GenericRelation('Like')

    def __str__(self):
        return self.title

    # 이 Meta 옵션을 사용하면 view에서 모든 정렬 로직을 생략해도 된다.
    # view에서 다시 정렬 로직을 추가하면 덮어써짐.
    # 추가 후 마이그레이션 필요.
    # class Meta:
    #     ordering = ["-created_at"]

class Comment(models.Model):
    content = models.TextField(max_length=300, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name="comments")

    #Comment.likes 로 접근가능
    likes = GenericRelation('Like') 

    def __str__(self):
        return self.content[:20]

class Like(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="likes")
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    liked_object = GenericForeignKey("content_type", "object_id")

    def __str__(self):
        return f"({self.user}, {self.liked_object})"
