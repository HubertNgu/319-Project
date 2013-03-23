from django.core.management.base import BaseCommand, CommandError
from survey_system import survey_mailer

class Command(BaseCommand):
    args = ''
    help = 'Email surveys to clients of the virtual deconstruction hub'

    def handle(self, *args, **options):
        survey_mailer.expire_and_mail_surveys()
        self.stdout.write('Successfully mailed surveys\n')
