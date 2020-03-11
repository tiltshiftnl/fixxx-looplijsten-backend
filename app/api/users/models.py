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

    @property
    def full_name(self):
        '''
        Parses and returns last name from email (f.foo will return F. Foo)
        '''
        if self.email:
            full_name = self.email.split('@')[0].split('.')
            processed_full_name = ''

            for part in full_name:
                part = part.capitalize()

                if len(part) == 1:
                    part = part + '.'

                processed_full_name = processed_full_name + ' ' + part

            return processed_full_name

    def __str__(self):
        return self.full_name

    def save(self, *args, **kwargs):
        self.username = generate_username(self.email)
        super().save(*args, **kwargs)
