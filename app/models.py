from django.db import models
from django.core.validators import MinValueValidator
from app.enums import InvoiceStatesEnum, PaymentTypesEnum, ServiceTypeEnum


class Invoice(models.Model):

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
        "InvoiceState", through="InvoiceStateHistory", related_name="invoice"
    )

    property

    def state(self):
        current_state = self.states.all().filter(is_active=True).first()
        return current_state


class InvoiceState(models.Model):
    name = models.CharField(max_length=20, choices=InvoiceStatesEnum.choices())


class InvoiceStateHistory(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.PROTECT)
    state = models.ForeignKey(InvoiceState, on_delete=models.PROTECT)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=[
                    "invoice",
                ],
                condition=models.Q(is_active=True),
                name="uniq_invoice_state_active",
            )
        ]


class Payment(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.PROTECT)
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
                    "invoice",
                ],
                name="just_one_payment",
            )
        ]
