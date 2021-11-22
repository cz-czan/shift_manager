from django.core.management.base import BaseCommand, CommandError
from django.db.utils import IntegrityError
from shift_manager.models import Shift


class Command(BaseCommand):
    help = 'Creates shifts for the entire week, also retrospectively.'

    def handle(self, *args, **options):
        try:
            Shift.add_shifts_for_week()
        except IntegrityError:
            raise CommandError("Shifts already created for this week.")

