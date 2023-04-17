from django.contrib.auth.decorators import login_required
from django.urls import path

from .views import BlogCreateView, BlogView

urlpatterns = [
    path(
        "create/",
        login_required(
            BlogCreateView.as_view(), login_url="/auth/login?next=/blogs/create"
        ),
        name="blog-create",
    ),
    path("<pk>/<title>/", BlogView.as_view(), name="post"),
]
