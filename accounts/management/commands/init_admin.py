import os
from django.core.management.base import BaseCommand
from accounts.models import CustomUser

class Command(BaseCommand):
    help = "Initializes the default admin superuser if not present."

    def handle(self, *args, **options):
        username = os.environ.get("ADMIN_USERNAME", "admin")
        email = os.environ.get("ADMIN_EMAIL", "admin@fenixitmall.com")
        password = os.environ.get("ADMIN_PASSWORD", "admin123")

        user, created = CustomUser.objects.get_or_create(
            username=username,
            defaults={
                "email": email,
                "role": "admin",
                "is_staff": True,
                "is_superuser": True,
            }
        )

        if created:
            user.set_password(password)
            user.save()
            self.stdout.write(self.style.SUCCESS(f"Successfully created admin user: {username}"))
        else:
            if not user.is_superuser or not user.is_staff:
                user.is_superuser = True
                user.is_staff = True
                user.role = "admin"
                user.save()
            self.stdout.write(self.style.WARNING(f"Admin user already exists: {username}"))
