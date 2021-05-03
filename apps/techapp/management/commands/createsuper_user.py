from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = 'Used to create a _custom_ superuser.'

    def add_arguments(self, parser):

        parser.add_argument('--user', default='admin',dest='username',)

        parser.add_argument('--password', )

        parser.add_argument('--email', help='e-mail address)')

    def _report_success(self, message):
        self.stdout.write(self.style.SUCCESS(message))

    def handle(self, *args, **option):
        username = option['username']
        password = option['password']
        email = option['email']

        User.objects.create_superuser(username=username,
                                      password=password,
                                      email=email)
        self._report_success('Superuser created successfully.')
