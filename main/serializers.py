from rest_framework import serializers
from .models import Student


class StudentSerializer(serializers.ModelSerializer):
    """
    학생 모델에 대한 Serializer
    """

    ### assignment2: 이곳에 과제를 작성해주세요
    from rest_framework import serializers
    from .models import Student  # Student 모델 임포트

    class StudentSerializer(serializers.ModelSerializer):
        class Meta:
            model = Student  # 모델 정의
            fields = '__all__'  # 모든 필드 포함

    ### end assignment2
