from django.db import models
import datetime as dt
from django.core.exceptions import ValidationError
from django.db.models.signals import pre_save
from django.dispatch import receiver


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


# I'm using the pre_save signal for validation here, since django validators first of all don't run on save(), but only
# on form submissions, but besides, validators don't allow the us of non-static methods, and the Shift object instance
# context is needed to validate whether an employee already has a shift in a given day.
@receiver(pre_save, sender=Shift)
def validate_shift_assignment(sender, instance :Shift, *args, **kwargs):
    if instance.assigned_employee:
        # 0AM, the day where the assignment is attempted
        day_0am = dt.datetime(year=instance.time_from.year,
                              month=instance.time_from.month,
                              day=instance.time_from.day)

        next_day_0am = dt.datetime(year=instance.time_from.year,
                                   month=instance.time_from.month,
                                   day=instance.time_from.day +1)
        # The shifts from the day where the assignment is attempted
        days_shifts = [shift.assigned_employee for shift in Shift.objects.filter(time_from__gte=day_0am,
                                                                                 time_from__lt=next_day_0am)]
        if instance.assigned_employee in days_shifts:
            raise ValidationError("Employee already has a shift in the given day")


# Using signals here for the same reasons
@receiver(pre_save, sender=Shift)
def validate_shift_time(sender, instance :Shift, *args, **kwargs):
    if instance.time_to.hour % 8 != 0 or instance.time_from.hour % 8 != 0:
        raise ValidationError("Invalid shift start/end time. Shift can start/end at 8 hour intervals since 00:00 only.")
    elif (instance.time_to.second != 0 and instance.time_to.minute != 0) or\
            (instance.time_from.second != 0 and instance.time_from.minute != 0):
        raise ValidationError("Invalid shift start/end time. Shifts can only start at precise hours, that is XX:00:00.")