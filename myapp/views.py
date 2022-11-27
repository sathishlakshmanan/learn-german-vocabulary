from django.shortcuts import render, redirect
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import *
from .forms import VocabularyForm, RegisterUserForm
from .filters import VocabularyFilter


def index(request):

    all_vocabularies = CreateVocabulary.objects.all()
    word_count = all_vocabularies.count()
    der_count = all_vocabularies.filter(article="der").count()
    die_count = all_vocabularies.filter(article="die").count()
    das_count = all_vocabularies.filter(article="das").count()

    my_filter = VocabularyFilter(request.GET, queryset=all_vocabularies)
    all_vocabularies = my_filter.qs

    print(word_count, der_count)

    context = {
        "all_vocabularies": all_vocabularies,
        "word_count": word_count,
        "der_count": der_count,
        "die_count": die_count,
        "das_count": das_count,
        "my_filter": my_filter,
    }

    return render(request, "index.html", context)


def user_login(request):

    if request.user.is_authenticated:
        return redirect("/")

    else:
        if request.method == "POST":
            username = request.POST.get("username")
            password = request.POST.get("password")

            user = authenticate(request, username=username, password=password)

            if user:
                login(request, user)
                return redirect("/")
            else:
                messages.info(request, "The username or password is incorrect!")

        context = {}

        return render(request, "templates/login.html", context)


def user_logout(request):

    logout(request)

    return redirect("/login")


def user_register(request):

    if request.user.is_authenticated:
        return redirect("/")

    else:
        register_form = RegisterUserForm()

        if request.method == "POST":
            register_form = RegisterUserForm(request.POST)
            if register_form.is_valid():
                register_form.save()
                messages.success(request, "Your account was created successfully!")

                return redirect("/login")

        context = {"register_form": register_form}

        return render(request, "templates/register.html", context)


def account(request, pk):

    # user = UserCreation.objects.get(id=pk) #working
    user = request.user.id
    total_words = user.createvocabulary_set.all().count()
    context = {"user": user, "total_words": total_words}

    return render(request, "account.html", context)

    return render(request, "templates/create_vocabulary.html", context)


@login_required(login_url="user_login")
def add_vocabularies(request, pk):

    VocabularyFormSet = inlineformset_factory(
        UserCreation,
        CreateVocabulary,
        fields=("article", "word_de", "word_en", "sentence"),
        extra=5,
    )

    user = UserCreation.objects.get(id=pk) 
    formset = VocabularyFormSet(queryset=CreateVocabulary.objects.none(), instance=user)

    if request.method == "POST":
        formset = VocabularyFormSet(request.POST, instance=user)
        if formset.is_valid():
            formset.save()
            return redirect("/")

    context = {"formset": formset, "user": user}

    return render(request, "templates/create_vocabulary.html", context)


@login_required(login_url="user_login")
def update_vocabulary(request, pk):

    vocabulary = CreateVocabulary.objects.get(id=pk)
    form = VocabularyForm(instance=vocabulary)

    if request.method == "POST":
        form = VocabularyForm(request.POST, instance=vocabulary)
        if form.is_valid():
            form.save()
            return redirect("/")
    context = {"form": form}

    return render(request, "templates/create_vocabulary.html", context)


@login_required(login_url="user_login")
def delete_vocabulary(request, pk):

    vocabulary = CreateVocabulary.objects.get(id=pk)

    if request.method == "POST":
        vocabulary.delete()
        return redirect("/")

    context = {"vocabulary": vocabulary}

    return render(request, "templates/delete_vocabulary.html", context)


@login_required(login_url="user_login")
def delete_account(request, pk):

    user = UserCreation.objects.get(id=pk)

    if request.method == "POST":
        user.delete()
        return redirect("/")

    context = {"user": user}

    return render(request, "templates/delete_account.html", context)


@login_required(login_url="user_login")
def my_vocabulary(request):

    user = request.user
    print(user, user.id)

    return render(request, "templates/my_vocabulary.html")


def user(request, pk):

    #users = UserCreation.objects.get(id=pk) # working
    #data = users.createvocabulary_set.all() # working

    data = CreateVocabulary.objects.filter(name=pk) # working
    #data = users.objects.filter(name)
    print('PK: ', pk)
     
    #data = CreateVocabulary.objects.all()
    print('DATA: ', data)

    #context = {"users": users, "data": data}
    context = {"data": data, "pk":pk}

    return render(request, "templates/user.html", context)


@login_required(login_url="user_login")
def all_users(request):

    nnn = request.user.user_name
    print("NNNNNNNNNN:", nnn)

    users = UserCreation.objects.all()
    context = {"users": users}

    return render(request, "templates/all_users.html", context)
