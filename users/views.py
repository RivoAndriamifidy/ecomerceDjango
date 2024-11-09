from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, login, logout,authenticate

# Create your views here.

User = get_user_model()
def seConnecter(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        
        user = User.objects.create_user(username = username,
                                        email = email,
                                        password = password)
        login(request, user)
        return redirect('index')
        
    
    return render(request, 'users/seConnecter.html')

def login_user(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username = username, password = password)
        if user:
            login(request, user) 
            return redirect('index') 
    return render(request, 'users/login.html')
        

def logout_user(request):
    logout(request)
    return redirect('index')

