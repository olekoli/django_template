from django.forms.models import model_to_dict
from django.test import TestCase
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import check_password

from ..models import User
from .factories import UserFactory


class TestUserModel(TestCase):
    def setUp(self):
        self.user = model_to_dict(UserFactory.build())

    def create_regular_user(self) -> User:
        user = User.objects.create_user(
            email=self.user.get("email"), password=self.user.get("password")
        )
        self.assertIsInstance(user, User)
        return user

    def test_can_create_a_regular_user(self):
        self.create_regular_user()

    def test_create_user_hashes_password(self):
        user = self.create_regular_user()
        self.assertTrue(check_password(self.user.get("password"), user.password))

    def test_user_manager_validates_email(self):
        user_with_valid_email = self.create_regular_user()
        validate_email(user_with_valid_email.email)

        invalid_emails = ["abs@", "example@.com", "olek.com"]

        for invalid_email in invalid_emails:
            with self.assertRaises(
                ValidationError, msg=f"{invalid_email} has not been properly validated"
            ):
                User.objects.create_user(email=invalid_email)

    def test_username_is_same_as_email(self):
        user = self.create_regular_user()
        self.assertEqual(user.email, user.username)

    def test_default_user_is_not_stuff(self):
        user = self.create_regular_user()
        self.assertFalse(user.is_staff)

    def test_default_user_is_not_superuser(self):
        user = self.create_regular_user()
        self.assertFalse(user.is_superuser)

    def test_create_super_user_raises_an_error_with_wrong_params(self):
        with self.assertRaises(
            ValueError,
            msg="Create super user did not raise an error when is_staff is False",
        ):
            User.objects.create_superuser(
                email=self.user.get("email"),
                password=self.user.get("password"),
                is_staff=False,
            )

        with self.assertRaises(
            ValueError,
            msg="Create super user did not raise an error when is_superuser is False",
        ):
            User.objects.create_superuser(
                email=self.user.get("email"),
                password=self.user.get("password"),
                is_superuser=False,
            )

    def test_create_super_user_sets_default_params_when_none_are_given(self):
        super_user = User.objects.create_superuser(
            email=self.user.get("email"), password=self.user.get("password")
        )
        self.assertTrue(super_user.is_staff)
        self.assertTrue(super_user.is_superuser)
