from django.test import TestCase
from spanishtrainer_api.models import User
import random
import string

#
#
# run with >python manage.py test
#
#
class RegisterUserTestCase(TestCase):
    def setUp(self):
        self.random_username = ''.join(random.choices(string.ascii_letters, k=8))
        self.random_firstname = ''.join(random.choices(string.ascii_letters, k=6))
        self.random_lastname = ''.join(random.choices(string.ascii_letters, k=12))
        print(self.random_username)
        print(self.random_firstname)
        print(self.random_lastname)
        user1 = User.objects.create(
            username=self.random_username,
            email=self.random_username + "@email.com",
            first_name=self.random_firstname,
            last_name=self.random_lastname,
        )
        user1.set_password("Password123!")
        user1.save()
        print("user added created and saved:" + user1.username)

    def test_user_exists(self):
        print(self.random_username)
        user = User.objects.get(username=self.random_username)
        assert user is not None
        assert user.username == self.random_username