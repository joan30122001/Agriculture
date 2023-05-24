from django.contrib.auth.models import User
from django.shortcuts import render, redirect, HttpResponse, redirect, get_object_or_404, reverse
from django.http import HttpResponseRedirect
from .forms import RegisterForm, UserForm, ProfileForm, StoryForm
from django.contrib.auth import authenticate, login, logout
from .forms import ArticleForm
from .models import Article, Comment, Category, Profile, Post, Story
from django.contrib import messages
from django.template.defaultfilters import slugify
from django.db.models import Count
from django.contrib.auth.decorators import login_required 
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView
from django.utils import timezone
from django.views.generic import View
from django.conf import settings






def home(request):
    return render(request, 'company/home.html')



def about(request):
    return render(request, 'company/about.html')



def create_story(request):
    # if request.method == 'POST':
    form = StoryForm(request.POST, request.FILES)
    if form.is_valid():
        story = form.save(commit=False)
        story.user = request.user
        story.save()
        return redirect('create_story')
    # else:
    #     form = StoryForm()
    return render(request, 'registration/create_story.html', {"form":form})



def story(request):
    story = Story.objects.all()
    return render(request, 'registration/story.html', {"story":story})



class DeleteExpiredRecordsView(View):
    def get(self, request, *args, **kwargs):
        expired_records = Story.objects.filter(expire_at__lt=timezone.now())
        expired_records.delete()
        return HttpResponse('Expired records deleted')



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
            return redirect('dashboard')
        else:
            # Incorrect credentials, let's throw an error to the screen.
            return render(request, 'registration/login.html', {'error_message': 'Incorrect username and / or password.'})
    else:
        # No post data availabe, let's just show the page to the user.
        return render(request, 'registration/login.html')



def user_logout(request):
    logout(request)
    return redirect('home')



# @login_required
# def profile(request):
#     return render(request, 'profile.html')






class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'registration/profile.html'



class ProfileUpdateView(LoginRequiredMixin, TemplateView):
    user_form = UserForm
    profile_form = ProfileForm
    template_name = 'registration/profile-update.html'

    def post(self, request):
        Profile.objects.get_or_create(user=request.user)
        post_data = request.POST or None
        file_data = request.FILES or None

        user_form = UserForm(post_data, instance=request.user)
        profile_form = ProfileForm(post_data, file_data, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.error(request, 'Your profile is updated successfully!')
            return HttpResponseRedirect(reverse_lazy('profile'))

        context = self.get_context_data(
                                        user_form=user_form,
                                        profile_form=profile_form
                                    )

        return self.render_to_response(context)     

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)



def all_profile(request):
    keyword = request.GET.get("keyword")    

    # profiles = Profile.objects.exclude(activity='', speciality='')

    # keyword = request.GET.get("keyword")
    if keyword:
        profiles = Profile.objects.filter(activity__contains = keyword)
        return render(request,"registration/all_profile.html",{"profiles":profiles})
    profiles = Profile.objects.exclude(activity='', speciality='')

    return render(request, 'registration/all_profile.html', {'profiles': profiles})




def articles(request):
    keyword = request.GET.get("keyword")

    categories = Category.objects.all()

    if keyword:
        articles = Article.objects.filter(title__contains = keyword)
        return render(request,"company/articles.html",{"articles":articles})
    articles = Article.objects.all()

    return render(request,"company/articles.html",{"articles":articles, "categories":categories})


    
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
        article.profile = request.user.profile
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
        # comment_author = request.POST.get("comment_author")
        comment_content = request.POST.get("comment_content")

        # newComment = Comment(comment_author  = comment_author, comment_content = comment_content)
        newComment = Comment(comment_content = comment_content)

        newComment.article = article
        newComment.comment_author = request.user

        newComment.save()
    return redirect(reverse("detail",kwargs={"slug":slug}))



def profile_posts(request, profile_id):
    profile = get_object_or_404(Profile, pk=profile_id)
    articles = Article.objects.filter(profile=profile)
    return render(request, 'registration/profile_posts.html', {'profile': profile, 'articles': articles})



# def profile_posts(request, profile_id):
#     profile = get_object_or_404(Profile, pk=profile_id)
#     articles = profile.articles.all()
#     return render(request, 'registration/profile_posts.html', {'profile': profile, 'articles': articles})



# def initiate_payment(request: HttpRequest) -> HttpResponse:
#     if request.method == 'POST':
#         payment_form = forms.PaymentForm(request.POST)
#         if payment_form.is_valid():
#             payment = payment_form.save()
#             return render(request, 'registration/make_payment.html', {'payment': payment, 'paystack_public_key': settings.PAYSTACK_PUBLIC_KEY})
#     else:
#         payment_form = forms.PaymentForm()
#     return render(request, 'registration/initiated_payment.html', {'payment_form': payment_form})



# def verify_payment(request: HttpRequest, ref: str) -> HttpResponse:
#     payment = get_object_or_404(Payment, ref=ref)
#     verified = payment.verify_payment()
#     if verified:
#         messages.success(request, "Verification Successfull")
#     else:
#         messages.error(request, "Verification Failed.")
#     return redirect('initiate-payment')