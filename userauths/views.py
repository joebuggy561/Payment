from django.shortcuts import render, redirect
from userauths.forms import UserRegisterForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from userauths.models import User

def RegisterView(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid:
            new_user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request,  "Your account was created successfully")
            new_user = authenticate(username=form.cleaned_data['email'], 
                                    password=form.cleaned_data['password1'])
            login(request, new_user)
            return redirect('account:account')
    
    elif request.user.is_authenticated:
        messages.warning(request, "You are already logged in.......")
        return redirect("account:account")

    else:
        form=UserRegisterForm()
    context = {
        'form':form
    }
    return render(request, "userauths/sign-up.html", context)
    


def LoginView(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            user = User.objects.get(email=email)
            user = authenticate(request, email=email, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, "You are logged In.")
                return redirect("account:account")
            else:
                messages.warning(request, "Username of Password")
                return redirect("userauths:sign-in")
        except:
            messages.warning(request, "User Does Not Exist")
    if request.user.is_authenticated:
        messages.success(request, "You are logged In.")
        return redirect("account:account")
    return render(request, 'userauths/sign-in.html')



def logoutView(request):
    logout(request)
    messages.success(request, "You have been logged out....")
    return redirect("userauths:sign-in")

# Create your views here.
