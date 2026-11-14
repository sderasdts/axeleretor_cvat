from django.core.management.base import BaseCommand, CommandError
from django.db import connection
from django.db.utils import OperationalError


class Command(BaseCommand):
    help = "Проверить подключение к базе данных и вывести параметры подключения"

    def handle(self, *args, **options):
        s = connection.settings_dict
        self.stdout.write(f"Подключаюсь к {s['USER']}@{s['HOST']}:{s['PORT']}/{s['NAME']} ...")
        try:
            with connection.cursor() as cur:
                cur.execute("SELECT version(), current_database(), current_user")
                version, db, user = cur.fetchone()
        except OperationalError as e:
            raise CommandError(f"Не удалось подключиться к БД: {e}")
        self.stdout.write(self.style.SUCCESS("OK: подключение к БД работает"))
        self.stdout.write(f"  база: {db}, пользователь: {user}")
        self.stdout.write(f"  сервер: {version}")
