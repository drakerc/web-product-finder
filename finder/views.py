from drf_yasg.utils import swagger_auto_schema
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Brand, RegexRule
from .serializers import BrandSerializer, RegexSerializer, ProductsSerializer, \
    ExportRegexesRequestSerializer, ExportRegexesSerializer, SearchSavedRegexSerializer
from rest_framework import generics

from .services.data_exporter.data_exporter import DataExporter
from .services.data_storage.data_storage import data_storage
from .services.regex_searcher.regex_searcher import RegexSearcher


class BrandList(generics.ListCreateAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer


class BrandDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer


class RegexList(generics.ListCreateAPIView):
    queryset = RegexRule.objects.all()
    serializer_class = RegexSerializer

    def get_queryset(self):
        queryset = RegexRule.objects.filter(brand=self.kwargs.get('brand_id'))
        return queryset

    def perform_create(self, serializer):
        try:
            brand = Brand.objects.get(pk=self.kwargs.get('brand_id'))
        except Brand.DoesNotExist:
            raise NotFound('Could not save this regex because the specified brand does not exist.')
        serializer.save(brand=brand)


class RegexDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = RegexRule.objects.all()
    serializer_class = RegexSerializer


class SearchRegex(APIView):
    serializer_class = RegexSerializer
    data_storage = data_storage
    regex_searcher = RegexSearcher()

    @swagger_auto_schema(
        operation_description='Searches for products matching the specified regex in the request',
        request_body=RegexSerializer,
        responses={200: ProductsSerializer}
    )
    def post(self, request):
        regex_serializer = self.serializer_class(data=request.data)
        regex_serializer.is_valid(raise_exception=True)
        regex = regex_serializer.validated_data.get('rule_text', )
        products = data_storage.products_list
        products_matching_regex = self.regex_searcher.find_matching_products(
            regex,
            products,
            ['name', 'item_description']
        )

        products_serializer = ProductsSerializer({'products': products_matching_regex})
        return Response(products_serializer.data)


class SearchSavedRegex(APIView):
    data_storage = data_storage
    regex_searcher = RegexSearcher()

    @swagger_auto_schema(
        operation_description='Searches for products matching a selected regex from the database',
        responses={200: SearchSavedRegexSerializer}
    )
    def get(self, request, brand_id, regex_id):
        try:
            regex = RegexRule.objects.get(pk=regex_id, brand_id=brand_id)
        except RegexRule.DoesNotExist:
            raise NotFound('Could not find the selected regex.')
        products = data_storage.products_list
        products_matching_regex = self.regex_searcher.find_matching_products(
            regex.rule_text,
            products,
            ['name', 'item_description']
        )

        products_serializer = SearchSavedRegexSerializer({
            'products': products_matching_regex,
            'regex': regex,
            'brand': regex.brand
        })
        return Response(products_serializer.data)


class ExportBrandRegexes(APIView):
    serializer_class = ExportRegexesRequestSerializer
    data_exporter = DataExporter()

    @swagger_auto_schema(
        operation_description='Exports regex rules of a brand to a selected file type',
        request_body=ExportRegexesRequestSerializer,
        responses={200: ExportRegexesSerializer}
    )
    def post(self, request, brand_id):
        input_serializer = self.serializer_class(data=request.data)
        input_serializer.is_valid(raise_exception=True)
        try:
            brand = Brand.objects.get(pk=brand_id)
        except Brand.DoesNotExist:
            raise NotFound('Could not find the selected brand.')
        generated_file = self.data_exporter.export_brand_regexes(
            brand,
            format_type=input_serializer.validated_data.get('file_type')
        )
        products_serializer = ExportRegexesSerializer({'file_path': generated_file})
        return Response(products_serializer.data)
