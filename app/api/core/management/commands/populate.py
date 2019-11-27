from django.core.management.base import BaseCommand
import random
from faker import Faker
from api.users.models import User
from api.cases.models import Case, Stadia

class Command(BaseCommand):
    help = 'Populate with fake data'
    fake = Faker('nl_NL')

    def create_cases(self):
        for i in range(100):
            address = self.fake.street_address()
            postal_code = self.fake.postcode()
            stadium_code = random.choice([tag.name for tag in Stadia])
            case = Case.objects.create(address=address, postal_code=postal_code, stadium_code=stadium_code)
            case.save()

    def create_users(self):
        users = []
        for i in range(20):
            profile = self.fake.profile()
            email = profile['mail']
            password = 'demo_demo'
            name = profile['name'].split(' ')
            kwargs = {'first_name': name[0], 'last_name': ' '.join(name[1:])}
            user = User.objects.create_user(email, password, **kwargs)
            users.append(user)
        return users

    def create_itineraries(self, users):
        for user in users:
            print(user)

    def handle(self, *args, **kwargs):
        # users = self.create_users()
        # self.create_itineraries(users)
        self.create_cases()
