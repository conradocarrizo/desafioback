from sqlite3 import IntegrityError
from rest_framework.views import exception_handler
from rest_framework import status

from app.errors import InvalidNumberCard, InvalidAmount, InvalidPaymentMethod
from rest_framework.response import Response


CUSTOM_400_ERRORS = [InvalidNumberCard, InvalidAmount, InvalidPaymentMethod]
constrais = {
    "payable_id": "just one payment for tax",
    "check_payment_method_card_number": "card number must be sent when the payment method is not cash",
}


def custom_exception_handler(exc, context):

    response = exception_handler(exc, context)
    if response is not None:
        return response

    if type(exc) in CUSTOM_400_ERRORS:
        return Response({"error": exc.message}, status=status.HTTP_400_BAD_REQUEST)

    for con in constrais.items():
        if con[0] in exc.args[0]:
            return Response(
                {"error": con[1]}, status=status.HTTP_400_BAD_REQUEST
            )

    else:
        return Response(
            {"error": format(exc)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
