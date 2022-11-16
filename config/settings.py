"""
Django settings for config project.

Generated by 'django-admin startproject' using Django 3.2.13.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-j%c8*e)anqbc)p37t@s&1a#$$^1u7!vco-4u-2e8%m8w^wtb-y"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # 어떤 기능을 여러사이트에서 사용할 수 있게 해줌(프로젝트 하나로 여러사이트 운영)
    "django.contrib.sites",
    "cheers",
    "widget_tweaks",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
]

# 각각 사이트의 아이디를 뜻함 (django.contrib.sites)
SITE_ID = 1

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

# django가 제공하는 기본 validator를 지우고 커스텀한 validator를 적용한다.
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "cheers.validators.CustomPasswordValidator",},
]


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = "ko"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = "/static/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")
MEDIA_URL = "/uploads/"

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# Auth User Settings

AUTH_USER_MODEL = "cheers.User"

AUTHENTICATION_BACKENDS = [
    # Needed to login by username in Django admin, regardless of `allauth`
    "django.contrib.auth.backends.ModelBackend",
    # `allauth` specific authentication methods, such as login by e-mail
    "allauth.account.auth_backends.AuthenticationBackend",
]

# 로그인시 redirect할 url 설정
ACCOUNT_SIGNUP_REDIRECT_URL = "index"
LOGIN_REDIRECT_URL = "index"
# 웹서비스 로그인 URL : LoginRequiredMixin이 실행되면 로그인을 하도록 아래 url로 설정
LOGIN_URL = 'account_login'
# 로그아웃시 redirect가 Allauth 기본 셋팅(로그아웃화면이뜸)으로 가는데 거치지 않고 바로 로그아웃 할 수 있게해줌.
ACCOUNT_LOGOUT_ON_GET = True
# 이메일로 로그인 하는 방법 (default = 유저네임으로 로그인, 둘다 허용하는 방법 = username_email)
ACCOUNT_AUTHENTICATION_METHOD = "email"
# 회원 가입시 email 필수 항목으로 설정, 유저네임은 없애줌
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
# 내가 정의한 SignupForm을 쓰겠다고 settings에 알려줌
ACCOUNT_SIGNUP_FORM_CLASS = "cheers.forms.SignupForm"
# 회원가입시 폼에 오류가 나더라도 비밀번호는 그대로 남아있게 설정
ACCOUNT_PASSWORD_INPUT_RENDER_VALUE = True
# 이메일 인증 관련 설정(mandatory, optional(default값), none)
ACCOUNT_EMAIL_VARIFICATION = "optional"
# 이메일 인증 완료 메일을 누르면 기존 allauth url로 redirect되는 것을 막고 내가 설정해놓은 곳으로 redirect
ACCOUNT_CONFIRM_EMAIL_ON_GET = True
# 인증 메일이 오면 email_confirmation.html이 뜰 수 있도록 한다.
ACCOUNT_EMAIL_CONFIRMATION_AUTHENTICATED_REDIRECT_URL = "account_email_confirmation"
ACCOUNT_EMAIL_CONFIRMATION_ANONYMOUS_REDIRECT_URL = "account_email_confirmation"
# 비밀번호 재설정 링크 유효기간(초)
PASSWORD_RESET_TIMEOUT = 3600
# allauth가 발송하는 이메일 제목에는 오버라이딩을 해도 항상 domain이 앞에 붙게 된다.(이를 제거하는 세팅)
ACCOUNT_EMAIL_SUBJECT_PREFIX = ""

# Email settings

# Allauth 이메일 기능 활용(현재 터미널콘솔로 이메일전송하는방법)
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

