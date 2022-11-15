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
    path('', include('allauth.urls')),
]
