from django.shortcuts import render

def login(request):
    return render(request, 'login.html')

# Create your views here.
def home(request):
    return render(request, 'home.html')

def signup(request):
    return render(request, 'signup.html')