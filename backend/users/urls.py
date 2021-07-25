from django.urls import include, path

from .views import (ChangePasswordView, FollowAPIView, ListFollowView,
                    UserView)

urlpatterns = [
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    path('users/set_password/', ChangePasswordView.as_view(),
         name='set_password'),
    path('users/me/', UserView.as_view(), name='me'),
    path('users/<int:author_id>/subscribe/', FollowAPIView.as_view(),
         name='subscribe'),
    path('users/subscriptions/', ListFollowView.as_view(),
         name='subscriptions'),
    path('', include('djoser.urls')),
]
