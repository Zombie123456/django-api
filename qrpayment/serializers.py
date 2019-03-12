from qrpayment.models import (QRCode,
                              PaymentType,
                              Transaction)
from rest_framework import serializers


class QRCodeSerializer(serializers.ModelSerializer):

    class Meta:
        model = QRCode
        fields = '__all__'


class PaymentTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = PaymentType
        fields = '__all__'

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        qr_codes = instance.qrcodes.filter(status=1)
        qrcode_list = []
        for qr_code in qr_codes:
            if qr_code.qr_code:
                    qrcode_list.append({'id': qr_code.id,
                                        'status': qr_code.status,
                                        'qrcode': qr_code.qr_code.url
                                        })
        ret['QRcode'] = qrcode_list
        return ret


class TransactionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Transaction
        fields = '__all__'
