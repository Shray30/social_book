from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import Code, CustomUser, Book


class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = ("email", "public_visibility")


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ("email", "public_visibility")

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = {'title', 'author', 'book', 'description', 'visibility', 'cost', 'year_of_published'}
    
class CodeForm(forms.ModelForm):
    number = forms.CharField(label='Code', help_text='Enter SMS verification')
    
    class Meta:
        model = Code
        fields = ('number',)