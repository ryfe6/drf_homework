from rest_framework.permissions import  IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from users.permissions import IsModer, IsAuthor
from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
    DestroyAPIView,
)

from ims.models import Lesson, Course
from ims.serializers import LessonSerializer, CourseSerializer


class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def perform_create(self, serializer):
        course = serializer.save()
        course.author = self.request.user
        course.save()

    def get_permissions(self):
        if self.action in ["create"]:
            self.permission_classes = (IsAuthenticated, ~IsModer)
        elif self.action in ["destroy"]:
            self.permission_classes = (IsAuthenticated, IsAuthor, ~IsModer)
        elif self.action in ["update", "retrieve",]:
            self.permission_classes = (IsAuthenticated, IsModer, IsAuthor)
        return super().get_permissions()


class LessonCreateApiView(CreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, ~IsModer]

    def perform_create(self, serializer):
        course = serializer.save()
        course.author = self.request.user
        course.save()


class LessonListApiView(ListAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsAuthor]


class LessonRetrieveApiView(RetrieveAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsModer | IsAuthor]


class LessonUpdateApiView(UpdateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsModer | IsAuthor]


class LessonDestroyApiView(DestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsAuthor, ~IsModer]
