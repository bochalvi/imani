from django.views.generic import ListView, DetailView
from django.views.generic import ListView
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import EmailMessage
from django.views.generic import CreateView, DetailView
from .models import Invitation
from .models import PasswordReset  # Import PasswordReset model
from django.urls import reverse_lazy, reverse
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.decorators import login_required

from .models import Member

from django.conf import settings
from django.http import HttpResponse  # Add this import
from django.template import loader  # Add this import
from django.utils.http import url_has_allowed_host_and_scheme  # Moved import here
# Create your views here.


def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'users/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            next_url = request.POST.get("next")
            if next_url and url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
                return redirect(next_url)
            else:
                # Redirect to home if next is not valid
                return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'users/login.html', {'form': form})


def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('users:login')
    return render(request, 'users/login.html')


class CreateInviteView(LoginRequiredMixin, CreateView):
    model = Invitation
    fields = ['email']  # Optional: Let inviters specify an email
    template_name = 'invite/create_invite.html'
    success_url = reverse_lazy('invite_success')

    def form_valid(self, form):
        form.instance.inviter = self.request.user
        form.instance.expires_at = timezone.now() + timedelta(days=3)  # 3-day expiration
        return super().form_valid(form)


class SignUpView(CreateView):
    form_class = UserCreationForm  # Or a custom form
    template_name = 'registration/signup.html'

    def dispatch(self, request, *args, **kwargs):
        # Validate the invite token from the URL
        token = kwargs.get('token')
        self.invite = get_object_or_404(
            Invitation, token=token, is_used=False, expires_at__gte=timezone.now())
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        # Save the user and mark the invite as used
        user = form.save()
        self.invite.is_used = True
        self.invite.save()
        return redirect('login')  # Redirect to login after signup


def ForgotPassword(request):
    if request.method == 'POST':
        email = request.POST.get('email')

        # verify if email exists
        try:
            user = User.objects.get(email=email)
            # create a new reset id
            new_password_reset = PasswordReset(user=user)
            new_password_reset.save()

        # creat password reset ur;
            password_reset_url = reverse(
                'users:reset-password', kwargs={'reset_id': new_password_reset.reset_id})
            full_password_reset_url = f'{request.scheme}://{request.get_host()}{password_reset_url}'
        # email content
            email_body = f'Reset your password using the link below:\n\n\n{full_password_reset_url}',

            email_message = EmailMessage(
                'Reset your password',  # email subject
                email_body,
                settings.EMAIL_HOST_USER,  # email sender
                [email]  # email  receiver
            )

            email_message.fail_silently = True
            email_message.send()

            return redirect('password-reset-sent', reset_id=new_password_reset.reset_id)

        except User.DoesNotExist:
            messages.error(request, f"No user with email '{email}' found")
            return redirect('forgot-password')

    return render(request, 'users/forgot_password.html')


def PasswordResetSent(request, reset_id):

    if PasswordReset.objects.filter(reset_id=reset_id).exists():
        return render(request, 'password_reset_sent.html')
    else:
        # redirect to forgot password page if code does not exist
        messages.error(request, 'Invalid reset id')
        return redirect('forgot-password')


def ResetPassword(request, reset_id):

    try:
        password_reset_id = PasswordReset.objects.get(reset_id=reset_id)

        if request.method == 'POST':
            password = request.POST.get('password')
            confirm_password = request.POST.get('confirm_password')

            passwords_have_error = False

            if password != confirm_password:
                passwords_have_error = True
                messages.error(request, 'Passwords do not match')

            if len(password) < 5:
                passwords_have_error = True
                messages.error(
                    request, 'Password must be at least 5 characters long')

            expiration_time = password_reset_id.created_when + \
                timezone.timedelta(minutes=10)

            if timezone.now() > expiration_time:
                passwords_have_error = True
                messages.error(request, 'Reset link has expired')

                reset_id.delete()

            if not passwords_have_error:
                user = reset_id.user
                user.set_password(password)
                user.save()

                # delete reset id after use
                reset_id.delete()

                # redirect to login
                messages.success(request, 'Password reset. Proceed to login')
                return redirect('login')
            else:
                # redirect back to password reset page and display errors
                return redirect('reset-password', reset_id=reset_id)

    except PasswordReset.DoesNotExist:

        # redirect to forgot password page if code does not exist
        messages.error(request, 'Invalid reset id')
        return redirect('forgot-password')

    return render(request, 'users/reset_password.html')


def loan(request):
    mymembers = Member.objects.all().values()
    context = {
        'mymembers': mymembers,
        'mymembers_count': Member.objects.count(),
    }
    template = loader.get_template('users/loan.html')
    return HttpResponse(template.render(context, request))


def get_form_kwargs(self):
    kwargs = super().get_form_kwargs()
    if 'member_id' in self.kwargs:  # If coming from a member detail page
        kwargs['initial'] = {'user': self.kwargs['member_id']}
    return kwargs
