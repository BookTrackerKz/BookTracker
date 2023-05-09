# create_multiple_users.py
from users.models import User
from django.core.management.base import BaseCommand, CommandParser, CommandError
from django.utils.crypto import get_random_string
from datetime import date


class Command(BaseCommand):
    help = "Create admin user"

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument(
            "-p", "--password", type=str, help="Admin user password to be created"
        )

        parser.add_argument(
            "-e", "--email", type=str, help="Admin user email to be created"
        )

        parser.add_argument(
            "-u", "--username", type=str, help="Admin user name to be created"
        )

    def handle(self, *args: tuple, **options: dict):
        admin_username = options.get("username")
        if not admin_username:
            admin_username = "admin"

        admin_password = options.get("password")
        if not admin_password:
            admin_password = "admin1234"

        admin_email = options.get("email")
        if not admin_email:
            admin_email = f"{admin_username}@booktarcker.com"

        username = User.objects.filter(username=admin_username).first()
        if username:
            raise CommandError(f"Username `{admin_username}` already taken.")

        email = User.objects.filter(email=admin_email).first()
        if email:
            raise CommandError(f"Email `{admin_email}` already taken.")

        admin_cleared_date = date.today()

        User.objects.create_superuser(
            username=admin_username,
            password=admin_password,
            email=admin_email,
            cleared_date=admin_cleared_date,
        )
        self.stdout.write(
            self.style.SUCCESS("Admin `%s` successfully created!" % admin_username)
        )
