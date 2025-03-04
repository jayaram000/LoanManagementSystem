from django.db import models
from django.contrib.auth import get_user_model
from datetime import timedelta, date
from django.core.exceptions import ValidationError

User = get_user_model()

def validate_amount(value):
    if value < 1000 or value > 100000:
        raise ValidationError("Amount must be between 1000 and 100000")

def validate_tenure(value):
    if value < 3 or value > 12:
        raise ValidationError("Tenure must be between 3 and 12")

class Loan(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    loan_id = models.CharField(max_length=10,unique=True,editable=False)
    amount = models.DecimalField(max_digits=10,decimal_places=2,validators=[validate_amount])
    tenure = models.IntegerField(validators=[validate_tenure])
    interest_rate = models.DecimalField(max_digits=5,decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10,choices=[('ACTIVE','Active'),('CLOSED','Closed')],default='ACTIVE')


    def monthly_installment(self):
        r = float(self.interest_rate)/100/12
        n= self.tenure
        if r == 0:
            emi = float(self.amount)/n
        else:
            emi = float(self.amount)*r*((1+r)**n)/(((1+r)**n)-1)
        return round(emi,2)

    def total_interest(self):
        return round((self.monthly_installment()*self.tenure)-float(self.amount),2)

    def total_amount(self):
        return round((self.monthly_installment()*self.tenure),2)

    def payment_schedule(self):
        schedule = []
        due_date = date.today()
        monthly_installment = self.monthly_installment()
        for i in range(1,self.tenure+1):
            due_date+=timedelta(days=30)
            schedule.append({
                "installment_no":i,
                "due_date":due_date.strftime("%y-%m-%d"),
                "amount":monthly_installment
            })
        return schedule

    def save(self, *args, **kwargs):
        if not self.loan_id:
            last_loan = Loan.objects.last()  # get the last loan
            new_number = int(last_loan.loan_id[4:]) + 1 if last_loan else 1  # extract last loan and gets the id & increment with id number .if last loan_id is none add 1
            self.loan_id = f"LOAN{new_number:03d}"  # generate ID like LOAN001
        super().save(*args, **kwargs)


    def __str__(self):
        return self.user.username + self.loan_id



