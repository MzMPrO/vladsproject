from rest_framework import serializers

from apps.categories.models import Category


class RecursiveField(serializers.Serializer):
    """
    Get categories field childrenren recursively
    """

    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data


class CategorySerializer(serializers.ModelSerializer):
    children = RecursiveField(many=True)

    class Meta:
        model = Category
        fields = [
            "id",
            'name',
            "icon",
            'level',
            "children",
        ]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if data["children"] == []:
            del data["children"]
        return data
