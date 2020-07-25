from rest_framework import serializers
from finder.models import Brand, RegexRule


class RegexSerializer(serializers.ModelSerializer):
    brand = serializers.PrimaryKeyRelatedField(read_only=True, required=False, many=False)
    created_at = serializers.DateTimeField(required=False, read_only=True)

    class Meta:
        model = RegexRule
        fields = ['pk', 'rule_text', 'brand', 'created_at']


class BrandSerializer(serializers.ModelSerializer):
    regexes = RegexSerializer(many=True, required=False, read_only=True)

    class Meta:
        model = Brand
        fields = ['pk', 'name', 'parent', 'created_at', 'regexes']


class ProductSerializer(serializers.Serializer):
    id_source = serializers.CharField()
    name = serializers.CharField()
    item_description = serializers.CharField()
    category = serializers.CharField()


class ProductsSerializer(serializers.Serializer):
    products = ProductSerializer(many=True)


class SearchSavedRegexSerializer(serializers.Serializer):
    products = ProductSerializer(many=True)
    brand = BrandSerializer()
    regex = RegexSerializer()


class ExportRegexesRequestSerializer(serializers.Serializer):
    file_type = serializers.ChoiceField(choices=['csv'], required=True)


class ExportRegexesSerializer(serializers.Serializer):
    file_path = serializers.CharField()
