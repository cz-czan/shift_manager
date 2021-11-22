from rest_framework import serializers
from shift_manager.models import *


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ['url', 'name']


class ShiftSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shift
        fields = ['url', 'assigned_employee', 'time_from', 'time_to']