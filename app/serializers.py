from rest_framework import serializers
from app.enums import PaymentTypesEnum
from app.errors import InvalidNumberCard, InvalidPaymentMethod, InvalidAmount
from app.models import Payable, PayableState, Transaction
from django.db.models import Sum

class PayableStateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PayableState
        fields = "__all__"


class PayableSerializer(serializers.ModelSerializer):
    state = serializers.SerializerMethodField()

    class Meta:
        model = Payable

        fields = (
            "bar_code",
            "service_type",
            "description",
            "due_date",
            "amount",
            "state",
        )

    def get_state(self, playable):
        if playable.state:
            return playable.state.name
        return None


class PayableWriteSerializer(serializers.ModelSerializer):
    service_type = serializers.CharField()
    description = serializers.CharField()
    due_date = serializers.DateTimeField()
    amount = serializers.FloatField()

    class Meta:
        model = Payable
        fields = (
            "service_type",
            "description",
            "due_date",
            "amount",
        )


class PayableListLittleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payable
        fields = (
            "bar_code",
            "due_date",
            "amount",
        )


class PayableListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payable
        fields = (
            "bar_code",
            "service_type",
            "due_date",
            "amount",
        )


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = "__all__"


class TransactionWriteSerializer(serializers.ModelSerializer):

    bar_code = serializers.IntegerField(required=True)
    payment_method = serializers.CharField(required=True)
    card_number = serializers.CharField()
    amount = serializers.FloatField(required=True)

    class Meta:
        model = Transaction
        fields = [
            "bar_code",
            "card_number",
            "payment_method",
            "amount",
        ]

    def create(self, validated_data):
        bar_code = validated_data.pop("bar_code")
        payable = Payable.objects.get(bar_code=bar_code)
        validated_data["payable"] = payable
        return super().create(validated_data)

    def validate_payment_method(self, value):
        if value not in [c[1] for c in PaymentTypesEnum.choices()]:
            raise InvalidPaymentMethod()
        return value

    def validate_card_number(self, value):
        if value and not value.isdigit():
            raise InvalidNumberCard()
        return value

    def validate_amount(self, value):
        if value <= 0:
            raise InvalidAmount()
        return value


class TransactionByDaySerializer(serializers.Serializer):

    def to_representation(self, instance):
        queryset = self.instance.get(instance)
        ret = {}
        ret["date"] = instance
        ret["transaction_number"] = queryset.count()
        ret["total"] = queryset.aggregate(sum=Sum('amount')).get('sum')
        return ret
