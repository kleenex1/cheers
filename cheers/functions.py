from django.shortcuts import redirect
from allauth.account.utils import send_email_confirmation
# rasise_excpetion에 들어가는 함수는 self, request를 파라미터로 받는다.
# redirect하기 위해 import redirect한다.

def confirmation_required_redirect(self, request):
    # 이메일 인증을 하지 않은 유저에게 이메일을 발송하기
    # allauth가 제공하는 sendemail confirmation 함수 사용하기
    send_email_confirmation(request, request.user)
    # 그 다음 이메일 인증 확인 페이지로 redirect해주기(회원가입시 보내는 인증메일과 다르다.)
    return redirect("account_email_confirmation_required")

