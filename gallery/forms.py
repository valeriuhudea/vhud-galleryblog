from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import *
from django.utils.translation import gettext as _

class AlbumForm(forms.ModelForm):
    class Meta:
        model = Album
        exclude = []

    zip = forms.FileField(required=False)

class AlbumImageForm(forms.ModelForm):
    class Meta:
        model = AlbumImage
        exclude = []

    #zip = forms.FileField(required=False)

class ContactForm(forms.ModelForm):
    name=forms.CharField(required=True, max_length=50, widget=forms.TextInput(attrs={'class' : 'contact-form', 'placeholder': 'Enter your name'}))
    email=forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class' : 'contact-form', 'placeholder': 'Enter your email', 'style':'background-color: #ffffffa8'}))
    subject=forms.CharField(required=True, max_length=50, widget=forms.TextInput(attrs={'class' : 'contact-form', 'placeholder': 'Message subject'}))
    message=forms.CharField(required=True, max_length=2000, widget=forms.Textarea(attrs={'class' : 'contact-form', 'placeholder': 'Type your message', 'rows': 5, 'style':'background-color: #ffffffa8'}))
	
    class Meta:
      model = ClientMessage
	  
      fields = ['name', 'email', 'subject', 'message']
      help_texts = {'name': "Enter your name", 'email': "Enter your email", 'subject': "Message Subject", 'message': "Enter your message"}
	  
class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class' : 'registration-form-email', 'placeholder': 'Enter your email address', 'style':'background-color: #ffffffa8'}), label=_(u'Email*'))
    username = forms.CharField(max_length=36, widget=forms.TextInput(attrs={'class' : 'registration-form-username', 'placeholder': 'Enter your username'}), label=_(u'Username*'), help_text='*36 characters or fewer. Letters, digits and only this symbols: @/./+/-/_ ')
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class' : 'registration-form-fname', 'placeholder': 'Enter your first name'}), label=_(u'First Name*'))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class' : 'registration-form-lname', 'placeholder': 'Enter your last name'}), label=_(u'Last Name*'))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'class' : 'registration-form-p1', 'placeholder': 'Enter your password'}), label=_(u'Password*'), help_text="*Your password must contain at least 8 character, can't be a commonly used password and can't be entirely numeric.")
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'class' : 'registration-form-p2', 'placeholder': 'Repeat your password'}), label=_(u'Password confirmation*'), help_text='*Enter the same password, for verification.')
	
    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2'
        )

        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

#   def clean_email(self):
#        email = self.cleaned_data.get('email')
#        username = self.cleaned_data.get('username')
#        if email and User.objects.filter(email=email).exclude(username=username).exists():
#            raise forms.ValidationError(u'Email addresses must be unique.')
#        return email		

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']

        if commit:
            user.save()

        return User

class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)

    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'login-form', 'placeholder': 'Enter your username/email', 'id': 'login-form-u'}), label=_(u'Username'))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'login-form',
            'placeholder': 'Enter your password',
            'id': 'login-form-p',
        }
))
