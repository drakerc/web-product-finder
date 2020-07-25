from django.conf.urls import url
from django.urls import path
from finder.views import BrandDetail, BrandList, SearchRegex, RegexList, ExportBrandRegexes, \
    RegexDetail, SearchSavedRegex
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="Product Finder API",
      default_version='v1',
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path('api/v1/brand/', BrandList.as_view()),
    path('api/v1/brand/<int:pk>/', BrandDetail.as_view()),
    path('api/v1/brand/<int:brand_id>/export-rules', ExportBrandRegexes.as_view()),
    path('api/v1/brand/<int:brand_id>/regex', RegexList.as_view()),
    path('api/v1/brand/<int:brand_id>/regex/<int:pk>', RegexDetail.as_view()),

    path('api/v1/brand/<int:brand_id>/regex/<int:regex_id>/search-regex', SearchSavedRegex.as_view()),
    path('api/v1/search-regex', SearchRegex.as_view()),

    url(r'^api/swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0),
        name='schema-json'),
    url(r'^api/swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    url(r'^api/redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
