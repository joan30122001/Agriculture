from django.contrib.auth.models import User
from django.shortcuts import render, redirect, HttpResponse, redirect, get_object_or_404, reverse
from django.http import HttpResponseRedirect
from .forms import RegisterForm
from django.contrib.auth import authenticate, login, logout
from .forms import ArticleForm
from .models import Article,Comment
from django.contrib import messages
from django.template.defaultfilters import slugify
from django.db.models import Count
from django.contrib.auth.decorators import login_required






def home(request):
    return render(request, 'company/home.html')



def about(request):
    return render(request, 'company/about.html')



# def register(request):
#     if request.method == 'POST':
#         email = request.POST['email']
#         username = request.POST['username']
#         phone_number = request.POST['phone_number']
#         password1 = request.POST['password1']
#         password2 = request.POST['password2']

#         if password1 != password2:
#             error = 'Passwords do not match'
#         elif CustomUser.objects.filter(email=email).exists():
#             error = 'Email already exists'
#         elif CustomUser.objects.filter(username=username).exists():
#             error = 'Username already exists'
#         elif CustomUser.objects.filter(phone_number=phone_number).exists():
#             error = 'Phone number already exists'
#         else:
#             user = CustomUser.objects.create_user(email=email, username=username, phone_number=phone_number, password=password1)
#             user.save()
#             return redirect('login')

#         return render(request, 'registration/register.html', {'error': error})
#     else:
#         return render(request, 'registration/register.html')
def user_register(request):
    # if this is a POST request we need to process the form data
    template = 'registration/register.html'
   
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = RegisterForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            if User.objects.filter(username=form.cleaned_data['username']).exists():
                return render(request, template, {
                    'form': form,
                    'error_message': 'Username already exists.'
                })
            elif User.objects.filter(email=form.cleaned_data['email']).exists():
                return render(request, template, {
                    'form': form,
                    'error_message': 'Email already exists.'
                })
            elif form.cleaned_data['password'] != form.cleaned_data['password_repeat']:
                return render(request, template, {
                    'form': form,
                    'error_message': 'Passwords do not match.'
                })
            else:
                # Create the user:
                user = User.objects.create_user(
                    form.cleaned_data['username'],
                    form.cleaned_data['email'],
                    form.cleaned_data['password']
                )
                user.first_name = form.cleaned_data['first_name']
                user.last_name = form.cleaned_data['last_name']
                user.phone_number = form.cleaned_data['phone_number']
                user.save()
               
                # Login the user
                login(request, user)
               
                # redirect to accounts page:
                return redirect('home')

   # No post data availabe, let's just show the page.
    else:
        form = RegisterForm()

    return render(request, template, {'form': form})







# def user_login(request):
#     if request.method == 'POST':
#         username = request.POST['username']
#         password = request.POST['password']

#         user = authenticate(request, username=username, password=password)

#         if user is not None:
#             login(request, user)
#             return redirect('home')
#             # return render(request, 'company/home.html')
#         else:
#             error = 'Invalid email or password'
#             return render(request, 'registration/login.html', {'error': error})
#     else:
#         return render(request, 'registration/login.html')
def user_login(request):
    if request.method == 'POST':
        # Process the request if posted data are available
        username = request.POST['username']
        password = request.POST['password']
        # Check username and password combination if correct
        user = authenticate(username=username, password=password)
        if user is not None:
            # Save session as cookie to login the user
            login(request, user)
            # Success, now let's login the user.
            # return render(request, 'company/home.html')
            return redirect('home')
        else:
            # Incorrect credentials, let's throw an error to the screen.
            return render(request, 'registration/login.html', {'error_message': 'Incorrect username and / or password.'})
    else:
        # No post data availabe, let's just show the page to the user.
        return render(request, 'registration/login.html')



def user_logout(request):
    logout(request)
    return redirect('home')



def articles(request):
    keyword = request.GET.get("keyword")

    if keyword:
        articles = Article.objects.filter(title__contains = keyword)
        return render(request,"company/articles.html",{"articles":articles})
    articles = Article.objects.all()

    return render(request,"company/articles.html",{"articles":articles})


    
def dashboard(request):
    articles = Article.objects.filter(author = request.user)
    context = {
        "articles":articles
    }
    return render(request,"company/dashboard.html",context)



# @login_required(login_url = "user:login")
def addArticle(request):
    form = ArticleForm(request.POST or None,request.FILES or None)

    if form.is_valid():
        article = form.save(commit=False)
        article.slug = slugify(article.title)
        article.author = request.user
        article.save()

        messages.success(request,"Post created successfully")
        return redirect("dashboard")
    return render(request,"company/addarticle.html",{"form":form})



def detail(request,slug):
    #article = Article.objects.filter(id = id).first()   
    article = get_object_or_404(Article, slug=slug)
    comments = article.comments.all()
    return render(request,"company/detail.html",{"article":article,"comments":comments })



# @login_required(login_url = "user:login")
def updateArticle(request, slug):

    article = get_object_or_404(Article, slug=slug)
    form = ArticleForm(request.POST or None,request.FILES or None,instance = article)
    if form.is_valid():
        article = form.save(commit=False)
        
        article.author = request.user
        article.save()

        messages.success(request,"Makale başarıyla güncellendi")
        return redirect("dashboard")


    return render(request,"company/update.html",{"form":form})



# @login_required(login_url = "user:login")
def deleteArticle(request,slug):
    article = get_object_or_404(Article,slug=slug)

    article.delete()

    messages.success(request,"Makale Başarıyla Silindi")

    return redirect("article:dashboard")


    
def addComment(request,slug):
    article = get_object_or_404(Article, slug=slug)

    if request.method == "POST":
        comment_author = request.POST.get("comment_author")
        comment_content = request.POST.get("comment_content")

        newComment = Comment(comment_author  = comment_author, comment_content = comment_content)

        newComment.article = article

        newComment.save()
    return redirect(reverse("detail",kwargs={"slug":slug}))
    