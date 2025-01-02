from django.db import models
from accounts.models import UserAccount
from ckeditor.fields import RichTextField

# Create your models here.

class BlogCategory(models.Model):
    category = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Blog Categories'

    def __str__(self):
        return self.category
    


class BlogModel(models.Model):

    title = models.CharField(max_length=255)
    blog_category = models.ForeignKey(BlogCategory, on_delete=models.CASCADE)
    author = models.ForeignKey(UserAccount, on_delete=models.PROTECT)
    blog_img = models.ImageField(upload_to='blog/images', blank=True, null=True)
    blog_thumb = models.ImageField(upload_to='blog/thumbnails', blank=True, null=True)
    blog_body = models.TextField()
    
    created_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(auto_now_add=True)

    def author_full_name(self):
        full_name = f'{self.author.first_name} {self.author.last_name}'
        return full_name
    

    def author_profile_pic(self):
        return self.author.profile_picture.url
    

    def __str__(self):
        return self.title
    

    
