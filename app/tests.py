from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from app.models import PayableState


class BaseTestCase(APITestCase):
    @property
    def bearer_token(self):
        user = User.objects.create_user(
            username="username", email='email@email.com', password='some_password'
        )
        refresh = RefreshToken.for_user(user)
        return {"HTTP_AUTHORIZATION": f'Bearer {refresh.access_token}'}


class PayablesList(BaseTestCase):
    base_url = "/api/tax/"


    def test_list_payable(self):
        response = self.client.get(self.base_url, **self.bearer_token)
        self.assertEqual(response.status_code, 200)
    
    def test_create_payable(self):
        create_url = "/api/tax/create-tax/"
        PayableState.objects.create(name="LUZ")
        data_to_create = {
            "service_type": "LUZ",
            "description": "factura de gas agosto 2022",
            "due_date": "2022-03-22T13:17:27.853707Z",
            "amount": 200.0
        }
        response = self.client.post(create_url, data_to_create, **self.bearer_token)
        self.assertEqual(response.status_code, 201)