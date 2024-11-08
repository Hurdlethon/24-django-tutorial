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
        data = serializer.validated_data

        result: Decimal = None

        a = Decimal(data['input_a'])
        b = Decimal(data['input_b'])
        if data['operator'] == '+':
            result = a + b
        elif data['operator'] == '-':
            result = a - b
        elif data['operator'] == '*':
            result = a * b
        elif data['operator'] == '/':
            result = a / b

        # serialization
        return Response(CalculatorResponseSerializer({"result": result}).data)