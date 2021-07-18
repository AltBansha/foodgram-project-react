from rest_framework.permissions import IsAuthenticated
from .models import CustomUser
from .serializers import (
    UserSerializer,
    ChangePasswordSerializer,
)
from rest_framework.generics import (
    UpdateAPIView,
    RetrieveAPIView,
)
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from recipes.permissions import IsAdminOrSuperUser


class ChangePasswordView(UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    model = CustomUser
    permission_classes = (IsAuthenticated, IsAdminOrSuperUser)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        obj = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            old_pass = serializer.data.get('old_pass')
            if not obj.check_password(old_pass):
                return Response({'old_pass': ['неверный пароль.']},
                                status=status.HTTP_400_BAD_REQUEST)
            new_pass = serializer.data.get('new_pass')
            new_pass_repeat = serializer.data.get('new_pass_repeat')
            if new_pass == old_pass:
                return Response(
                    {
                        'new_pass':
                            ['старый пароль не отличается от нового']},
                        status=status.HTTP_400_BAD_REQUEST
                )
            if new_pass == new_pass_repeat:
                obj.set_password(serializer.data.get('new_pass'))
                obj.save()
                response = {
                    'status': 'success',
                    'code': status.HTTP_200_OK,
                    'message': 'пароль успешно изменен',
                    'data': []
                }

                return Response(response)
            else:
                return Response({
                    'new_pass': ['новый пароль не подтвержден']},
                                status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserView(RetrieveAPIView):
    model = CustomUser
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsAdminOrSuperUser]
    queryset = CustomUser.objects.all()

    def get_object(self):
        queryset = self.get_queryset()
        user = get_object_or_404(queryset,
                                 auth_token=self.request.user.auth_token)
        return user
