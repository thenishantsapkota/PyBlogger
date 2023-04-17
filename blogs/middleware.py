from django.shortcuts import redirect
from django.urls import reverse


class PreventLoginAndRegistrationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            if request.path_info in [reverse("login"), reverse("register")]:
                return redirect("home")

        response = self.get_response(request)

        return response
