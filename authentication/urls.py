from django.urls import path
from .views import LoginView


urlpatterns = [
    path(
        "",
        LoginView.as_view(template_name="auth_login.html"),
        name="auth-login",
    )
]
