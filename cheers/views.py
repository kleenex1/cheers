from django.shortcuts import render
from django.urls import reverse
from django.views.generic import (
    ListView, 
    DetailView, 
    CreateView, 
    UpdateView,
    DeleteView,
)
from allauth.account.views import PasswordChangeView
from cheers.models import Recipe
from cheers.forms import RecipeForm
# Create your views here.

class IndexView(ListView):
    model = Recipe
    template_name = 'cheers/index.html'
    context_object_name = "recipes"
    paginate_by = 4
    ordering = ['-created_at']
    

class RecipeDetailView(DetailView):
    model = Recipe 
    template_name = 'cheers/recipe_detail.html'
    pk_url_kwarg = 'recipe_id'

class RecipeCreateView(CreateView):
    model = Recipe
    form_class = RecipeForm
    template_name = "cheers/recipe_form.html"

    # 아래 메소드는 입력받은 데이터가 유효할때 데이터로 채워진 오브젝트로 만들고 저장
    # Recipe를 작성한 유저 데이터도 추가해서 같이 저장하도록 할 것 -> form_valid가 수행할것
    # class형 view에서는 self.request로 접근해야한다.
    # RecipeCreateView의 form_valid 메소드를 호출해주기만 하면 된다.
    # super는 recipecreateview의 상위 클래스 : CreateView를 뜻함
    # form instance에 유저author를 추가해주고, CreateView의 form_valid에 넣어줬기 때문에
    # author도 같이 저장되게 된다.(오버라이딩)
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    # redirect url 경로 설정
    # id가 파라미터로 전달(kwargs): 새로 생성된 오브젝트는 self.object로 접근가능
    def get_success_url(self):
        return reverse("recipe-detail", kwargs={"recipe_id": self.object.id})

class RecipeUpdateView(UpdateView):
    model = Recipe
    form_class = RecipeForm
    template_name = "cheers/recipe_form.html"
    pk_url_kwarg = "recipe_id"

    def get_success_url(self):
        return reverse("recipe-detail", kwargs={"recipe_id": self.object.id})

class RecipeDeleteView(DeleteView):
    model = Recipe
    template_name = "cheers/recipe_confirm_delete.html"
    pk_url_kwarg = "recipe_id"

    def get_success_url(self):
        return reverse('index')

# 비밀번호 변경 페이지를 커스텀해주는 View 
# 기존 PasswordChangeView를 상속받아서 자식 class에서 오버라이딩
class CustomPasswordChangeView(PasswordChangeView):
    def get_success_url(self):
        return reverse('index')