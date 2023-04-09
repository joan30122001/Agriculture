from django.db import models
from ckeditor.fields import RichTextField






class Article(models.Model):
    author = models.ForeignKey("auth.User",on_delete = models.CASCADE)
    title = models.CharField(max_length = 50)
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
    comment_author = models.CharField(max_length = 50)
    comment_content = models.CharField(max_length = 200)
    comment_date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.comment_content
    class Meta:
        ordering = ['-comment_date']