from rest_framework import serializers
from .models import Student  # Student 모델 임포트

class StudentSerializer(serializers.ModelSerializer):
    """
    학생 모델에 대한 Serializer
    """

    class Meta:
        model = Student
        fields = '__all__'  # 필요한 필드 설정
