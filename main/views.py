# Create your views here.
from decimal import Decimal

from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from main.serializers import (
    CalculatorSerializer,
    CalculatorResponseSerializer,
)


class CalculatorAPIView(GenericAPIView):
    authentication_classes = []
    permission_classes = []
    serializer_class = CalculatorSerializer

    def post(self, request):
        # de-serialization
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        result: Decimal = None

        a = Decimal(serializer.validated_data.get("input_a"))
        b = Decimal(serializer.validated_data.get("input_b"))
        operator = serializer.validated_data.get("operator")

        if operator == '+':
            result = a + b
        elif operator == '-':
            result = a - b
        elif operator == '*':
            result = a * b
        else:
            result = a / b

        ## end assignment1
        # serialization
        return Response(CalculatorResponseSerializer({"result": result}).data)
