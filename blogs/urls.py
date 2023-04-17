from django.contrib.auth.decorators import login_required
from django.urls import path

from .views import BlogCreateView, BlogDeleteView, BlogEditView, BlogView

urlpatterns = [
    path(
        "create/",
        login_required(
            BlogCreateView.as_view(), login_url="/auth/login?next=/blogs/create"
        ),
        name="blog-create",
    ),
    path("<pk>/<title>/", BlogView.as_view(), name="post"),
    path(
        "<pk>/<title>/edit/",
        login_required(
            BlogEditView.as_view(), login_url="/auth/login?next=/blogs/create"
        ),
        name="blog-edit",
    ),
    path(
        "<pk>/<title>/delete/",
        login_required(
            BlogDeleteView.as_view(), login_url="/auth/login?next=/blogs/create"
        ),
        name="blog-delete",
    ),
]
