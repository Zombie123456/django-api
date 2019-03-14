from django.db.models import Sum
from rest_framework import pagination


class PaginationForTransaction(pagination.LimitOffsetPagination):
    '''
    '''

    def paginate_queryset(self, queryset, request, view=None):
        self.total_amount = \
            queryset.aggregate(Sum('amount')).get('amount__sum')
        return super(PaginationForTransaction, self).\
            paginate_queryset(queryset, request, view)

    def get_paginated_response(self, data):
        paginated_response = super(PaginationForTransaction, self).\
            get_paginated_response(data)
        paginated_response.data['total_amount'] = self.total_amount
        return paginated_response
