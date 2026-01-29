from rest_framework import serializers
from categories.models import Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = (
            "id",
            "name",
            "category_type",
            "parent",
            "is_active",
        )


class CategoryTreeSerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = (
            "id",
            "name",
            "category_type",
            "children",
        )

    def get_children(self, obj):
        qs = obj.children.filter(
            is_active=True,
            is_deleted=False,
        )
        return CategoryTreeSerializer(qs, many=True).data
