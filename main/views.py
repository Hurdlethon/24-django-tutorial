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
        ## assignment1: 이곳에 과제를 작성해주세요
        input_a = serializer.validated_data['input_a']
        input_b = serializer.validated_data['input_b']
        operator = serializer.validated_data['operator']

        try:
            a = Decimal(input_a)
            b = Decimal(input_b)

            if operator == '+':
                result = a + b
            elif operator == '-':
                result = a - b
            elif operator == '*':
                result = a * b
            elif operator == '/':
                if b == 0:
                    return Response({"error": "Division by zero is not allowed"}, status=400)
                result = a / b
            else:
                return Response({"error": "Unsupported operator"}, status=400)
        except Exception as e:
            return Response({"error": str(e)}, status=400)
        ## end assignment1

        # serialization
        return Response(CalculatorResponseSerializer({"result": result}).data)
