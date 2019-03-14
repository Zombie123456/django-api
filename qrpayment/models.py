from __future__ import unicode_literals
import uuid
import datetime

from django.db import models
from django.contrib.auth.models import User

from mewtwo.utils import PathAndRename


STATUS_OPTIONS = (
    (0, 'Inactive'),
    (1, 'Active')
)


TRANSACTION_STATUS_OPTIONS = (
    (0, 'Ongoing'),
    (1, 'Success'),
    (2, 'Cancelled'),
)


SCAN_CODE_OPTIONS = (
    (0, 'qr_code'),
    (1, 'bank_scan')
)


TRANSACTION_TYPE_OPTIONS = (
    (0, 'Application'),
    (1, 'Transaction')
)


class PaymentType(models.Model):
    code = models.CharField(max_length=255, null=True)
    name = models.CharField(max_length=255)
    display_name = models.CharField(max_length=255)
    status = models.IntegerField(default=1, choices=STATUS_OPTIONS)
    description = models.TextField(null=True, blank=True)
    rank = models.IntegerField(default=1, null=True, blank=True)
    scan_code_type = models.IntegerField(default=0, choices=SCAN_CODE_OPTIONS)

    def __str__(self):
        return f'{self.name} - {self.code} '

    class Meta:
        db_table = 'transaction_paymenttype'
        permissions = (('list_paymenttype', 'Can list payment type'),)


class QRCode(models.Model):
    name = models.CharField(max_length=255)
    display_name = models.CharField(max_length=255)
    bank_num = models.CharField(max_length=255, null=True, blank=True)
    code = models.CharField(max_length=255, null=True, blank=True)
    bank_name = models.CharField(max_length=255, null=True, blank=True)
    appid = models.CharField(max_length=255, null=True, blank=True)
    qr_code = models.ImageField(upload_to=PathAndRename('qr_codes/'),
                                null=True, blank=True)
    payment_type = models.ForeignKey(PaymentType, null=True, blank=True,
                                     related_name='qrcodes', on_delete=models.SET_NULL)
    status = models.IntegerField(default=1, choices=STATUS_OPTIONS)

    def __str__(self):
        return f'{self.name} - {self.code} '

    class Meta:
        db_table = 'transaction_qrcode'
        permissions = (('list_qrcode', 'Can list qr code'),)


class Transaction(models.Model):
    transaction_id = models.CharField(max_length=255, null=True,
                                      blank=True, unique=True)
    member_order_id = models.CharField(max_length=255, null=True, blank=True)
    username = models.CharField(max_length=255)
    amount = models.FloatField(default=0.0)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(
        User, related_name='transaction_updated_by',
        on_delete=models.SET_NULL, null=True, blank=True)
    status = models.IntegerField(default=0, choices=TRANSACTION_STATUS_OPTIONS)

    memo = models.TextField(null=True, blank=True)
    type = models.IntegerField(default=0, choices=TRANSACTION_TYPE_OPTIONS)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        unique_id = str(uuid.uuid4().fields[0])
        datetime_now = datetime.datetime.now().strftime('%Y%m%d%H%M%S')

        if not self.transaction_id:
            self.transaction_id = f'{datetime_now}{unique_id}'

    def __str__(self):
        return self.transaction_id

    class Meta:
        db_table = 'transaction_transaction'
        permissions = (('list_transaction', 'Can list transaction'),)
