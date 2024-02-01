import random
import string

from apps.website.models import Room
from django.contrib.auth.models import User, Group


class ChatHelper:

    def __init__(self):
        self.a = 0

    def create_room(self, user):
        try:
            manager = random.choice(User.objects.filter(groups__id__in=Group.objects.filter(name='manager')))
            room_name = manager.username
            room_slug = self.generate_random_string()
            room = Room(name=room_name, slug=room_slug, client=user, manager=manager)
            room.save()
        except Exception as e:
            return -1
        return room

    def generate_random_string(self, length=20):
        letters = string.ascii_letters
        rand_string = ''.join(random.choice(letters) for i in range(length))
        return rand_string

