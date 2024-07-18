from django.urls import path
from .views import AuthView


urlpatterns = [
    path(
        "",
        AuthView.as_view(template_name="auth_login.html"),
        name="auth-login",
    )
]
