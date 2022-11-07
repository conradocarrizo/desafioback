from django.db import models
from django.core.validators import MinValueValidator
from app.enums import PayableStatesEnum, PaymentTypesEnum, ServiceTypeEnum


class Payable(models.Model):

    bar_code = models.AutoField(primary_key=True)
    service_type = models.CharField(max_length=20, choices=ServiceTypeEnum.choices())
    description = models.CharField(max_length=255, blank=True, null=True)
    due_date = models.DateTimeField(null=True)
    amount = models.FloatField(
        validators=[
            MinValueValidator(0.0),
        ]
    )
    states = models.ManyToManyField(
        "PayableState", through="PayableStateHistory", related_name="payable"
    )

    @property
    def state(self):
        current_state = (
            self.states.all().filter(payablestatehistory__is_active=True).first()
        )
        return current_state


class PayableState(models.Model):
    name = models.CharField(max_length=20, choices=PayableStatesEnum.choices())


class PayableStateHistory(models.Model):
    payable = models.ForeignKey(Payable, on_delete=models.PROTECT)
    state = models.ForeignKey(PayableState, on_delete=models.PROTECT)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=[
                    "payable",
                ],
                condition=models.Q(is_active=True),
                name="uniq_payable_state_active",
            )
        ]


class Transaction(models.Model):
    payable = models.ForeignKey(Payable, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)

    payment_method = models.CharField(max_length=20, choices=PaymentTypesEnum.choices())
    card_number = models.CharField(max_length=16, null=True)
    amount = models.FloatField(
        validators=[
            MinValueValidator(0.0),
        ]
    )

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(
                    payment_method__in=[
                        PaymentTypesEnum.CREDIT_CARD.value,
                        PaymentTypesEnum.DEBIT_CARD.value,
                    ],
                    card_number__isnull=False,
                )
                | models.Q(
                    payment_method=PaymentTypesEnum.CASH.value, card_number__isnull=True
                ),
                name="check_payment_method_card_number",
            ),
            models.UniqueConstraint(
                fields=[
                    "payable",
                ],
                name="just_one_payment",
            ),
        ]
