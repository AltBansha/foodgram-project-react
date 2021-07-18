from django.urls import include, path
# from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views

from .views import (
    ChangePasswordView,
    UserView,
)

# router = DefaultRouter()
# router.register('users', CustomUserListCreateView)
# router.register(r'api/users/<int:pk>', CustomUserDetailView)

urlpatterns = [
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    path('auth/token/', views.obtain_auth_token),
    # path('', include('djoser.urls')),
    path('users/{id}/', include('djoser.urls')),
    path('users/set_password/', ChangePasswordView.as_view()),
    path('users/me/', UserView.as_view()),

]
