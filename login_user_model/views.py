from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse

from .models import *
from django.core.mail import EmailMessage
from .token import account_activation_token
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from django.template.loader import render_to_string
from django.core.mail import send_mail

from django.contrib.auth import get_user_model
User = get_user_model()


def index(request):
    return render(request, 'login_user_model/register.html')


def user_login(request):
    if request.user.is_authenticated:
        return redirect('login_user_model:success')

    if request.method == "POST":
        username = request.POST['username']
        print('i am', username)
        password = request.POST['password']
        user = authenticate(request, email=username, password=password)
        print('i am ', user)
        if user:
            login(request, user)
            return redirect('login_user_model:success')
    else:
        return render(request, 'login_user_model/login.html')


def user_logout(request):
    if request.method == "POST":
        logout(request)
        return redirect('login_user_model:login')


def success(request):
    context = {}
    context['user'] = request.user
    return render(request, 'login_user_model/success.html', context)


def registration(request):
    if request.method == 'POST':
        context = {}
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        c_password = request.POST['c_password']

        if password != c_password:
            context['error'] = 'Password did not match'
            return render(request, 'login_user_model/login.html', context)

        elif UserData.objects.filter(username=username).exists():
            print(username)
            context['user_exist'] = 'Username Already Taken'
            return render(request, 'login_user_model/login.html', context)

        elif User.objects.filter(email=email).exists():
            print(email)
            context['email_exist'] = 'Email Already Taken'
            return render(request, 'login_user_model/login.html', context)
        else:
            user = UserData.objects.create_user(username=username, email=email, password=password)
            print('done')
            user.is_staff = False
            user.is_active = False
            user.save()

            current_site = get_current_site(request)
            mail_subject = 'Activate your  account.'

            message = render_to_string('login_user_model/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })

            email1 = EmailMessage(
                mail_subject, message, to=[email]
            )
            email1.send()
            return HttpResponse('Please confirm your email address to complete the registration')

    return redirect('login_user_model:login')

def activate(request, uidb64, token,backend='django.contrib.auth.backends.ModelBackend'):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = UserData.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user,backend='django.contrib.auth.backends.ModelBackend')
        # return redirect('home')
        return redirect('login_user_model:success')
    else:
        return HttpResponse('Activation link is invalid!')

def send_email(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        send_mail('subject goes here', 'message goes here', 'kamleshkumarbca92@gmail.com', [email], fail_silently=False)

        return HttpResponse('mail sent to :' + email)
    return render(request, 'login_user_model/send_email.html')
