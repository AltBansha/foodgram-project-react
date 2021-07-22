from django.urls import include, path
from rest_framework.authtoken import views

from .views import ChangePasswordView, UserView
from recipes.views import ListFollowViewSet, FollowViewSet

urlpatterns = [
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    path('auth/token/', views.obtain_auth_token),
    path('users/set_password/', ChangePasswordView.as_view()),
    path('users/me/', UserView.as_view()),
    path('users/<int:author_id>/subscribe/', FollowViewSet.as_view()),
    path('users/subscriptions/', ListFollowViewSet.as_view()),
    path('', include('djoser.urls')),
]
