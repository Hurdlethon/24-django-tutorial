# main/urls.py
from django.urls import path
from .views import StudentListAPIView, StudentAPIView

urlpatterns = [
    path("student/", StudentListAPIView.as_view(), name='student-list'),  # 학생 목록 조회 및 추가
    path("student/<int:pk>/", StudentAPIView.as_view(), name='student-detail'),  # 특정 학생 조회, 수정, 삭제
]
