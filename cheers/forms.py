from django import forms 
from .models import User

class SignupForm(forms.ModelForm):
    class Meta:
        model = User
        # 기본적인 email, username은 제외하고 추가한 필드만 명시
        fields = ["nickname"]
        
    def signup(self, request, user):
        # django form에 기입된 데이터는 cleaned_data로 가져올 수 있다.
        user.nickname = self.cleaned_data["nickname"]
        user.save()