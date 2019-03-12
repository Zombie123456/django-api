from urllib.parse import urlencode

from rest_condition import Or
from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import mixins, viewsets
from rest_framework.response import Response

from mewtwo.lib import constants
from mewtwo.utils import MewtwoRenderer
from qrpayment.models import (QRCode,
                              Transaction,
                              PaymentType)
from loginsvc.permissions import (IsAdmin,
                                  IsStaff)
from qrpayment.serializers import (QRCodeSerializer,
                                   PaymentTypeSerializer,
                                   TransactionSerializer)


class PaymentTypeMemberViewSet(mixins.CreateModelMixin,
                               mixins.ListModelMixin,
                               viewsets.GenericViewSet):

    model = PaymentType
    queryset = PaymentType.objects.filter(status=1)
    permission_classes = []
    serializer_class = PaymentTypeSerializer
    renderer_classes = [MewtwoRenderer]

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        data = serializer.data
        for qrcode in data:
            if not qrcode.get('QRcode'):
                data.remove(qrcode)
        return Response(data)


class TransactionMemberView(mixins.CreateModelMixin,
                            viewsets.GenericViewSet):

    model = Transaction
    permission_classes = []
    renderer_classes = [MewtwoRenderer]
    serializer_class = TransactionSerializer


class BankQrcodeMemberViewSet(viewsets.GenericViewSet):

    permission_classes = []

    def list(self, request, *args, **kwargs):
        return render(request, 'pay.html')

    def create(self, request, *args, **kwargs):
        data = request.data
        amount = data.get('money')
        user_name = data.get('remark')
        if not amount or not str(amount).isdigit():
            return Response({'code': constants.FIELD_ERROR, 'msg': 'amount error'})

        alipaytobank_obj = PaymentType.objects.\
            filter(status=1, code='alipaytobank').first()
        qrcode = QRCode.objects.filter(status=1, payment_type=\
            alipaytobank_obj).order_by('?').first()

        if not qrcode or not alipaytobank_obj:
            return Response({'code': constants.FIELD_ERROR, 'msg': 'no card'})
        Transaction.objects.create(username=user_name, amount=amount, type=1)

        params = {
            'appId': qrcode.appid,
            'actionType': 'toCard',
            'sourceId': 'bill',
            'cardNo': f'{qrcode.bank_num[:6]}***{qrcode.bank_num[-4:]}',
            'bankAccount': qrcode.name,
            'money': amount,
            'amount': amount,
            'bankMark': qrcode.code,
            'bankName': qrcode.bank_name,
            'cardNoHidden': 'true',
            'cardChannel': 'HISTORY_CARD',
            'orderSource': 'from',
        }

        params_url = urlencode(params)
        alipay_api = f'alipays://platformapi/startapp?{params_url}'
        return Response({'code': constants.ALL_OK, 'url': alipay_api})
