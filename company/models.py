from django.db import models
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from PIL import Image
from django.utils import timezone
import secrets
# from .paystack import PayStack




CATEGORIES = (
    ('Coseiller agricole', 'Coseiller agricole'),
    ("Conducteur d'engins forestiers", "Conducteur d'engins forestiers"),
    ('Horticulteur', 'Horticulteur'),
    ('Ingénieur agronome', 'Ingénieur agronome'),
    ('Arboriculteur', 'Arboriculteur'),
    ('Jardinier', 'Jardinier'),
    ('Maraîcher', 'Maraîcher'),
    ('Mécanicien de machines agricoles', 'Mécanicien de machines agricoles'),
    ('Pépiniériste', 'Pépiniériste'),
)

class Category(models.Model):
    category = models.CharField(max_length=100)

    def __str__(self):
        return self.category


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    phone_number = models.CharField(max_length=12, blank=True)
    activity = models.CharField(max_length=255, blank=True)
    speciality = models.CharField(max_length=255, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    profile_image = models.ImageField(default='default-avatar.png', upload_to='users/', null=True, blank=True)

    # def __str__(self):
    #     return '%s %s' % (self.user.first_name, self.user.last_name)
    def __str__(self):
        return self.user.username




class Article(models.Model):
    author = models.ForeignKey("auth.User",on_delete = models.CASCADE, related_name='articles')
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, blank=True, null=True)
    title = models.CharField(max_length = 255)
    # category = models.CharField(max_length=100, choices=CATEGORIES)
    category = models.ForeignKey("Category",on_delete = models.CASCADE)
    content = RichTextField()
    created_date = models.DateTimeField(auto_now_add=True)
    article_image = models.FileField(upload_to='files/', blank = True,null = True)
    slug = models.SlugField(unique=True, max_length=100)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super(Article, self).save(*args, **kwargs)        

    class Meta:
        ordering = ['-created_date']


        
class Comment(models.Model):
    article = models.ForeignKey(Article,on_delete = models.CASCADE,related_name="comments")
    # comment_author = models.CharField(max_length = 50)
    comment_author = models.ForeignKey(User,on_delete = models.CASCADE)
    comment_content = models.CharField(max_length = 200)
    comment_date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.comment_content
    class Meta:
        ordering = ['-comment_date']



# class Profile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     bio = models.TextField(max_length=500, blank=True)
#     phone_number = models.CharField(max_length=12, blank=True)
#     activity = models.CharField(max_length=255, blank=True)
#     speciality = models.CharField(max_length=255, blank=True)
#     birth_date = models.DateField(null=True, blank=True)
#     profile_image = models.ImageField(default='default-avatar.png', upload_to='users/', null=True, blank=True)

#     # def __str__(self):
#     #     return '%s %s' % (self.user.first_name, self.user.last_name)
#     def __str__(self):
#         return self.user.username


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()



class Post(models.Model):
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    title = models.CharField(max_length = 255)
    # category = models.CharField(max_length=100, choices=CATEGORIES)
    category = models.ForeignKey("Category",on_delete = models.CASCADE)
    content = RichTextField()
    created_date = models.DateTimeField(auto_now_add=True)
    article_image = models.FileField(upload_to='files/', blank = True,null = True)
    slug = models.SlugField(unique=True, max_length=100)



class Story(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/')
    caption = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    expire_at = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.expire_at:
            self.expire_at = timezone.now() + timezone.timedelta(minutes=10)
        super().save(*args, **kwargs)



# class Payment(models.Model):
#     amount = models.PositiveIntegerField()
#     ref = models.CharField(max_length=255)
#     email = models.EmailField()
#     verified = models.BooleanField(default=False)
#     date_created = models.DateTimeField(auto_now_add=True) 

#     class META: 
#         ordering = ("-date_created",)

#     def __str__(self) -> str:
#         return f"Payment: {self.amount}"

#     def save(self, *args, **kwargs) -> None:
#         while not self.ref:
#             ref = secrets.token_urlsafe(50)
#             object_with_similar_ref = Payment.objects.filter(ref=ref) 
#             if not object_with_similar_ref:
#                 self.ref = ref
#         super().save(*args, **kwargs)
    
#     def amount_value(self) -> int:
#         return self.amount *100

#     def verify_payment(self):
#         paystack = PayStack()
#         status, result = paystack.verify_payment(self.ref, self.amount)
#         if status:
#             if result['amount'] / 100 == self.amount:
#                 self.verified = True
#             self.save
#         if self.verified:
#             return True
#         return False