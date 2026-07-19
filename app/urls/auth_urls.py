from django.urls import path

from app.views.auth.login import user_login
from app.views.auth.logout import logout_view
from app.views.auth.register import register_view
from app.views.auth.password import (
    forgot_password,
    reset_password,
    change_password,
    verify_reset_token,
    resend_reset_email,
)
from app.views.auth.social_login import (
    google_login,
    github_login,
)

urlpatterns = [
    path(
        "",
        user_login,
        name="login",
    ),
    path(
        "auth/logout/",
        logout_view,
        name="logout",
    ),
    path(
        "auth/register/",
        register_view,
        name="register",
    ),
    path(
        "auth/password/forgot/",
        forgot_password,
        name="forgot_password",
    ),
    path(
        "auth/password/reset/<uidb64>/<token>/",
        reset_password,
        name="reset_password",
    ),
    path(
        "auth/password/change/",
        change_password,
        name="change_password",
    ),
    path(
        "auth/password/verify/<uidb64>/<token>/",
        verify_reset_token,
        name="verify_reset_token",
    ),
    path(
        "auth/  password/resend/",
        resend_reset_email,
        name="resend_reset_email",
    ),
    path(
        "google/",
        google_login,
        name="google_login",
    ),
    path(
        "github/",
        github_login,
        name="github_login",
    ),
]