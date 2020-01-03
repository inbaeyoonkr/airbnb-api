import random
from datetime import datetime
from django.core.management.base import BaseCommand
from django_seed import Seed
from rooms.models import Room, Photo
from users.models import User


class Seed(Seed):
    @classmethod
    def faker(cls, locale=None, codename=None):
        code = codename or cls.codename(locale)
        if code not in cls.fakers:
            from faker import Faker

            cls.fakers[code] = Faker(locale)
            cls.fakers[code].seed_instance(random.randint(1, 10000))
        return cls.fakers[code]


class Command(BaseCommand):
    help = "It seeds the DB with tons of stuff"

    def handle(self, *args, **options):
        user_seeder = Seed.seeder()
        user_seeder.add_entity(User, 20, {"is_staff": False, "is_superhost": False})
        user_seeder.execute()

        users = User.objects.all()
        room_seeder = Seed.seeder()
        room_seeder.add_entity(
            Room,
            150,
            {
                "user": lambda x: random.choice(users),
                "name": lambda x: room_seeder.faker.company(),
                "price": lambda x: random.randint(0, 300),
                "beds": lambda x: random.randint(0, 5),
                "bedrooms": lambda x: random.randint(0, 3),
                "bathrooms": lambda x: random.randint(0, 5),
                "check_in": lambda x: datetime.now(),
                "check_out": lambda x: datetime.now(),
                "instant_book": lambda x: random.choice([True, False]),
            },
        )
        room_seeder.execute()

        rooms = Room.objects.all()
        for room in rooms:
            for i in range(random.choice([5, 10])):
                Photo.objects.create(
                    caption=room_seeder.faker.sentence(),
                    room=room,
                    file=f"room_photos/{random.randint(1, 31)}.webp",
                )

        self.stdout.write(self.style.SUCCESS("Everything seeded"))
