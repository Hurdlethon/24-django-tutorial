from rest_framework.response import Response
from rest_framework import status
from rest_framework.mixins import (
    ListModelMixin,
    CreateModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
)
from rest_framework.generics import GenericAPIView
from .models import Student
from .serializers import StudentSerializer

class StudentListAPIView(ListModelMixin, CreateModelMixin, GenericAPIView):
    """
    GET: 학생 목록 조회
    POST: 학생 추가
    """
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)  # GET 요청 처리



    def post(self, request, *args, **kwargs):
        # de-serialization
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # CREATE
        self.perform_create(serializer)

        # serialization
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class StudentAPIView(RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin, GenericAPIView):
    """
    GET: 학생 조회
    PATCH: 학생 수정
    DELETE: 학생 삭제
    """
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        #instance 가져오기
        instance=self.get_Object()

        # de-serialization
        serializer = self.get_serializer(instance, data=request.data,partial=True)
        serializer.is_valid(raise_exception=True)

        #UPDATE
        serializer.save()

        #???
        if getattr(instance,'_prefetched_objects_cache',None):
            instance.prefetched_ocjects_cache={}

        #serialization
        return Response(Serializer.data)


    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

