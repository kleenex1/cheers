from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Recipe
# Register your models here.

admin.site.register(User, UserAdmin)
# User모델의 추가 필드는 admin 페이지에 따로 나오지 않기 때문에 설정을 해줘야한다.
UserAdmin.fieldsets += (("Custom fields", {"fields": ("nickname", "profile_pic", "introduce",)}),)

admin.site.register(Recipe)