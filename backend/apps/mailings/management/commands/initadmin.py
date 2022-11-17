from django.contrib.auth.models import User
from django.core.management import BaseCommand



class Command(BaseCommand):
    help = 'Создает админа (root:root)'
    def handle(self, *args, **options):
        """Создает админа, если в БД нет ни одного user(is_superuser=True)"""

        if not User.objects.filter(is_superuser=True):
            User.objects.create_superuser(
                username='root',
                password='12345',
            )
        self.stdout.write(self.style.SUCCESS("Админ создан!"))