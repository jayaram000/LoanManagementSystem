from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import Loan
from.serializers import LoanSerializer

class LoanCreateView(APIView):
    permission_classes = [IsAuthenticated,]

    def post(self,request):
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
        loans = Loan.objects.filter(user=request.user)
        serializer = LoanSerializer(loans,many=True)
        return Response({"status":"success","data":{"loans":serializer.data}},status=status.HTTP_200_OK)

class LoanForeclosureView(APIView):
    permission_classes = [IsAuthenticated,]

    def post(self,request,loan_id):
        try:
            loan = Loan.objects.get(loan_id=loan_id,user=request.user)
            if loan.status == "CLOSED":
                return Response({"status":"error","message":"Loan is already closed"},status = status.HTTP_400_BAD_REQUEST)

            amount_paid = loan.total_amount() - 500
            closure_settlement = amount_paid - 500

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
