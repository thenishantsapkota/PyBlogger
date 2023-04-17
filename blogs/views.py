from django.contrib import messages
from django.shortcuts import redirect, render
from django.views import View

from .forms import BlogCreateForm
from .models import Post

# Create your views here.


class HomeView(View):
    def get(self, request):
        posts = Post.objects.all()
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
        return render(request, "blogs/blog.html")
