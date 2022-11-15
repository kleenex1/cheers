from django.shortcuts import render

# Create your views here.

def index(request):
    print(request.user.is_authenticated)
   
    return render(request, "cheers/index.html")