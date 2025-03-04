from rest_framework import serializers
from .models import Loan


class LoanSerializer(serializers.ModelSerializer):
    monthly_installment = serializers.SerializerMethodField()
    total_interest = serializers.SerializerMethodField()
    total_amount = serializers.SerializerMethodField()
    payment_schedule = serializers.SerializerMethodField()


    class Meta:
        model = Loan
        fields =  ['loan_id', 'amount', 'tenure', 'interest_rate', 'monthly_installment',
                  'total_interest', 'total_amount', 'payment_schedule','status','created_at']



    def get_monthly_installment(self,obj):
        return obj.monthly_installment()

    def get_total_interest(self,obj):
        return obj.total_interest()

    def get_total_amount(self,obj):
        return obj.total_amount()

    def get_payment_schedule(self,obj):
        return obj.payment_schedule()