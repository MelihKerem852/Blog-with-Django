from django.shortcuts import render,redirect,HttpResponseRedirect
from .forms import RegisterForm,LoginForm
from django.contrib.auth.models import User
from django.contrib.auth import login,authenticate,logout
from django.contrib import messages

def userNotLogged(func):
    def _func(request, *args, **kwargs):
        # eğer bir kullanıcımız giriş yapmış ise
        if request.user.is_authenticated:
            # Anasayfaya yönlendiriyoruz
            return HttpResponseRedirect("/")
        #giris yapmamışsa fonksiyonu olduğu gibi dönderiyoruz ve sayfaya erişiyor
        return func(request, *args, **kwargs)
    return _func


@userNotLogged
def register(request):

    form = RegisterForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")

        newUser = User(username =username)
        newUser.set_password(password)

        newUser.save()
        login(request,newUser)
        messages.success(request,"Başarıyla Kayıt Oldunuz...")

        return redirect("index")
    context = {
            "form" : form
        }
    return render(request,"register.html",context)

    
    

@userNotLogged
def loginUser(request):
    form = LoginForm(request.POST or None)

    context = {
        "form":form
    }

    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")

        user = authenticate(username = username,password = password)

        if user is None:
            messages.info(request,"Kullanıcı Adı veya Parola Hatalı")
            return render(request,"login.html",context)

        messages.success(request,"Başarıyla Giriş Yaptınız")
        login(request,user)
        return redirect("index")
    return render(request,"login.html",context)
def logoutUser(request):
    logout(request)
    messages.success(request,"Başarıyla Çıkış Yaptınız")
    return render(request,"index.html")
