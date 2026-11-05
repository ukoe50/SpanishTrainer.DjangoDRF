
from django.contrib.auth.base_user import BaseUserManager

#
# MyUserManager (using Defaults)
#
class MyUserManager(BaseUserManager):
    def create_user(self, password):
        user = self.model()
        user.set_password(password)
        user.save(using=self._db)
        return user

#
# CustomUserManager
# that uses an email as the unique identifier instead of a username
#
# class CustomUserManager(BaseUserManager):
#     def create_user(self, email, password, **extra_fields):
#         if not email:
#             raise ValueError(_("The Email must be set"))
#         email = self.normalize_email(email)
#         user = self.model(email=email, **extra_fields)
#         user.set_password(password)
#         user.save()
#         return user