from django.shortcuts import render, redirect
from django.views.generic import TemplateView

from authentication.form.login_form import LoginForm
from web_project import TemplateLayout
from web_project.template_helpers.theme import TemplateHelper

"""
This file is a view controller for multiple pages as a module.
Here you can override the page view layout.
Refer to auth/urls.py file for more pages.
"""


class AuthView(TemplateView):
    # Predefined function
    def get_context_data(self, **kwargs):
        # A function to init the global layout. It is defined in web_project/__init__.py file
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        form = LoginForm(self)
        # Update the context
        context.update(
            {
                "layout_path": TemplateHelper.set_layout("layout_blank.html", context),
                "form": form,
            }
        )

        return context

    def post(self, request, *args, **kwargs):
        return redirect("index")
