from rest_framework import status
from rest_framework.generics import RetrieveAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from recipes.permissions import IsAdminOrSuperUser

from .models import CustomUser
from .serializers import ChangePasswordSerializer, UserSerializer


class ChangePasswordView(UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    model = CustomUser
    permission_classes = [IsAuthenticated, IsAdminOrSuperUser]

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        obj = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            obj.set_password(serializer.data.get('new_pass'))
            obj.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Пароль успешно изменен.',
                'data': []
            }
            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserView(RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, ]
    queryset = CustomUser.objects.all()

    def get_object(self):
        return self.request.user
