from django.urls import path, include
from rest_framework import routers
from shift_manager.views import *

router = routers.DefaultRouter()

router.register('employees', EmployeeViewSet)
router.register('shifts', ShiftViewSet)

urlpatterns = [
    path('api/', include(router.urls))
]
