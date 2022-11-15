"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from cheers.views import CustomPasswordChangeView


urlpatterns = [
    # admin
    path('admin/', admin.site.urls),
    
    # cheers
    path('', include("cheers.urls")),
    
    # allauth

    # 단순히 페이지를 render해주기만 하면되는 페이지라서 
    # 따로 view를 작성하지 않고 Generic view(template view)를 활용
    path("email-confirmation", 
    TemplateView.as_view(template_name="cheers/email_confirmation.html") 
    ,name="account_email_confirmation"),
    # Password 변경시 url 설정 (allauth가 설정한 곳이 아닌 커스텀하여 내가 redirect하고싶은 곳으로)
    # 'allauth.urls'보다 먼저 나와있어야 해당 url로 먼저 간다.
    path('password/change/', 
    CustomPasswordChangeView.as_view(), 
    name='account_password_change' ),
    path('', include('allauth.urls')),
]
