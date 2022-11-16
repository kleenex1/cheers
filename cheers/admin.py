from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.contenttypes.admin import GenericStackedInline
from .models import User, Recipe, Comment, Like
# Register your models here.

class UserInline(admin.StackedInline):
    model = User.following.through
    fk_name = 'to_user'
    verbose_name = 'Follower'
    verbose_name_plural = 'Followers' 

class CommentInline(admin.StackedInline):
    model = Comment

# GenericForeignKey를 통해 관계를 맺고 있는것은 StackedInline을 못쓴다.
# class LikeInline(admin.StackedInline):
#     model = Like

class LikeInline(GenericStackedInline):
    model = Like

class RecipeAdmin(admin.ModelAdmin):
    inlines = (
        CommentInline,
        LikeInline,
    )

class CommentAdmin(admin.ModelAdmin):
    inlines = (
        LikeInline,
    )

admin.site.register(User, UserAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Like)


# User모델의 추가 필드는 admin 페이지에 따로 나오지 않기 때문에 설정을 해줘야한다.
UserAdmin.fieldsets += (("Custom fields", {"fields": ("nickname", "profile_pic", "introduce", "following")}),)
UserAdmin.inlines = (UserInline,)

