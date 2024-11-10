from rest_framework.exceptions import AuthenticationFailed, PermissionDenied
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin, DestroyModelMixin, CreateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth import login, authenticate
from main.models import Study, StudyParticipation
from main.serializers import (
    StudySerializer,
    LoginSerializer,
    UserSerializer,
    StudyParticipationSerializer
)
from rest_framework import generics

class LoginView(GenericAPIView):
    authentication_classes = []
    permission_classes = []
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = authenticate(
            request,
            username=serializer.validated_data["username"],
            password=serializer.validated_data["password"],
        )
        if not user:
            raise AuthenticationFailed("아이디 또는 비밀번호가 틀렸습니다")
        login(request, user)
        return Response()

class SignupView(generics.CreateAPIView):
    authentication_classes = []
    permission_classes = []
    serializer_class = UserSerializer

class StudyListView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Study.objects.all()
    serializer_class = StudySerializer

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

class StudyDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Study.objects.all()
    serializer_class = StudySerializer

    def get_queryset(self):
        if self.request.method == "GET":
            return super().get_queryset()
        return super().get_queryset().filter(created_by=self.request.user)

class StudyParticipationListView(ListModelMixin, CreateModelMixin, GenericAPIView):
    """
    GET: 현재 사용자의 스터디 참여 목록만 조회 가능
    POST: 현재 사용자의 스터디 참여만 추가 가능 (다른 사용자의 경우 403 에러)
    """
    permission_classes = [IsAuthenticated]
    serializer_class = StudyParticipationSerializer

    def get_queryset(self):
        # 현재 로그인된 사용자의 스터디 참여 목록만 필터링
        return StudyParticipation.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # 현재 사용자가 아닌 다른 사용자의 참여를 추가하려고 할 경우 예외 발생
        if serializer.validated_data.get('user') != self.request.user:
            raise PermissionDenied("다른 사용자의 참여를 추가할 권한이 없습니다.")
        serializer.save(user=self.request.user)

class StudyParticipationView(DestroyModelMixin, GenericAPIView):
    """
    DELETE: 현재 사용자의 스터디 참여 목록만 삭제 가능. 다른 사용자의 경우 404 에러
    """
    permission_classes = [IsAuthenticated]
    serializer_class = StudyParticipationSerializer

    def get_queryset(self):
        # 현재 로그인된 사용자의 스터디 참여 이력만 조회
        return StudyParticipation.objects.filter(user=self.request.user)
