class InvalidNumberCard(Exception):
    message: str = "the card must be a number"

    def __str__(self):
        return self.message


class InvalidPaymentMethod(Exception):
    message: str = "the payment method is invalid"

    def __str__(self):
        return self.message


class InvalidAmount(Exception):
    message: str = "the amount must be positive"

    def __str__(self):
        return self.message
