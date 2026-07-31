from .register import register_view
from .login import user_login
from .logout import logout_view
from .password import (
    resetpass,
    passwordResetEmail,
    reset_password,
)
from .social_login import (
    google_login as social_login,
    github_login as social_login_callback,
)

password_reset = reset_password

__all__ = [
    'register_view',
    'resend_otp',
    'user_login',
    'logout_view',
    'resetpass',
    'passwordResetEmail',
    'password_reset',
    'social_login',
    'social_login_callback',
]
