from django.shortcuts import render
from django.urls import reverse
from allauth.account.views import PasswordChangeView
# Create your views here.

def index(request):
    
   
    return render(request, "cheers/index.html")

# 비밀번호 변경 페이지를 커스텀해주는 View 
# 기존 PasswordChangeView를 상속받아서 자식 class에서 오버라이딩
class CustomPasswordChangeView(PasswordChangeView):
    def get_success_url(self):
        return reverse('index')