from rest_framework.pagination import PageNumberPagination


class CustomUserPagination(PageNumberPagination):
    page_size = 1
