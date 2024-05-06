from rest_framework.routers import SimpleRouter
from django.urls import path

from ims.views import (
    CourseViewSet,
    LessonCreateApiView,
    LessonUpdateApiView,
    LessonDestroyApiView,
    LessonRetrieveApiView,
    LessonListApiView,
)
from ims.apps import ImsConfig

app_name = ImsConfig.name

router = SimpleRouter()
router.register("", CourseViewSet)


urlpatterns = [
    path("lessons/", LessonListApiView.as_view(), name="lessons_list"),
    path("lessons/<int:pk>", LessonRetrieveApiView.as_view(), name="lessons_retrieve"),
    path("lessons/create/", LessonCreateApiView.as_view(), name="lessons_create"),
    path(
        "lessons/<int:pk>/delete/",
        LessonDestroyApiView.as_view(),
        name="lessons_delete",
    ),
    path(
        "lessons/<int:pk>/update/", LessonUpdateApiView.as_view(), name="lessons_update"
    ),
]

urlpatterns += router.urls
