from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.generic import (
    View,
    ListView, 
    DetailView, 
    CreateView, 
    UpdateView,
    DeleteView,
)
from django.contrib.contenttypes.models import ContentType
from braces.views import LoginRequiredMixin, UserPassesTestMixin
from allauth.account.models import EmailAddress
from allauth.account.views import PasswordChangeView
from cheers.models import Recipe, User, Comment, Like
from cheers.forms import RecipeForm, ProfileForm, CommentForm
from cheers.functions import confirmation_required_redirect

# Create your views here.

class IndexView(View):
    def get(self, request, *args, **kwargs):
        context = {}
        context['latest_recipes'] = Recipe.objects.all().order_by("-created_at")[:4]
        user = self.request.user
        if user.is_authenticated:
            context['latest_following_recipes'] = Recipe.objects.filter(author__followers=user).order_by("-created_at")[:4]
        return render(request, 'cheers/index.html', context)

class RecipeListView(ListView):
    model = Recipe
    context_object_name = 'recipes'
    template_name = 'cheers/recipe_list.html'
    paginate_by = 8
    ordering = ['-created_at']

class FollowingRecipeListView(LoginRequiredMixin, ListView):
    model = Recipe
    context_object_name = 'following_recipes'
    template_name = 'cheers/following_recipe_list.html'
    paginate_by = 8

    def get_queryset(self):
        return Recipe.objects.filter(author__followers=self.request.user)

class RecipeDetailView(DetailView):
    model = Recipe 
    template_name = "cheers/recipe_detail.html"
    pk_url_kwarg = "recipe_id"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        # 좋아요 contenttype id를 넘겨주기 위한 코드
        context['recipe_ctype_id'] = ContentType.objects.get(model='recipe').id
        context['comment_ctype_id'] = ContentType.objects.get(model='comment').id
        
        # 좋아요 눌렀는지 판단하기
        user = self.request.user
        if user.is_authenticated:
            recipe = self.object 
            context['likes_recipes'] = Like.objects.filter(user=user, recipe=recipe).exists()
            context['liked_comments'] = Comment.objects.filter(recipe=recipe).filter(likes__user=user)
        return context

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

class CommentCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    http_method_names = ['post']
    model = Comment
    form_class = CommentForm

    redirect_unauthenticated_users = True
    raise_exception = confirmation_required_redirect

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.recipe = Recipe.objects.get(id=self.kwargs.get('recipe_id'))
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('recipe-detail', kwargs={'recipe_id': self.kwargs.get('recipe_id')})

    def test_func(self, user):
        return EmailAddress.objects.filter(user=user, verified=True).exists()

class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = 'cheers/comment_update_form.html'
    pk_url_kwarg = 'comment_id'
    redirect_unauthenticated_users = True
    raise_exception = confirmation_required_redirect
    
    def get_success_url(self):
        return reverse('recipe-detail', kwargs={'recipe_id': self.object.recipe.id})
    
    def test_func(self, user):
        recipe = self.get_object()
        return recipe.author == user

class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = 'cheers/comment_confirm_delete.html'
    pk_url_kwarg = 'comment_id'
    redirect_unauthenticated_users = True
    raise_exception = confirmation_required_redirect
    
    def get_success_url(self):
        return reverse('recipe-detail', kwargs={'recipe_id': self.object.recipe.id})

    def test_func(self, user):
        recipe = self.get_object()
        return recipe.author == user

class ProcessLikeView(LoginRequiredMixin, UserPassesTestMixin, View):
    http_method_name = ['post']
    redirect_unauthenticated_users = True
    raise_exception = confirmation_required_redirect
    
    def post(self, request, *args, **kwargs):
        # self.kwargs.get('content_type_id')
        # self.kwargs.get('object_id')
        
        like, created = Like.objects.get_or_create(
            user=self.request.user,
            content_type_id=self.kwargs.get('content_type_id'),
            object_id=self.kwargs.get('object_id'),
        )

        if not created:
            like.delete()

        return redirect(self.request.META['HTTP_REFERER'])

   	
    def test_func(self, user):
        return EmailAddress.objects.filter(user=user, verified=True).exists()
    

class ProfileView(DetailView):
    model = User 
    template_name = "cheers/profile.html"
    pk_url_kwarg = "user_id"
    context_object_name = "profile_user"

    # context는 dic형태인데 여기에 추가해주면된다.
    # url로 전달되는 파라미터는 self.kwargs로 접근가능하다.
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        profile_user_id = self.kwargs.get('user_id')
        if user.is_authenticated:
            context['is_following'] = user.following.filter(id=profile_user_id).exists()
        context["user_recipes"] = Recipe.objects.filter(author__id=profile_user_id).order_by("-created_at")[:4]
        return context

# 요청에 따라 다르게 처리해줘야 해서 제네릭 뷰가 아닌 일반 뷰
class ProcessFollowView(LoginRequiredMixin, UserPassesTestMixin, View):
    http_method_name = ['post']

    redirect_unauthenticated_users = True
    raise_exception = confirmation_required_redirect

    def post(self, request, *args, **kwargs):
        user = self.request.user
        profile_user_id = self.kwargs.get('user_id')
        if user.following.filter(id=profile_user_id).exists():
            user.following.remove(profile_user_id)
        else:
            user.following.add(profile_user_id)
        return redirect('profile', user_id=profile_user_id)   

    def test_func(self, user):
        return EmailAddress.objects.filter(user=user, verified=True).exists()

class FollowingListView(ListView):
    model = User
    template_name = 'cheers/following_list.html'
    context_object_name = 'following'
    paginate_by = 10

    def get_queryset(self):
        profile_user = get_object_or_404(User, pk=self.kwargs.get('user_id'))
        return profile_user.following.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile_user_id'] = self.kwargs.get('user_id')
        return context

class FollowerListView(ListView):
    model = User
    template_name = 'cheers/follower_list.html'
    context_object_name = 'followers'
    paginate_by = 10

    def get_queryset(self):
        profile_user = get_object_or_404(User, pk=self.kwargs.get('user_id'))
        return profile_user.followers.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile_user_id'] = self.kwargs.get('user_id')
        return context

class UserRecipesListView(ListView):
    model = Recipe
    template_name = "cheers/user_recipe_list.html"
    context_object_name = "user_recipes"
    paginate_by = 4

    # 기본적으로 전체 Recipes들을 List로 전달한다. 따로 context에 전달하지 않아도 됨
    def get_queryset(self):
        user_id = self.kwargs.get("user_id")
        return Recipe.objects.filter(author__id=user_id).order_by("-created_at")
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["profile_user"] = get_object_or_404(User, id=self.kwargs.get("user_id"))
        return context


class ProfileSettingView(LoginRequiredMixin, UpdateView):
    model = User 
    form_class = ProfileForm
    template_name = 'cheers/profile_setting_form.html'

    # updateview는 쿼리하나만 다루니까 get_object 오버라이드
    # listview는 쿼리셋을 다루니까 get_queryset 오버라이드
    def get_object(self, queryset=None):
        return self.request.user
    
    def get_success_url(self):
        return reverse("index")
   
class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User 
    form_class = ProfileForm
    template_name = 'cheers/profile_update_form.html'

    # updateview는 쿼리하나만 다루니까 get_object 오버라이드
    # listview는 쿼리셋을 다루니까 get_queryset 오버라이드
    def get_object(self, queryset=None):
        return self.request.user
    
    def get_success_url(self):
        return reverse("profile", kwargs={"user_id": self.request.user.id})



# 비밀번호 변경 페이지를 커스텀해주는 View 
# 기존 PasswordChangeView를 상속받아서 자식 class에서 오버라이딩
class CustomPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    def get_success_url(self):
        return reverse("profile", kwargs={"user_id": self.request.user.id})