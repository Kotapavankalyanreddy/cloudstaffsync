from employees.models import ProfilePage, StaffProfilePage
from django.contrib.auth.models import User

def get_or_create_profile(user):
    profile, created = ProfilePage.objects.get_or_create(
        user=user,
        defaults={
            'full_name': user.get_full_name(),
            'email': user.email,
            'staff_id': 00000,
            'address': 'Your Address Here',
            'mobile_no': '0000000000'
        }
    )
    return profile

def get_or_create_staff_profile(user):
    staff_profile, created = StaffProfilePage.objects.get_or_create(
        user=user,
        defaults={
            'full_name': user.get_full_name(),
            'email': user.email,
            'staff_id': 00000,
            'address': 'Your Address Here',
            'mobile_no': '0000000000'
        }
    )
    return staff_profile
