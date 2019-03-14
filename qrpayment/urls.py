from rest_framework import routers
from django.conf.urls import url, include

from qrpayment import views as qrpayment


member_router = routers.DefaultRouter()
manage_router = routers.DefaultRouter()

member_router.register(r'payment',
                       qrpayment.PaymentTypeMemberViewSet,
                       base_name='payment')
member_router.register(r'transaction',
                       qrpayment.TransactionMemberView,
                       base_name='transaction')
member_router.register(r'alipaytobank',
                       qrpayment.BankQrcodeMemberViewSet,
                       base_name='alipaytobank')


manage_router.register(r'paymenttype',
                       qrpayment.PaymentTypeViewSet,
                       base_name='paymenttype')
manage_router.register(r'qrcode',
                       qrpayment.QRCodeViewSet,
                       base_name='qrcode')
manage_router.register(r'transaction',
                       qrpayment.TransactionViewSet,
                       base_name='transaction')


urlpatterns = [
    url(r'^member/', include(member_router.urls)),
    url(r'manage/', include(manage_router.urls))
]
