from django.forms import ModelForm
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import CreateVocabulary


class VocabularyForm(ModelForm):
    class Meta:
        model = CreateVocabulary
        fields = "__all__"
        # fields = ['article', 'word_de', 'word_en', 'sentence']


class RegisterUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]
