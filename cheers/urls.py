from django.urls import path
from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('recipes/<int:recipe_id>/', views.RecipeDetailView.as_view(),name='recipe-detail'),
    path('recipes/create/', views.RecipeCreateView.as_view(), name="recipe-create")
]