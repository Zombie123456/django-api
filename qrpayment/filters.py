import django_filters
from qrpayment.models import Transaction


class TransactionFilter(django_filters.FilterSet):
    class Meta:
        model = Transaction
        fields = '__all__'
    id = django_filters.CharFilter(field_name='id', lookup_expr='exact')
    username = django_filters.CharFilter(field_name='username',
                                         lookup_expr='exact')
    username_q = django_filters.CharFilter(field_name='username',
                                           lookup_expr='contains')
    created_at = django_filters.DateFromToRangeFilter()
    updated_at = django_filters.DateFromToRangeFilter()
    updated_by = django_filters.CharFilter(
        field_name='updated_by__username', lookup_expr='contains')
    type = django_filters.CharFilter(field_name='type', lookup_expr='exact')
