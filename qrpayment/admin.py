from django.contrib import admin
from qrpayment.models import (QRCode,
                              Transaction,
                              PaymentType)


class TransactionAdmin(admin.ModelAdmin):
    list_display = ('transaction_id', 'member_order_id', 'username',
                    'amount', 'created_at', 'updated_at', 'updated_by', 'status')


class QRCodeAdmmin(admin.ModelAdmin):
    list_display = ('name', 'display_name', 'bank_num', 'code',
                    'bank_name', 'appid', 'qr_code', 'payment_type', 'status')


class PaymentTypeAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'display_name', 'status', 'description',
                    'rank', 'scan_code_type')


admin.site.register(Transaction, TransactionAdmin)
admin.site.register(QRCode, QRCodeAdmmin)
admin.site.register(PaymentType, PaymentTypeAdmin)
