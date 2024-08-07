from django.urls import path
from .views import LoginView, LogoutView

urlpatterns = [
    path(
        "",
        LoginView.as_view(template_name="auth_login.html"),
        name="auth-login",
    ),
    path('logout/', LogoutView, name='logout'),

]
