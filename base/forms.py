from django.forms import ModelForm
from .models import Post

class PostCreateForm(ModelForm):
    class Meta:
        model = Post
        fields = ['topic','title','body']          
class PostUpdateForm(ModelForm):
    class Meta:
        model = Post
        fields = ['topic','title','body']