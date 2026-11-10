from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from users.views import Register, CurrentUserProfile

urlpatterns = [
    path("auth/register/", Register.as_view(), name="auth-register"),
    path("auth/login/", TokenObtainPairView.as_view(), name="token-obtain-pair"),
    path("auth/refresh/", TokenRefreshView.as_view(), name="token-refresh"),
    path("auth-me", CurrentUserProfile.as_view(), name="user-profile")
]
