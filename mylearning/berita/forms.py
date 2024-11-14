from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'category']


class SignUpForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput(), label='Password')
    password2 = forms.CharField(widget=forms.PasswordInput(), label='Konfirmasi Password')

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email']
        
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError(email + " sudah digunakan.")
        return email
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise ValidationError(username + " sudah digunakan.")
        return username
    
    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Password tidak cocok.")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user
    
# class SignUpForm(UserCreationForm):
#     email = forms.EmailField(max_length=200, help_text='Required')

#     class Meta:
#         model = User
#         fields = ['username', 'email', 'password1', 'password2']

#         def save(self, commit=True):
#             User = super(SignUpForm, self).save(commit=False)
#             User.email = self.cleaned_data['email']
#             if commit:
#                 User.save()
#             return User

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3, 'placeholder': 'komentar anda..'})
        }
        
        
class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['fullname', 'email', 'message']
        
        
class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }