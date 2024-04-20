from drf_spectacular.utils import extend_schema
from rest_framework.mixins import ListModelMixin
from rest_framework.viewsets import GenericViewSet

from apps.categories.models import Category
from apps.categories.serializers import CategorySerializer


@extend_schema(tags=["categories"])
class CategoryListViewSet(ListModelMixin, GenericViewSet):
    queryset = (
        Category.objects.all()
        .select_related("parent")
        .prefetch_related("parent")
    ).get_cached_trees()
    serializer_class = CategorySerializer

    # @extend_schema(parameters=[OpenApiParameter(name="level", type=int, description="The level of the category")])
    # def get_queryset(self) -> QuerySet:
    #     print(self.request.query_params)
    #     queryset = super().get_queryset()
    #     level = self.request.query_params.get("level")
    #     if level:
    #         queryset = queryset.filter(level=level)
    #     return queryset
