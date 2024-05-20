from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from ..models import Order, GeneratedReport
from .serializers import OrderSerializer, GeneratedReportSerializer

class OrderList(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, *args, **kwargs):
        queryset = GeneratedReport.objects.filter(is_automated=True)
        # paginator = PageNumberPagination()

        # You may want to customize the page size per request
        # For example, to allow clients to specify a page size, uncomment the following line:
        # paginator.page_size = request.query_params.get('page_size', 10)

        # page = paginator.paginate_queryset(queryset, request)
        # if page is not None:
        #     serializer = GeneratedReportSerializer(page, many=True)
        #     return paginator.get_paginated_response(serializer.data)

        # Fallback for if pagination is not applicable
        serializer = GeneratedReportSerializer(queryset, many=True)
        return Response(serializer.data)
