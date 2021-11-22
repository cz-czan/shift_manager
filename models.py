from django.db import models
import datetime as dt


class Employee(models.Model):
    name = models.TextField()


class Shift(models.Model):
    assigned_employee = models.ForeignKey(Employee, null=True, blank=True, on_delete=models.CASCADE)
    time_from = models.DateTimeField(unique=True)
    time_to = models.DateTimeField(unique=True)

    @classmethod
    def add_shifts_for_week(cls):
        now = dt.datetime.now()
        monday = now - dt.timedelta(days=now.weekday())
        # Resetting the time to 00:00:00
        monday = dt.datetime(year=monday.year, month=monday.month, day=monday.day)
        for i in range(0, 7):
            day = monday + dt.timedelta(days=i)
            for hour_from in (0, 8, 16):
                time_from = day + dt.timedelta(hours=hour_from)
                time_to = day + dt.timedelta(hours=hour_from + 8)

                shift = Shift(time_from=time_from, time_to=time_to)
                shift.save()

