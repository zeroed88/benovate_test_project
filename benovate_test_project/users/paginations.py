from rest_framework import pagination

class MyPageNumberPagination(pagination.PageNumberPagination):
        page_size_query_param = 'page_size'
