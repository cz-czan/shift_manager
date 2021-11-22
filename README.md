Django web-app written for a recruitation at TeamWay. 

## Setup
Install django and DRF:
```shell
pip install django djangorestframework 
```
Start a django project
```shell
django-admin startproject <project-name>
```
Move the `shift_manager` directory to the project root.

Add the app and DRF to `INSTALLED_APPS` in the project's ``settings.py``:
```python
INSTALLED_APPS = [
    ...
    'shift_manager',
    'rest_framework'
]
```
Set the default permissions classes in `settings.py` as follows ( paste at the bottom of the file ):
```python
REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ]
}
```

Make migrations and then migrate:
```shell
python manage.py makemigrations
python manage.py migrate
```

Add the app's `urlpatterns` to the project's `urls.py` as follows:
```python
urlpatterns = [
    ...
    path('', include(shift_manager.urls))
]
```
## Usage
Run the development server at `localhost:8000`:
```shell
python manage.py runserver
```

Shifts are available under the `/api/shifts/` endpoint, employees under `/api/employees/`

Use this command:
```shell
python manage.py create_shifts_for_week.py
```
or simply send a `GET` request to `/api/shifts/`
to create and save to the database all the shifts for this week.

Send a `PUT` request to the shift endpoint to assign an employee to a shift, referencing the employee by their `id` field.


