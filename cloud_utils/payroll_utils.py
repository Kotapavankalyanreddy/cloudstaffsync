from employees.models import Payroll

def add_or_update_payroll(user, month, year, staff_id, gross_pay, pf_amount, taxes, benefits):
    payroll, created = Payroll.objects.get_or_create(
        employee=user,
        month=month,
        year=year,
        staff_id=staff_id,
        defaults={
            'gross_pay': gross_pay,
            'pf_amount': pf_amount,
            'taxes': taxes,
            'benefits': benefits
        }
    )

    if not created:
        payroll.gross_pay = gross_pay
        payroll.pf_amount = pf_amount
        payroll.taxes = taxes
        payroll.benefits = benefits
        payroll.calculate_net_pay()
        payroll.save()
        return False, f"Payroll for {month} updated successfully!"
    else:
        return True, f"Payroll for {month} added successfully!"
