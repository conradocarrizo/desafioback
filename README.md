* configurar entorno virtual
    ``` bash
    # se hace uso de pyenv
    cd ~/desafioback/
    pyenv install 3.8.0 
    pyenv virtualenv 3.8.0 desafioback
    pyenv activate desafioback

    # con el entornovirtaul activo deberia ver algo asi en la shell: (pickup_points_api)     
    pip install -r requirements.txt 
    ```
* iniciar el django
    ``` bash
    cd ~/desafioback/
    ./manage.py migrate 

    ./manage.py runservert 
    ```
* Endpoints

```
los endpoint requieren Bearer Token que se puede obtener desde este endpoint

POST /api/token/ 
body = { username, password}
response {
	"refresh": "eyJhbGciOiJIUzI1Ni"
    	"access": "eyJhbGciO"
}



POST /api/tax/create-tax/ crear tax/invoice

body
{
    "service_type": LUZ|GAS,
    "description": "factura de gas agosto 2022",
    "due_date": "2022-03-22T13:17:27.853707Z",
    "amount": 200.0
}
RESPONSE 
{
    "bar_code": 20,
    "service_type": "LUZ",
    "description": "factura de gas agosto 2022",
    "due_date": "2022-03-22T13:17:27.853707Z",
    "amount": 200.0,
    "state": "pending"
}


GET /api/tax/ lista de taxes/payables
query_param  service_type = LUZ|GAS
RESPONSE
[
    {
        "bar_code": 1,
        "service_type": "GAS",
        "due_date": "2022-03-22T13:17:27.853707Z",
        "amount": 200.0
    },
]

POST /api/transaction/pay-tax/ pagar payable
body
{
    "bar_code":17,
    "payment_method":"credit_card",
    "card_number":"3121123456782367",
    "amount": 200.2

}
response = {
    "id": 3,
    "created_at": "2022-11-07T09:35:31.716426Z",
    "payment_method": "credit_card",
    "card_number": "3121123456782367",
    "amount": 200.2,
    "payable": 17
}

GET /api/transaction/ agrupa las transacciones por dia y muestra su total.

query_params since y until

Response
[
    {
        "date": "2022-11-07",
        "transaction_number": 3,
        "total": 600.5999999999999
    },
    {
        "date": "2022-11-08",
        "transaction_number": 1,
        "total": 200.1999999999999
    },
    {
        "date": "2022-11-09",
        "transaction_number": 4,
        "total": 800.7999999999999
    }
]

```