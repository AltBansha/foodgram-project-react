from rest_framework import serializers

from .models import CustomUser


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = (
            'id',
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
        )


class ChangePasswordSerializer(serializers.ModelSerializer):
    model = CustomUser
    old_pass = serializers.CharField(required=True)
    new_pass = serializers.CharField(required=True)
    new_pass_repeat = serializers.CharField(required=True)

    class Meta:
        model = CustomUser
        fields = ('old_pass', 'new_pass', 'new_pass_repeat')

    # def validate(self, data):
    #     password = data.get('new_password')
    #     errors = dict()
    #     try:
    #         validators.validate_password(password=password)
    #     except exceptions.ValidationError as e:
    #         errors['new_password'] = list(e.messages)
    #     if errors:
    #         raise serializers.ValidationError(errors)
    #     return super(ChangePasswordSerializer, self).validate(data)
