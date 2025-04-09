from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.apps import apps
from django.conf import settings

User = get_user_model()


class CustomUser(AbstractUser):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255, blank=True)
    email = models.EmailField(blank=True)
    staff_id = models.IntegerField(validators=[MaxValueValidator(9999999999)], default=0)
    Dob = models.DateField(null=True, blank=True)
    #mobile_no = models.CharField(max_length=10, validators=[validate_mobile_no], null=False, blank=True)
    address = models.CharField(max_length=255,blank=False, null=False)
    profile_pic = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

    ROLE_CHOICES = [
        ('staff', 'Staff'),
        ('management', 'Management'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='staff')
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_set',  # Unique related_name
        blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_permissions_set',  # Unique related_name
        blank=True
    )
    def __str__(self):
        return f"{self.user.username} - {self.role}"

    





def validate_mobile_no(value):
    if not value.isdigit() or len(value) != 10:
        raise ValidationError("Mobile number must be exactly 10 digits and contain only digits.")

class Attendance(models.Model):
    employee = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(max_length=20, choices=[('Present', 'Present'), ('Absent', 'Absent')])

    def __str__(self):
        return f"{self.employee.username} - {self.date} - {self.status}"

class Task(models.Model):
    employee = models.ForeignKey(User, on_delete=models.CASCADE)
    task_name = models.CharField(max_length=255)
    date = models.DateField()

    def __str__(self):
        return f"{self.task_name} - {self.date} - {self.employee.username}"

class ProfilePage(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    full_name = models.CharField(max_length=255, blank=True)
    email = models.EmailField(blank=True)
    role = models.CharField(max_length=100)
    staff_id = models.IntegerField(validators=[MaxValueValidator(9999999999)], default=0)
    Dob = models.DateField(null=True, blank=True)
    mobile_no = models.CharField(max_length=10, validators=[validate_mobile_no], null=False, blank=True)
    address = models.CharField(max_length=255,blank=False, null=False)
    profile_pic = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

    def __str__(self):
        return self.user.username

    class Meta:
        db_table = 'employees_profilepage'

class StaffProfilePage(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255, blank=True)
    email = models.EmailField(blank=True)
    staff_id = models.IntegerField(validators=[MaxValueValidator(9999999999)], default=0)
    Dob = models.DateField(null=True, blank=True)
    mobile_no = models.CharField(max_length=10, validators=[validate_mobile_no], null=False, blank=True)
    address = models.CharField(max_length=255,blank=False, null=False)
    profile_pic = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

    def __str__(self):
        return self.user.username

    class Meta:
        db_table = 'employees_staffprofilepage'






class StaffLeaveRequest(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    ]

    staff = models.ForeignKey(User, on_delete=models.CASCADE)
    reason = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.staff.username} - {self.status}"


class PerformanceReport(models.Model):
    employee = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.IntegerField()
    remarks = models.CharField(max_length=100)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.employee.username} - {self.score} - {self.date}"
    
    
    
class Payroll(models.Model):
    employee = models.ForeignKey(User, on_delete=models.CASCADE)
    month = models.CharField(max_length=20)  # Example: "March 2025"
    year = models.IntegerField()
    staff_id=models.IntegerField()
    gross_pay = models.DecimalField(max_digits=10, decimal_places=2)
    pf_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    taxes = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    benefits = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    net_pay = models.DecimalField(max_digits=10, decimal_places=2)

    def calculate_net_pay(self):
        """Calculate net pay based on deductions."""
        self.net_pay = self.gross_pay - (self.pf_amount + self.taxes + self.benefits)
        return self.net_pay

    def save(self, *args, **kwargs):
        """Automatically calculate net pay before saving."""
        self.calculate_net_pay()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Payroll for {self.employee.username} - {self.month}"




























if not apps.is_installed('employees'):
    raise LookupError("App 'employees' is not installed correctly.")