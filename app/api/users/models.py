import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models
from api.users.user_manager import UserManager
from api.users.utils import generate_username

class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(
        unique=True,
        blank=False,
        error_messages={
            'unique': "A user with that email already exists.",
        },
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def get_last_name_from_email(self):
        '''
        Parses and returns last name from email (f.foo will return foo)
        '''
        if self.email:
            split_email_username = self.email.split('@')[0].split('.')
            if len(split_email_username) == 2:
                last_name = split_email_username[1]
                last_name = last_name.capitalize()
                return last_name

    @property
    def full_name(self):
        last_name = self.last_name

        if not last_name:
            last_name = self.get_last_name_from_email()
            print('\033[91m HELLO', last_name)

        last_name = '' if last_name is None else last_name

        return '{} {}'.format(self.first_name, last_name)

    def __str__(self):
        return self.full_name

    def save(self, *args, **kwargs):
        self.username = generate_username(self.email)
        super().save(*args, **kwargs)
