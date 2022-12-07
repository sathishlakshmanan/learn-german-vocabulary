from django.shortcuts import render, redirect
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage

from .models import *
from .forms import VocabularyForm, RegisterUserForm
from .filters import VocabularyFilter
from .token import activate_account_token 


def index(request):

    all_vocabularies = CreateVocabulary.objects.all()
    word_count = all_vocabularies.count()
    der_count = all_vocabularies.filter(article="der").count()
    die_count = all_vocabularies.filter(article="die").count()
    das_count = all_vocabularies.filter(article="das").count()


    my_filter = VocabularyFilter(request.GET, queryset=all_vocabularies)
    all_vocabularies = my_filter.qs.order_by('word_de')
    
    paginator = Paginator(all_vocabularies, 20)
    page_number = request.GET.get('page')
    all_vocabularies = paginator.get_page(page_number)

    context = {
        "all_vocabularies": all_vocabularies,
        "word_count": word_count,
        "der_count": der_count,
        "die_count": die_count,
        "das_count": das_count,
        "my_filter": my_filter,
        "user": str(request.user),
        "AnonymousUser": "AnonymousUser"
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


def activate_account(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except:
        user = None

    if user is not None and activate_account_token.check_token(user, token):
        user.is_active = True
        user.save()

        messages.success(request, "Thank you for your confirmation. You can now login to your account.")
        return redirect('/login')
    else:
        messages.error(request, "Sorry, the link has expired!")

    return redirect('/')


def activate_mail(request, user, mail_id):
    subject = "Activate your Learn German Vocabulary account."
    message = render_to_string("activate_account.html", {
        'user': user.username,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': activate_account_token.make_token(user),
        "protocol": 'https' if request.is_secure() else 'http'
    })
    email = EmailMessage(subject, message, to=[mail_id])
    if email.send():
        messages.success(request, f"An activation link has been sent to {mail_id}. Please check your email!")
    else:
        messages.error(request, f"Problem sending email to {mail_id}. Please check if you typed your email correctly.")


def user_register(request):

    if request.user.is_authenticated:
        return redirect("/")

    else:
        register_form = RegisterUserForm()

        if request.method == "POST":
            register_form = RegisterUserForm(request.POST)
            if register_form.is_valid():
                user = register_form.save(commit=False)
                user.is_active=False
                user.save()
                activate_mail(request, user, register_form.cleaned_data.get('email'))
                #messages.success(request, "Your account was created successfully!")

                return redirect("/login")

        context = {"register_form": register_form}

        return render(request, "templates/register.html", context)


@login_required(login_url="user_login")
def account(request):

    # user = UserCreation.objects.get(id=pk) #working
    user = request.user
    total_words = CreateVocabulary.objects.filter(name=user).values('word_de').count()
    mail = user.email
    date_joined = user.date_joined

    context = {"user": user, "mail": mail, "date_joined": date_joined, "total_words": total_words}

    return render(request, "account.html", context)

    return render(request, "templates/create_vocabulary.html", context)


@login_required(login_url="user_login")
def add_vocabularies(request):

    VocabularyFormSet = inlineformset_factory(
        User,
        CreateVocabulary,
        fields=("article", "word_de", "word_en", "sentence"),
        extra=5,
    )

    user = request.user
    #user = CreateVocabulary.objects.get(id=username) 
    formset = VocabularyFormSet(queryset=CreateVocabulary.objects.none(), instance=user)

    if request.method == "POST":
        formset = VocabularyFormSet(request.POST, instance=user)
        if formset.is_valid():
            formset.save()
            return redirect("/my_vocabulary")

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
            return redirect("/my_vocabulary")
    context = {"form": form}

    return render(request, "templates/update_vocabulary.html", context)


@login_required(login_url="user_login")
def delete_vocabulary(request, pk):

    vocabulary = CreateVocabulary.objects.get(id=pk)

    if request.method == "POST":
        vocabulary.delete()
        return redirect("/my_vocabulary")

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

    user_id = user.id
    user_vocabularies = CreateVocabulary.objects.filter(name=user)

    context = {"user_vocabularies": user_vocabularies}

    return render(request, "templates/my_vocabulary.html", context)


def user(request, pk):

    #users = UserCreation.objects.get(id=pk) # working
    #data = users.createvocabulary_set.all() # working

    data = CreateVocabulary.objects.filter(name=pk) # working
    #data = users.objects.filter(name)
     
    #data = CreateVocabulary.objects.all()

    #context = {"users": users, "data": data}
    context = {"data": data, "pk":pk}

    return render(request, "templates/user.html", context)


@login_required(login_url="user_login")
def all_users(request):

    users = UserCreation.objects.all()
    context = {"users": users}

    return render(request, "templates/all_users.html", context)
