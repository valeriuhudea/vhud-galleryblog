from django import forms
from .models import Comment


class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class' : 'share-form-name', 'placeholder': 'Type your message', 'style':'background-color: #ffffffa8'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class' : 'share-form-email', 'placeholder': 'Enter your email', 'style':'background-color: #ffffffa8'}))
    to = forms.EmailField(widget=forms.EmailInput(attrs={'class' : 'share-form-to', 'placeholder': 'Send to email', 'style':'background-color: #ffffffa8'}))
    comments = forms.CharField(required=False, widget=forms.Textarea(attrs={'class' : 'share-form-comm', 'placeholder': 'Type your message', 'rows': 5, 'style':'background-color: #ffffffa8'}))

class CommentForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class' : 'comment-name-form', 'placeholder': 'Enter your name'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class' : 'comment-form-email', 'placeholder': 'Enter your email address', 'style':'background-color: #ffffffa8'}))	
    comment = forms.CharField(widget=forms.Textarea(attrs={'class' : 'comment-form', 'placeholder': 'Type your comment', 'rows': 5, 'style':'background-color: #ffffffa8'}))	
    class Meta:
        model = Comment
        fields = ['name', 'email', 'comment']


class SearchForm(forms.Form):
    query = forms.CharField()
