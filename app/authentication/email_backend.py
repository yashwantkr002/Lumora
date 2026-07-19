import logging
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import AbstractBaseUser
from django.http import HttpRequest
from typing import Optional
from app.models.user import CustomUser
logger = logging.getLogger(__name__)

class EmailBackend(ModelBackend):
    """
    Custom authentication backend that allows users to authenticate using 
    their email address instead of a username.
    """

    def authenticate(
        self, 
        request: Optional[HttpRequest], 
        username: Optional[str] = None, 
        password: Optional[str] = None, 
        **kwargs
    ) -> Optional[AbstractBaseUser]:
        """
        Validates the user using email and password.
        Note: Django's authenticate() method passes the identifier as 'username' 
        even if the form field is named 'email'.
        """
        # अगर यूजरनेम (ईमेल) या पासवर्ड गायब है, तो सीधे वापस जाओ
        email = username or kwargs.get("email")
        if not email or not password:
            return None

        try:
            # ईमेल केस-इन्सेंसिटिव होना चाहिए (FAANG Standard)
            user = CustomUser.objects.get(email__iexact=email)
        except CustomUser.DoesNotExist:
            # Security: Timing attack से बचने के लिए, यूजर न मिलने पर भी 
            # एक डमी पासवर्ड हैश चेक रन होना चाहिए ताकि अटैकर टाइमिंग डिफरेंस से ईमेल का पता न लगा सके।
            CustomUser().set_password(password)
            return None
        except Exception as e:
            logger.error(f"Unexpected error during email authentication lookup: {str(e)}")
            return None

        # पासवर्ड चेक करो और सुनिश्चित करो कि यूजर एक्टिव है
        if user.check_password(password) and self.user_can_authenticate(user):
            return user
            
        return None

    def get_user(self, user_id: int) -> Optional[AbstractBaseUser]:
        """
        Retrieves the user instance from the database using the user_id session token.
        Required by Django session framework.
        """
        try:
            return CustomUser.objects.get(pk=user_id)
        except CustomUser.DoesNotExist:
            return None