from django.contrib.auth import views as auth_views
from django.views import generic
from django.urls import reverse_lazy
from django.core.mail import send_mail
from .forms import RegisterForm, NewPasswordForm, OTPVerificationForm, SendOTPForm
from django.shortcuts import redirect, render
from django.contrib import messages
from random import randint
from django.conf import settings
from django.contrib.auth import login, get_user_model, update_session_auth_hash
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

User = get_user_model()
class LoginView(auth_views.LoginView):
    template_name = 'accounts/login.html'


class RegisterView(generic.CreateView):
    form_class = RegisterForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('accounts:login')

class HomeView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'accounts/index.html'


def send_otp(request):
    if request.method == 'POST':
        form = SendOTPForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            user = User.objects.get(email=email)
            if user:
                otp = get_otp()
                user.otp = otp
                user.save()
                subject = 'password resetting OTP'
                message = otp
                send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email])
                return redirect('accounts:otp_verification')
        else:
            messages.error(request, 'Account does not exist for this mail')
    else:
        form = SendOTPForm()
    return render(request, 'accounts/send_otp.html', {'form': form})

def otp_verification(request):
    if request.method == 'POST':
        form = OTPVerificationForm(request.POST)
        if form.is_valid():
            otp = form.cleaned_data.get('otp')
            if User.objects.filter(otp=otp).exists():
                user = User.objects.get(otp=otp)
                user.otp = get_otp()
                user.save()
                login(request, user)
                return redirect('accounts:new_password')
            else:
                messages.error(request, 'you entered the wrong otp')
    else:
        form = OTPVerificationForm()
    return render(request, 'accounts/otp_verification.html', {'form': form})

@login_required
def user_change_password_view(request):
    form = NewPasswordForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            password1 = form.cleaned_data.get('new_password1')
            password2 = form.cleaned_data.get('new_password2')
            if password1 == password2:
                user = request.user
                user.set_password(password1)
                user.save()
                update_session_auth_hash(request, user)
                return redirect('accounts:login')
            else:
                messages.error(request, 'your password doesnt match')

    else:
        form = NewPasswordForm(request.POST or None)
    template = 'accounts/change_password.html'
    context = {
        'form' : form
    }
    return render(request, template, context)


def get_otp():
    digit = randint(000000, 999999)
    otp = '{}'.format(digit)
    return otp
