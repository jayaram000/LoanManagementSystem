from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import Loan
from.serializers import LoanSerializer
from django.shortcuts import get_object_or_404


class LoanCreateView(APIView):
    permission_classes = [IsAuthenticated,]

    def post(self,request):
        if request.user.role != 'user':  #only allow users can apply for loan
            return Response({"status": "error", "message": "Only users can apply for loans."},
                            status=status.HTTP_403_FORBIDDEN)
        data = request.data
        data["user"] = request.user.id
        serializer = LoanSerializer(data=data)
        if serializer.is_valid():
            loan = Loan.objects.create(user=request.user,
                                amount=data["amount"],
                                tenure=data["tenure"],
                                interest_rate=data["interest_rate"])
            response_data = LoanSerializer(loan).data
            return Response({"status":"success","data":response_data},status=status.HTTP_201_CREATED)
        return Response({"status":"error","errors":serializer.errors},status=status.HTTP_400_BAD_REQUEST)

class LoanListView(APIView):
    permission_classes = [IsAuthenticated,]

    def get(self,request):

        if request.user.role == 'admin':
            loans = Loan.objects.all()
        else:
            loans = Loan.objects.filter(user=request.user)
        serializer = LoanSerializer(loans,many=True)
        return Response({"status":"success","data":{"loans":serializer.data}},status=status.HTTP_200_OK)

class LoanForeclosureView(APIView):
    permission_classes = [IsAuthenticated,]

    def post(self,request,loan_id):

        if request.user.role != 'user':  #only allow users can foreclose  loan
            return Response({"status": "error", "message": "Only users can foreclose loans."},
                            status=status.HTTP_403_FORBIDDEN)
        try:
            loan = Loan.objects.get(loan_id=loan_id,user=request.user)

            if loan.status == "CLOSED":
                return Response({"status":"error","message":"Loan is already closed"},status = status.HTTP_400_BAD_REQUEST)

            amount_paid = loan.total_amount() - 500
            closure_settlement = amount_paid

            loan.status = "CLOSED"
            loan.save()

            return Response({"status":"success",
                             "message":"Loan Foreclosed successfully.",
                             "data":{"loan_id":loan.loan_id,
                                     "amount_paid":amount_paid,
                                     "foreclosure_discnt":500.00,
                                     "closure_settlement":closure_settlement,
                                     "status":"CLOSED"}
                             },status=status.HTTP_200_OK)

        except Loan.DoesNotExist:
            return Response({"status":"error","message":"Loan not found"},status = status.HTTP_404_NOT_FOUND)


class LoanDeleteView(APIView):
    permission_classes = [IsAuthenticated,]

    def delete(self,request,loan_id):
        if request.user.role != 'admin':
            return Response({"status":"error","message":"only admins can delete loan"},status=status.HTTP_403_FORBIDDEN)

        loan = get_object_or_404(Loan,loan_id=loan_id)
        loan.delete()
        return Response({"status":"success","message":"Loan deleted successfully"},status=status.HTTP_200_OK)
