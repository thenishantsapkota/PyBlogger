from django import forms

from blogs.models import Post


class BlogCreateForm(forms.ModelForm):
    title = forms.CharField(
        max_length=255,
        widget=forms.TextInput(
            {"class": "input", "placeholder": "Enter your blog title"}
        ),
    )

    content = forms.CharField(
        max_length=2500,
        widget=forms.Textarea(
            {
                "class": "textarea",
                "placeholder": "Enter your content",
                "style": "height:364px;",
                "id": "markdown-input",
            }
        ),
    )

    class Meta:
        model = Post
        fields = ("title", "content")
