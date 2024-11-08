# Create your views here.
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import (
    ListModelMixin,
    DestroyModelMixin,
    CreateModelMixin,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_403_FORBIDDEN

from main.models import Study
from django.contrib.auth import login, authenticate
from main.serializers import (
    StudySerializer,
    LoginSerializer,
    UserSerializer,
)
from rest_framework import generics
from main.models import StudyParticipation
from main.serializers import StudyParticipationSerializer

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


class StudyParticipationListView(
    ListModelMixin,
    CreateModelMixin,
    GenericAPIView,
):
    """
    GET: 내 스터디 참여 목록. 남의 것이 조회되면 안됩니다.
    POST: 내 스터디 참여 목록 추가. 남의 것을 추가할 수 없습니다(HTTP 403 에러)
    """

    ### assignment3: 이곳에 과제를 작성해주세요
    serializer_class = StudyParticipationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # 현재 사용자만 조회 가능하도록 제한
        return StudyParticipation.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        study = serializer.validated_data.get('study')

        # 스터디 소유자가 아닌 경우 403 Forbidden 반환
        if study.created_by != self.request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)

        # 생성 후 데이터 반환
        study_participation = serializer.save(user=self.request.user)
        return Response(StudyParticipationSerializer(study_participation).data, status=status.HTTP_201_CREATED)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    ### end assignment3


class StudyParticipationView(
    DestroyModelMixin,
    GenericAPIView,
):
    """
    DELETE: 내 스터디 참여 목록 제거. 남의 것을 제거할 수 없습니다(HTTP 404 에러)
    """

    ### assignment3: 이곳에 과제를 작성해주세요
    serializer_class = StudyParticipationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # 현재 사용자만 조회 가능하도록 쿼리셋 제한
        return StudyParticipation.objects.filter(user=self.request.user)

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()  # 현재 사용자 소유의 instance만 가져옴

        # 삭제하려는 객체가 현재 사용자 소유인지 검증
        if instance.user != request.user:
            return Response(status=status.HTTP_404_NOT_FOUND)

        # 현재 사용자가 소유한 객체인 경우에만 삭제 진행
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
    ### end assignment3
