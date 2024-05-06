from django.urls import path

from users.apps import UsersConfig
from users.views import (
    PaymentCreateAPIView,
    PaymentListAPIView,
    PaymentRetrieveAPIView,
    PaymentUpdateAPIView,
    PaymentDestroyAPIView,
)

app_name = UsersConfig.name

urlpatterns = [
    path("payment/create/", PaymentCreateAPIView.as_view(), name="payment_create"),
    path("payment/", PaymentListAPIView.as_view(), name="payment_list"),
    path("payment/<int:pk>/", PaymentRetrieveAPIView.as_view(), name="payment_get"),
    path(
        "payment/update/<int:pk>/",
        PaymentUpdateAPIView.as_view(),
        name="payment_update",
    ),
    path(
        "payment/delete/<int:pk>/",
        PaymentDestroyAPIView.as_view(),
        name="payment_delete",
    ),
]
