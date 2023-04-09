from django.urls import path
from .views import home, about
from . import views

urlpatterns = [
    path('', home, name='home'),
    path('about', about, name='about'),

    path('register/', views.user_register, name='user_register'),
    path('login/', views.user_login, name='user_login'),
    path('logout/', views.user_logout, name='user_logout'),

    path('dashboard/',views.dashboard,name = "dashboard"),
    path('addarticle/',views.addArticle,name = "addarticle"),
    path('article/<slug:slug>/',views.detail,name = "detail"),
    path('update/<slug:slug>',views.updateArticle,name = "update"),
    path('delete/<slug:slug>',views.deleteArticle,name = "delete"),
    path('Services',views.articles,name = "articles"),
    path('comment/<slug:slug>',views.addComment,name = "comment"),
]