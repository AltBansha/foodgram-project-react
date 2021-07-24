from django.urls import include, path

from .views import (ChangePasswordView, FollowAPIView, ListFollowViewSet,
                    UserView)

urlpatterns = [
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    path('users/set_password/', ChangePasswordView.as_view()),
    path('users/me/', UserView.as_view()),
    path('users/<int:author_id>/subscribe/', FollowAPIView.as_view()),
    path('users/subscriptions/', ListFollowViewSet.as_view()),
    path('', include('djoser.urls')),
]
