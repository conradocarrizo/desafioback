import datetime
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from app.models import (
    Payable,
    PayableState,
    PayableStateHistory,
    PayableStatesEnum,
    Transaction,
)
from django.db import transaction

from app.serializers import (
    PayableListLittleSerializer,
    PayableListSerializer,
    PayableSerializer,
    PayableWriteSerializer,
    TransactionByDaySerializer,
    TransactionSerializer,
    TransactionWriteSerializer,
)


class TaxViewSet(ViewSet):

    permission_classes = [IsAuthenticated]
    serializer_class = PayableSerializer
    queryset = Payable.objects.all()

    def get_serializer_class(self):
        if self.action == "create-tax":
            return PayableWriteSerializer

        if self.action == "list":
            service_type = self.filtered_by_service_type()
            if service_type:
                return PayableListLittleSerializer
            return PayableListSerializer

        return PayableSerializer

    def create_pending_state(self, payable):
        pending_state = PayableState.objects.get(name=PayableStatesEnum.PENDING.value)
        PayableStateHistory.objects.create(payable=payable, state=pending_state)

    def filtered_by_service_type(self):
        if self.request.query_params:
            return self.request.query_params.get("service_type")

    def filter_queryset(self, queryset):
        service_type = self.filtered_by_service_type()
        if service_type:
            queryset = queryset.filter(service_type=service_type)
        return queryset

    def list(self, request):
        queryset = self.queryset
        queryset = self.filter_queryset(queryset)
        serializer = self.get_serializer_class()
        return Response(serializer(queryset, many=True).data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["POST"], url_path="create-tax")
    def create_tax(self, request):
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            with transaction.atomic():
                payable = serializer.save()
                self.create_pending_state(payable)

        return Response(PayableSerializer(payable).data, status=status.HTTP_201_CREATED)


class TransactionView(ViewSet):

    permission_classes = [IsAuthenticated]
    serializer_class = TransactionSerializer
    queryset = Transaction.objects.all()

    def create_paid_state(self, payable):
        paid_state = PayableState.objects.get(name=PayableStatesEnum.PAID.value)
        PayableStateHistory.objects.create(payable=payable, state=paid_state)

    def get_serializer_class(self):
        if self.action == "pay_tax":
            return TransactionWriteSerializer

        if self.action == "list":
            return TransactionByDaySerializer

        return TransactionSerializer

    @action(detail=False, methods=["POST"], url_path="pay-tax")
    def pay_tax(self, request):
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            with transaction.atomic():
                transaction_instance = serializer.save()
                payable = transaction_instance.payable

                payable.payablestatehistory_set.all().update(is_active=False)

                self.create_paid_state(payable)

        return Response(
            TransactionSerializer(transaction_instance).data,
            status=status.HTTP_201_CREATED,
        )

    def get_days(self, since, number_days):
        days = [since]
        today = since
        for day in range(number_days.days):
            today = today + datetime.timedelta(days=1)
            days.append(today)

        return days

    def filter_queryset_to_group_them(self, queryset):
        since = self.request.query_params.get("since")
        until = self.request.query_params.get("until")
        if not since or not until:
            return Response(
                {"error": "since and until fields are required"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        _since = datetime.datetime.strptime(since, "%Y-%m-%d")
        _until = datetime.datetime.strptime(until, "%Y-%m-%d")
        number_days = _until - _since
        days = self.get_days(_since, number_days)
        response = {}
        for date in days:
            response[date.strftime("%Y-%m-%d")] = self.get_queryset_by_date(queryset, date)
        return response

    def get_queryset_by_date(self, queryset, date):
        today_min = datetime.datetime.combine(date, datetime.time.min)
        today_max = datetime.datetime.combine(date, datetime.time.max)
        return queryset.filter(created_at__range=(today_min, today_max))

    def list(self, request):
        queryset = self.queryset
        queryset = self.filter_queryset_to_group_them(queryset)
        serializer = self.get_serializer_class()
        return Response(serializer(queryset, many=True).data, status=status.HTTP_200_OK)
