from django.urls import path

from apps.categories.views import CategoryListViewSet


urlpatterns = [
    path("", CategoryListViewSet.as_view({"get": "list"}), name="list"),
]
