from django import forms
from .models import Article, Category, Profile, Story
from ckeditor.widgets import CKEditorWidget
from tinymce.widgets import TinyMCE
from django.contrib.auth.models import User
from PIL import Image



class RegisterForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password_repeat = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    phone_number = forms.CharField(widget=forms.NumberInput(attrs={'class':'form-control'}), required=False)


# CATEGORIES = (
#     ('Coseiller agricole', 'Coseiller agricole'),
#     ("Conducteur d'engins forestiers", "Conducteur d'engins forestiers"),
#     ('Horticulteur', 'Horticulteur'),
#     ('Ingénieur agronome', 'Ingénieur agronome'),
#     ('Arboriculteur', 'Arboriculteur'),
#     ('Jardinier', 'Jardinier'),
#     ('Maraîcher', 'Maraîcher'),
#     ('Mécanicien de machines agricoles', 'Mécanicien de machines agricoles'),
#     ('Pépiniériste', 'Pépiniériste'),
# )


class ArticleForm(forms.ModelForm):
    # content = forms.CharField(widget = CKEditorWidget())
    # forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 30}))
    # category = forms.CharField(widget=forms.Select(attrs={'class':'form-control'}))
    # category = forms.ChoiceField(choices = CATEGORIES, widget=forms.Select(attrs={'class': 'form-control'}))
    category = forms.ModelChoiceField(queryset=Category.objects.all(), widget=forms.Select(attrs={'class':'form-control'}))
    # profile = forms.ModelChoiceField(queryset=Profile.objects.all(), widget=forms.Select(attrs={'class':'form-control'}))
    class Meta:
        model = Article
        fields = [
            # "profile",
            "title",
            "category",
            "content",
            "article_image",
        ]    
    # widgets = {
    #     'category': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Emetteur du courrier...',}),
    #     }



# class UserForm(forms.ModelForm):
#     class Meta:
#         model = User
#         fields = ('first_name', 'last_name', 'email', 'username')



# class ProfileForm(forms.ModelForm):
#     class Meta:
#         model = Profile
#         fields = ('bio', 'location', 'birth_date', 'profile_pic')





class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'username', 
            'first_name', 
            'last_name', 
            'email', 
        ]

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            'bio',
            'phone_number',
            'birth_date',
            'activity',
            'speciality',
            'profile_image'
        ]



class StoryForm(forms.ModelForm):
    class Meta:
        model = Story
        fields = ['image', 'caption']



# class PaymentForm(forms.ModelForm):
#     class Meta: 
#         model = Payment
#         fields = [
#             'amount', 
#             'email',
#         ]