from django.shortcuts import render
from django.urls import reverse
from django.views.generic import ListView
from allauth.account.views import PasswordChangeView
from cheers.models import Recipe
# Create your views here.

class IndexView(ListView):
    model = Recipe
    template_name = 'cheers/index.html'
    context_object_name = "recipes"
    paginate_by = 4
    ordering = ['-created_at']
    

# 비밀번호 변경 페이지를 커스텀해주는 View 
# 기존 PasswordChangeView를 상속받아서 자식 class에서 오버라이딩
class CustomPasswordChangeView(PasswordChangeView):
    def get_success_url(self):
        return reverse('index')