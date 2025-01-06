from django import forms
from ckeditor.widgets import CKEditorWidget
from blog.models import BlogModel


class BlogPostForm(forms.ModelForm):
    
    blog_body = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = BlogModel
        fields = ['title', 'blog_category', 'blog_img', 'blog_thumb', 'blog_body']

    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].required = True
        self.fields['blog_category'].required = True
        self.fields['blog_img'].required = True
        self.fields['blog_thumb'].required = True
        self.fields['blog_body'].required = True










class UpdateBlogForm(forms.ModelForm):
    
    blog_body = forms.CharField(widget=CKEditorWidget())

    class Meta():
        model = BlogModel
        fields = ['title', 'blog_category', 'blog_img', 'blog_thumb', 'blog_body']
        exclude = ['author']




        