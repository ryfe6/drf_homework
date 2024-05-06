from django_filters.rest_framework import DjangoFilterBackend, OrderingFilter
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
    DestroyAPIView,
)
from users.serializers import PaymentSerializer
from users.models import Payment


class PaymentCreateAPIView(CreateAPIView):

    serializer_class = PaymentSerializer


class PaymentListAPIView(ListAPIView):

    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    filter_backends = [OrderingFilter]
    ordering_fields = ["payment_date"]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ("payment_course", "payment_lesson", "payment_method")


class PaymentRetrieveAPIView(RetrieveAPIView):

    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()


class PaymentUpdateAPIView(UpdateAPIView):

    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()


class PaymentDestroyAPIView(DestroyAPIView):

    queryset = Payment.objects.all()
