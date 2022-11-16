from django.shortcuts import render
from django.urls import reverse
from django.views.generic import (
    ListView, 
    DetailView, 
    CreateView, 
    UpdateView,
    DeleteView,
)
from braces.views import LoginRequiredMixin, UserPassesTestMixin
from allauth.account.models import EmailAddress
from allauth.account.views import PasswordChangeView
from cheers.models import Recipe, User
from cheers.forms import RecipeForm
from cheers.functions import confirmation_required_redirect
# Create your views here.

class IndexView(ListView):
    model = Recipe
    template_name = "cheers/index.html"
    context_object_name = "recipes"
    paginate_by = 4
    ordering = ["-created_at"]
    

class RecipeDetailView(DetailView):
    model = Recipe 
    template_name = "cheers/recipe_detail.html"
    pk_url_kwarg = "recipe_id"

class RecipeCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Recipe
    form_class = RecipeForm
    template_name = "cheers/recipe_form.html"

    # user가 CreateView에 접근하려고하면, LoginRequiredMixin UserPassesTestMixin이 실행되고 통과하지 못하면,
    # 아래 redirec_unauthenticated_users 는 LOGIN_URL로 redirect 되고
    # 로그인이 되어있지만 인증이 되어있지 않은 유저는 raise_exception으로 처리된다.
    # raise_exception의 커스텀 함수 confirmation_required_redirect의 로직으로 처리됨.
    redirect_unauthenticated_users = True
    raise_exception = confirmation_required_redirect

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

    # TestMixin의 메소드를 구현
    # 이메일 Address를 allauth에서 import하여 사용
    # allauth는 유저들의 Email들을 EmailAddress를 저장한다. 
    def test_func(self, user):
        return EmailAddress.objects.filter(user=user, verified=True).exists()
            

class RecipeUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Recipe
    form_class = RecipeForm
    template_name = "cheers/recipe_form.html"
    pk_url_kwarg = "recipe_id"

    raise_exception = True

    def get_success_url(self):
        return reverse("recipe-detail", kwargs={"recipe_id": self.object.id})
    
    # TestMixin으로 User 확인해주기
    # html에서 유저가 본인 게시물인지 확인을 해서 버튼을 숨겨놨어도
    # 주소창을 통해서 해당 글을 수정하려고 하는 것을 막기 위함
    # 부적절한 접근은 403으로 막아준다. --> rasise_exception = True
    # 로그인이 유무랑 상관없이 403으로 redirect_unauthenticated_users = False (default값)
    def test_func(self, user):
        recipe = self.get_object()
        return recipe.author == user

class RecipeDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Recipe
    template_name = "cheers/recipe_confirm_delete.html"
    pk_url_kwarg = "recipe_id"

    raise_exception = True

    def get_success_url(self):
        return reverse("index")

    def test_func(self, user):
        recipe = self.get_object()
        return recipe.author == user

class ProfileView(DetailView):
    model = User 
    template_name = "cheers/profile.html"
    pk_url_kwarg = "user_id"
    context_object_name = "profile_user"

    # context는 dic형태인데 여기에 추가해주면된다.
    # url로 전달되는 파라미터는 self.kwargs로 접근가능하다.
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_id = self.kwargs.get("user_id")
        context["user_recipes"] = Recipe.objects.filter(author__id=user_id).order_by("-created_at")[:4]
        return context

# 비밀번호 변경 페이지를 커스텀해주는 View 
# 기존 PasswordChangeView를 상속받아서 자식 class에서 오버라이딩
class CustomPasswordChangeView(PasswordChangeView):
    def get_success_url(self):
        return reverse("index")