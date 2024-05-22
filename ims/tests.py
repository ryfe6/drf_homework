from rest_framework import status
from rest_framework.test import APITestCase
from users.models import User
from ims.models import Course, Lesson, Subscription
from django.urls import reverse


class LessonTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email="test@sky.pro", password="qwe123rty")
        self.course = Course.objects.create(
            name="HTML",
        )
        self.lesson = Lesson.objects.create(
            name="урок 1",
            course=self.course,
            description="Изучение backend на языке python",
            url="https://www.youtube.com/watch?v=WpmjzP2mWZY",
            author=self.user,
        )
        self.Subscription = Subscription.objects.create(
            user=self.user, course=self.course
        )
        self.client.force_authenticate(user=self.user)

    def test_lesson_retrieve(self):
        url = reverse("ims:lessons_retrieve", args=(self.lesson.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("name"), "урок 1")

    def test_lesson_create(self):
        url = reverse("ims:lessons_create")
        data = {"name": "урок 2", "url": "https://www.youtube.com/watch?v=WpmjzP2mWZY"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.all().count(), 2)

    def test_lesson_update(self):
        url = reverse("ims:lessons_update", args=(self.lesson.pk,))
        data = {"name": "урок 2"}
        response = self.client.patch(url, data)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("name"), "урок 2")

    def test_lesson_delete(self):
        url = reverse("ims:lessons_delete", args=(self.lesson.pk,))

        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.all().count(), 0)

    def test_lesson_list(self):
        url = reverse("ims:lessons_list")
        response = self.client.get(url)
        data = response.json()
        result = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": self.lesson.pk,
                    "name": self.lesson.name,
                    "course": self.course.pk,
                    "url": self.lesson.url,
                },
            ],
        }
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, result)

    def test_subscription_create(self):
        url = reverse("ims:subscription_create")
        data = {"user": self.user.pk, "course": self.course.pk}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class LessonTestCaseNoAuth(APITestCase):

    def setUp(self):
        self.course = Course.objects.create(name="HTML")
        self.lesson = Lesson.objects.create(
            name="урок 1",
            course=self.course,
            description="Изучение backend на языке python",
            url="https://www.youtube.com/watch?v=WpmjzP2mWZY",
        )

    def test_lesson_retrieve(self):

        url = reverse("ims:lessons_retrieve", args=(self.lesson.pk,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_lesson_create(self):
        url = reverse("ims:lessons_create")
        data = {"name": "урок 2", "url": "https://www.youtube.com/watch?v=WpmjzP2mWZY"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_lesson_update(self):
        url = reverse("ims:lessons_update", args=(self.lesson.pk,))
        data = {"name": "урок 2"}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_lesson_delete(self):
        url = reverse("ims:lessons_delete", args=(self.lesson.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_lesson_list(self):
        url = reverse("ims:lessons_list")
        response = self.client.get(url)
        data = response.json()
        result = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": self.lesson.pk,
                    "name": self.lesson.name,
                    "course": self.course.pk,
                    "url": self.lesson.url,
                },
            ],
        }
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
