from django.conf.urls import url, include
from qrpayment import views as qrpayment
from rest_framework import routers


member_router = routers.DefaultRouter()

member_router.register(r'payment',
                       qrpayment.PaymentTypeMemberViewSet,
                       base_name='payment')
member_router.register(r'transaction',
                       qrpayment.TransactionMemberView,
                       base_name='transaction')
member_router.register(r'alipaytobank',
                       qrpayment.BankQrcodeMemberViewSet,
                       base_name='alipaytobank')

urlpatterns = [
    url(r'^member/', include(member_router.urls)),
]
