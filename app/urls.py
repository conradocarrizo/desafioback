from rest_framework.routers import DefaultRouter
from app.views import TaxViewSet, TransactionView


router = DefaultRouter()
router.register('tax', TaxViewSet)
router.register('transaction', TransactionView)