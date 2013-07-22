from dirapp.models import UserProfile
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
import names
from loremipsum import get_sentence
from random import randint


class Command(BaseCommand):
    help = 'Import dummy data into database'

    def handle(self, *args, **options):
        for i in range(1,100):  # Will create 100 sample users with profile
            self.create_sample_user(count=i)

    def create_sample_user(self, count):
        firstname = names.get_first_name()
        lastname = names.get_last_name()
        username = firstname[0].lower() + lastname.lower()
        email = username + '@dir.app'
        password = username
        address = get_sentence()[0:50]
        phone = '+' + str(randint(100,999)) + '-' + str(randint(100000000,999999999))
        user = User.objects.create_user(username=username, email=email, password=password)
        user.first_name = firstname
        user.last_name = lastname
        user.save()
        profile = UserProfile.objects.create(user=user, Address=address, Phone=phone,)
        profile.save()
        print "Creating user %i" % count
