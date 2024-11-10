from rest_framework.exceptions import AuthenticationFailed, PermissionDenied
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin, DestroyModelMixin, CreateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth import login, authenticate
from main.models import Study, StudyParticipation
from main.serializers import StudySerializer, LoginSerializer, UserSerializer, StudyParticipationSerializer
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

    permission_classes = [IsAuthenticated]
    serializer_class = StudyParticipationSerializer

    def get_queryset(self):
        return StudyParticipation.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        user_data = serializer.validated_data.get('user')
        if user_data != self.request.user:
            raise PermissionDenied("다른 사용자의 참여를 추가할 권한이 없습니다.")
        serializer.save(user=self.request.user)

class StudyParticipationView(DestroyModelMixin, GenericAPIView):

    permission_classes = [IsAuthenticated]
    serializer_class = StudyParticipationSerializer

    def get_queryset(self):
        return StudyParticipation.objects.filter(user=self.request.user)
