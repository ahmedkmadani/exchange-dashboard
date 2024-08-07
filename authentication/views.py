"""Module for handling user authentication."""
import logging

from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.generic import TemplateView

from web_project import TemplateLayout
from web_project.template_helpers.theme import TemplateHelper
from .form.login_form import LoginForm
from validators.validators import FileValidator

logger = logging.getLogger(__name__)



def LogoutView(request):
    # Log the user out
    logout(request)
    logger.debug(f"user logged out of the system")
    # Redirect to a specific URL after logging out (you can change this URL)
    return redirect(reverse("auth-login"))



class LoginView(TemplateView):
    """View for handling user login."""

    def get_context_data(self, **kwargs):
        """Initialize view context with a LoginForm and layout."""
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        form = LoginForm()
        context["form"] = form

        context.update(
            {"layout_path": TemplateHelper.set_layout("layout_blank.html", context)}
        )

        return context

    def post(self, request):
        """Handle POST requests, initializing a LoginForm with request data."""
        form = LoginForm(request.POST)
        if form.is_valid():
            phone_number = form.cleaned_data.get("phone_number")
            phone_number = FileValidator.arabic_to_english(phone_number)
            if phone_number.startswith("0"):
                phone_number = phone_number.lstrip("0")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=phone_number, password=password)
            if user is not None:
                if request.POST.get("remember_me"):
                    request.session.set_expiry(0)
                login(request, user)
                logger.debug("user %s: has logged in the system", phone_number)
                return redirect('index')
            form.add_error(None, _("Invalid phone number or password"))
        context = self.get_context_data()
        context["form"] = form
        return render(request, self.template_name, context)
