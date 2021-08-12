from django.http import request
from django.shortcuts import render,redirect,get_object_or_404,HttpResponseRedirect,reverse
from .forms import ArticleForm
from .models import Article,Comment
from django.contrib import messages
from django.contrib.auth.decorators import login_required


def articles(request):
    
    articles= Article.objects.all()
    return render(request,"articles.html",{"articles":articles})


def articles2(requset):
    articles = Article.objects.all()
    return render(requset,"articles2.html",{"articles":articles})

def userNotLogged(func):
    def _func(request, *args, **kwargs):
        # eğer bir kullanıcımız giriş yapmış ise
        if request.user.is_authenticated:
            # Anasayfaya yönlendiriyoruz
            return HttpResponseRedirect("/")
        #giris yapmamışsa fonksiyonu olduğu gibi dönderiyoruz ve sayfaya erişiyor
        return func(request, *args, **kwargs)
    return _func

    
# Create your views here.
def index(request):
    return render(request,"index.html")


def about(request):
    return render(request,"about.html")


@login_required(login_url="user:login")
def dashboard(request):
    articles =Article.objects.filter(author=request.user)
    context={
        "articles":articles
    }
    return render(request,"dashboard.html",context)


@login_required(login_url="user:login")
def addArticle(request):
    form = ArticleForm(request.POST or None,request.FILES or None)

    if form.is_valid():
        article = form.save(commit=False)
        
        article.author = request.user
        article.save()

        messages.success(request,"Makale başarıyla oluşturuldu")
        return redirect("article:dashboard")
    return render(request,"addarticle.html",{"form":form})


def detail(request,id):
    article = get_object_or_404(Article,id = id)

    comments = article.comments.all()
    return render(request,"detail.html",{"article":article,"comments":comments})


@login_required(login_url="user:login")
def updateArticle(request,id):
    article =get_object_or_404(Article,id=id)
    form =ArticleForm(request.POST or None,request.FILES or None, instance=article)
    if form.is_valid():
        article = form.save(commit=False)
        
        article.author = request.user
        article.save()

        messages.success(request,"Makale Başarıyla Güncellendi")
        return redirect("article:dashboard")

    return render(request,"update.html",{"form":form})


@login_required(login_url="user:login")
def deleteArticle(request,id):
    article = get_object_or_404(Article, id = id)
    if article.author.id == request.user.id:
        article.delete()
        messages.success(request,"Makale başarı ile silindi.")
        return redirect("article:dashboard")
    else:
        messages.error(request,"Bu makale size ait değil silemezsiniz.")
        return redirect("article:dashboard")
def addComment(request,id):
    article = get_object_or_404(Article,id=id)
    if request.method =="POST":
        comment_author=request.POST.get("comment_author")
        comment_content =request.POST.get("comment_content")

        newComment=Comment(comment_author = comment_author, comment_content= comment_content)
        newComment.article =article
        newComment.save()
        return redirect(reverse("article:detail",kwargs={"id":id}))