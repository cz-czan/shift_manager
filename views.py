from rest_framework import viewsets
from rest_framework import permissions
from shift_manager.models import Shift
from rest_framework.response import Response
from shift_manager.serializers import *
from django.http import HttpRequest

class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all().order_by('id')
    serializer_class = EmployeeSerializer
    permission_classes = [permissions.AllowAny]


class ShiftViewSet(viewsets.ModelViewSet):
    queryset = Shift.objects.all()
    serializer_class = ShiftSerializer
    permission_classes = [permissions.AllowAny]

    def list(self, request, *args, **kwargs):
        shifts = Shift.objects.all()
        now = dt.datetime.now()
        # Resetting the time to 00:00:00
        now = dt.datetime(year=now.year, month=now.month, day=now.day)

        if now not in [shift.time_from for shift in shifts]:
            Shift.add_shifts_for_week()

        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)