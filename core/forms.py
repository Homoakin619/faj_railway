from pyexpat import model
from django import forms
from ckeditor.widgets import CKEditorWidget
from .models import Post, Profile

class CreatePostForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    content = forms.CharField(widget=CKEditorWidget())
    image = forms.ImageField(required=False,widget=forms.ClearableFileInput(attrs={'class':'form-control'}))
    video_link = title = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))

    class Meta:
        model = Post
        fields = ['title','content','image','video_link']

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('verified',)
