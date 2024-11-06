"""
URL configuration for django_tutorial project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from .views import StudentListAPIView, StudentAPIView  # 필요한 뷰 임포트

urlpatterns = [
    path("student/", StudentListAPIView.as_view(), name='student-list'),  # 학생 목록 조회 및 추가
    path("student/<int:pk>/", StudentAPIView.as_view(), name='student-detail'),  # 특정 학생 조회, 수정, 삭제
]

