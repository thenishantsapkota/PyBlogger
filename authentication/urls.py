from django.contrib.auth.decorators import login_required
from django.urls import path

from .views import (
    ActivateView,
    LoginView,
    LogoutView,
    RegisterView,
    ResetPasswordView,
    ResetSuccessView,
)

urlpatterns = [
    path("register/", view=RegisterView.as_view(), name="register"),
    path("login/", view=LoginView.as_view(), name="login"),
    path("logout/", view=LogoutView.as_view(), name="logout"),
    path("activate/<uidb64>/<token>", view=ActivateView.as_view(), name="activate"),
    path("reset/<uidb64>/<token>", view=ResetSuccessView.as_view(), name="reset"),
    path("password-reset/", view=ResetPasswordView.as_view(), name="reset-password"),
]
