from app.services.auth import (
    AuthenticationService,
    RegistrationService,
    PasswordService,
    OTPService,
    SocialAuthService,
)


class AuthService:
    """
    Compatibility wrapper for the auth service layer.
    """

    @staticmethod
    def register(cleaned_data, files):
        form = type("RegistrationForm", (), {"cleaned_data": cleaned_data, "files": files})()
        return RegistrationService.register_user(form)

    send_password_reset_email = staticmethod(PasswordService.send_password_reset_email)
    reset_password = staticmethod(PasswordService.reset_password)
    change_password = staticmethod(PasswordService.change_password)
    verify_token = staticmethod(PasswordService.verify_token)
    login_user = staticmethod(AuthenticationService.login_user)
    logout_user = staticmethod(AuthenticationService.logout_user)
    send_otp = staticmethod(OTPService.generate_otp)
    verify_otp = staticmethod(OTPService.verify_otp)
    handle_social_login = staticmethod(SocialAuthService.initialize_social_user)
