from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .models import Student
from .serializers import StudentSerializer

class StudentListAPIView(ListCreateAPIView):
    """
    GET: 학생 목록 조회
    POST: 학생 추가
    """
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

class StudentAPIView(RetrieveUpdateDestroyAPIView):
    """
    GET: 학생 조회
    PATCH: 학생 수정
    DELETE: 학생 삭제
    """
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
