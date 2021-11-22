from django.test import TestCase
from rest_framework.test import APIClient
from django.core.exceptions import ValidationError
from shift_manager.models import *


class Test(TestCase):

    # The test database starts off empty, and it should be filled out with shifts after a GET request is sent and the
    # overriden list() viewset method is called
    def test_auto_shift_creation(self):
        self.assertTrue(not Shift.objects.all())
        client = APIClient()
        client.get('/api/shifts/')
        # Assert the queryset is not empty after the GET request
        self.assertTrue(Shift.objects.all())

    # Ensure validation error is raised if employee is assigned over 1 shift per day.
    def test_employee_shifts(self):
        Shift.add_shifts_for_week()
        shifts = Shift.objects.all()[0:2]
        employee = Employee(name='John Doeson')
        employee.save()
        with self.assertRaises(ValidationError):
            for shift in shifts:
                shift.assigned_employee = employee
                shift.save()

    # Ensure a validation error is raised if shift time is set improperly.
    def test_shift_time_validation(self):
        invalid_shifts = [Shift(time_from=dt.datetime(year=2021, month=11, day=13, hour=5),
                                time_to=dt.datetime(year=2021, month=11, day=13, hour=5)),
                          Shift(time_from=dt.datetime(year=2021, month=11, day=13, hour=8, minute=4),
                                time_to=dt.datetime(year=2021, month=11, day=13, hour=8, minute=4)),
                          Shift(time_from=dt.datetime(year=2021, month=11, day=13, hour=8, second=5),
                                time_to=dt.datetime(year=2021, month=11, day=13, hour=8, second=5))]

        with self.assertRaises(ValidationError):
            for shift in invalid_shifts:
                shift.save()


