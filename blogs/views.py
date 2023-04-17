from django.contrib import messages
from django.shortcuts import redirect, render
from django.utils.text import slugify
from django.views import View

from .forms import BlogCreateForm
from .models import Post


class HomeView(View):
    def get(self, request):
        posts = Post.objects.all().order_by("-created_at")
        return render(request, "blogs/home.html", {"posts": posts})


class BlogCreateView(View):
    form = BlogCreateForm

    def get(self, request):
        form = self.form()
        return render(request, "blogs/create_blog.html", {"form": form})

    def post(self, request):
        form = self.form(request.POST)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.author = request.user
            blog.save()
            messages.success(request, "Blog created successfully!")
            return redirect("home")
        return render(request, "blogs/create_blog.html", {"form": form})


class BlogView(View):
    def get(self, request, pk, title):
        post = Post.objects.filter(id=pk)
        posts = Post.objects.all()
        if post.exists():
            return render(
                request,
                "blogs/blog.html",
                {
                    "post": post.first(),
                    "posts": posts,
                },
            )
        return render(request, "blogs/404.html", status=404)


class BlogEditView(View):
    form = BlogCreateForm

    def get(self, request, pk, title):
        post = Post.objects.filter(id=pk).first()
        if post and request.user == post.author:
            form = self.form(instance=post)
            return render(request, "blogs/create_blog.html", {"form": form})

        return render(request, "blogs/404.html", status=404)

    def post(self, request, pk, title):
        form = self.form(request.POST)
        post = Post.objects.filter(id=pk).first()
        if post and request.user == post.author and form.is_valid():
            post.title = form.data.get("title")
            post.content = form.data.get("content")
            post.save()
            return redirect("post", post.id, slugify(post.title))
        return render(request, "blogs/404.html", status=404)


class BlogDeleteView(View):
    def get(self, request, pk, title):
        post = Post.objects.filter(id=pk).first()
        if post and request.user == post.author:
            post.delete()
            messages.success(request, "Post deleted successfully!")
            return redirect("home")
        return render(request, "blogs/404.html", status=404)


def handler404(request, exception):
    return render(request, "blogs/404.html", status=404)
