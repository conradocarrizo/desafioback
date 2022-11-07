
from enum import Enum

class BaseEnum(Enum):
    @classmethod
    def choices(cls):
        return tuple((i.name, i.value) for i in cls)

class ServiceTypeEnum(BaseEnum):

    GAS = "gas"
    LUZ = "luz"


class InvoiceStatesEnum(BaseEnum):

    PAID = "paid"
    PENDING = "pending"
    CANCELLED = "canceled"
    OVERDUE = "overdue"

class PaymentTypesEnum(BaseEnum):

    CREDIT_CARD = "credit_card"
    DEBIT_CARD = "debit_card"
    CASH = "cash"
