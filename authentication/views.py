from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.db import transaction
from django.shortcuts import redirect, render
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.views import View

from .forms import LoginForm, PasswordResetForm, PasswordResetSuccessForm, RegisterForm
from .models import UsedPasswordResetToken
from .utils.helpers import activate_email, reset_email
from .utils.tokens import account_activation_token


class RegisterView(View):
    form = RegisterForm

    def get(self, request):
        form = self.form()
        return render(
            request,
            "authentication/register.html",
            context={"form": form},
        )

    @transaction.atomic
    def post(self, request):
        form = self.form(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            activate_email(request, user, form.data.get("email"))
            messages.success(request, "Registered successfully!")
            return redirect("login")

        return render(
            request,
            "authentication/register.html",
            context={"form": form},
        )


class LoginView(View):
    form = LoginForm

    def get(self, request):
        form = self.form()
        return render(request, "authentication/login.html", context={"form": form})

    def post(self, request):
        form = self.form(request.POST)
        if form.is_valid():
            username = form.data.get("username")
            password = form.data.get("password")
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "Logged in successfully!")
                return redirect("home")
            form.add_error("password", "Invalid username or password!")
        return render(request, "authentication/login.html", context={"form": form})


class LogoutView(View):
    def get(self, request):
        logout(request)
        messages.success(request, "Logged out successfully!")
        return redirect("home")


class ResetPasswordView(View):
    form = PasswordResetForm

    def get(self, request):
        form = self.form()
        return render(request, "authentication/reset.html", context={"form": form})

    def post(self, request):
        form = self.form(request.POST)
        if form.is_valid():
            User = get_user_model()
            email = form.data.get("email")
            user = User.objects.filter(email=email)
            if not user.exists():
                messages.error(request, "No user with the specified email found!")
                return redirect("login")
            reset_email(request, user.first(), email)
            return redirect("login")
        return render(request, "authentication/reset.html", {"form": form})


class ResetSuccessView(View):
    form = PasswordResetSuccessForm

    def get(self, request, uidb64, token):
        form = self.form()
        User = get_user_model()
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if UsedPasswordResetToken.objects.filter(user=user, token=token).exists():
            messages.error(request, "Invalid password reset link!")
            return redirect("login")

        if user is not None and account_activation_token.check_token(user, token):
            return render(
                request,
                "authentication/reset_password_success.html",
                {"form": form, "user": user},
            )
        else:
            messages.error(request, "Invalid password reset link!")
            return redirect("login")

    @transaction.atomic
    def post(self, request, uidb64, token):
        form = self.form(request.POST)
        if form.is_valid():
            User = get_user_model()
            try:
                uid = force_str(urlsafe_base64_decode(uidb64))
                user = User.objects.get(pk=uid)
            except (TypeError, ValueError, OverflowError, User.DoesNotExist):
                user = None
            password1 = form.data.get("password1")
            password2 = form.data.get("password2")
            if password1 != password2:
                form.add_error("password2", "Passwords donot match")
                return render(
                    request,
                    "authentication/reset_password_success.html",
                    {"form": form},
                )

            if UsedPasswordResetToken.objects.filter(user=user, token=token).exists():
                messages.error(request, "Invalid password reset link!")
                return redirect("login")
            else:
                UsedPasswordResetToken.objects.create(user=user, token=token)

            user.set_password(password1)
            user.save()
            messages.success(request, "Password reset successfully!")
            return redirect("login")
        return render(
            request, "authentication/password_reset_success.html", {"form": form}
        )


class ActivateView(View):
    def get(self, request, uidb64, token):
        User = get_user_model()
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()

            messages.success(
                request,
                "Thank you for your email confirmation. Now you can login your account.",
            )
            return redirect("login")
        else:
            messages.error(request, "Activation link is invalid!")
            return redirect("home")
