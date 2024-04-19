from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView

from apps.user.views import (UserRegisterCreateAPIView, CheckActivationCodeGenericAPIView, ResetPasswordView,
                             ResetPasswordConfirmView, UserViewSet)

urlpatterns = [
    path('register/', UserRegisterCreateAPIView.as_view()),
    path('activate-code/', CheckActivationCodeGenericAPIView.as_view()),
    path('reset-password/', ResetPasswordView.as_view()),
    path('reset-password-confirm/', ResetPasswordConfirmView.as_view()),
    path('login/', TokenObtainPairView.as_view()),
    path("", UserViewSet.as_view({"get": "list"}), name="list"),
    path("<int:id>/", UserViewSet.as_view({"get": "retrieve"}), name="detail"),
    path("update/<int:id>/", UserViewSet.as_view({"put": "partial_update"}), name="update"),
    path("me/", UserViewSet.as_view({"get": "me"}), name="me"),
]
