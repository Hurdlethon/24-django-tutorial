from rest_framework.generics import GenericAPIView
from rest_framework import mixins
from .models import Student
from .serializers import StudentSerializer

class StudentListAPIView(mixins.ListModelMixin, mixins.CreateModelMixin, GenericAPIView):
    """
    GET: 학생 목록 조회
    POST: 학생 추가
    """

    ### assignment2: 이곳에 과제를 작성해주세요
    serializer_class = StudentSerializer
    queryset = Student.objects.all()

    def get(self, request, *args, **kwargs):
        response = self.list(request, *args, **kwargs)
        return response

    def post(self, request, *args, **kwargs):
        response = self.create(request, *args, **kwargs)
        return response
    ### end assignment2


class StudentAPIView(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, GenericAPIView):
    """
    GET: 학생 조회
    PATCH: 학생 수정
    DELETE: 학생 삭제
    """

    ### assignment2: 이곳에 과제를 작성해주세요
    serializer_class = StudentSerializer
    queryset = Student.objects.all()

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        result = self.partial_update(request, *args, **kwargs)
        return result

    def delete(self, request, *args, **kwargs):
        outcome = self.destroy(request, *args, **kwargs)
        return outcome
    ### end assignment2
