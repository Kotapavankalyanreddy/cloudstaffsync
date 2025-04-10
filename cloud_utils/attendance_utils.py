from employees.models import Attendance

def create_or_warn_attendance(staff_id, date, status):
    if Attendance.objects.filter(staff_id=staff_id, date=date, status=status).exists():
        return False, "Attendance for this date already exists!"
    else:
        Attendance.objects.create(staff_id=staff_id, date=date, status=status)
        return True, "Attendance added successfully!"
