from django.urls import path
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from users.apps import UsersConfig
from users.views import (
    PaymentCreateAPIView,
    PaymentListAPIView,
    PaymentRetrieveAPIView,
    PaymentUpdateAPIView,
    PaymentDestroyAPIView,
    UserCreateApiView
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
    path('register/', UserCreateApiView.as_view(), name="register"),
    path('login/', TokenObtainPairView.as_view(permission_classes=(AllowAny,)), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(permission_classes=(AllowAny,)), name='token_refresh'),
]
