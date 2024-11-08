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
        input_a = Decimal(serializer.validated_data.get("input_a"))
        input_b = Decimal(serializer.validated_data.get("input_b"))
        operator = serializer.validated_data.get("operator")

        if operator == "+":
            result = input_a + input_b
        elif operator == "-":
            result = input_a - input_b
        elif operator == "*":
            result = input_a * input_b
        elif operator == "/":
            if not input_b:
                return Response({"error": "0으로 나눗셈 불가"})
            else:
                result = input_a / input_b
        else:
            return Response({"error": "연산자에 오류가 있습니다."})
        ## end assignment1

        # serialization
        return Response(CalculatorResponseSerializer({"result": result}).data)
