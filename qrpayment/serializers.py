from rest_framework import serializers

from mewtwo.lib import constants
from qrpayment.models import (QRCode,
                              PaymentType,
                              Transaction)


class QRCodeSerializer(serializers.ModelSerializer):

    class Meta:
        model = QRCode
        fields = '__all__'


class PaymentTypeMemberSerializer(serializers.ModelSerializer):

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


class TransactionMemberSerializer(serializers.ModelSerializer):

    class Meta:
        model = Transaction
        fields = '__all__'


class PaymentTypeSerializer(serializers.ModelSerializer):
    qr_codes = QRCodeSerializer(source='qrcodes', many=True, required=False)

    class Meta:
        model = PaymentType
        fields = '__all__'


class TransactionSerializer(serializers.ModelSerializer):
    updated_by = serializers.ReadOnlyField(source='updated_by.username')

    class Meta:
        model = Transaction
        fields = '__all__'

    def update(self, instance, validated_data):
        request = self.context['request']
        validated_data['updated_by'] = self.context['request'].user
        status = validated_data.get('status', None)
        if status:
            perm = None
            if status == 1:
                perm = 'approve_transactions'
            elif status == 2:
                perm = 'decline_transactions'

            if perm and not IsUserPermittedAdv(request, perm):
                raise serializers.ValidationError(constants.NOT_ALLOWED)

        for key, val in validated_data.items():
            setattr(instance, key, val)
        instance.save(update_fields=validated_data.keys())
        return instance
