from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm

from .models import *

def index(request):
    
    all_vocabularies = CreateVocabulary.objects.all()

    return render(request, 'index.html', {'all_vocabularies': all_vocabularies})

def register(request):

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            # return redirect('login_url')

    else:
        form = UserCreationForm()
    context = { 
        'form':form
    }

    return render(request, 'register.html', context)

def vocabularies(request):
    
    #all_vocabs = VocabularyCreation.objects.all()

    #context = {'all_vocabs':all_vocabs}
    
    return render(request, 'templates/vocabularies.html')
