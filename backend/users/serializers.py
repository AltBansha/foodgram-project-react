from rest_framework import serializers

from .models import CustomUser


class UserSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField(
        method_name='get_is_subscribed'
    )

    class Meta:
        model = CustomUser
        fields = (
            'id',
            'email',
            'is_subscribed',
            'username',
            'first_name',
            'last_name',
        )

    def get_is_subscribed(self, obj):
        user = self.context.get('request').user
        return user.following.filter(author=obj).exists()


class ChangePasswordSerializer(serializers.Serializer):
    old_pass = serializers.CharField(required=True)
    new_pass = serializers.CharField(required=True)
    new_pass_repeat = serializers.CharField(required=True)

    def validate(self, data):
        if not self.context['request'].user.check_password(
            data.get('old_pass')
        ):
            raise serializers.ValidationError(
                {'old_pass': 'Неверный пароль.'}
            )

        if data.get('new_pass') == data.get('old_pass'):
            raise serializers.ValidationError(
                {'new_pass': 'Новый пароль идентичен старому.'}
            )

        if data.get('new_pass_repeat') != data.get('new_pass'):
            raise serializers.ValidationError(
                {'new_pass': 'Пароли не совпадают.'}
            )

        return data

    def update(self, instance, validated_data):
        instance.set_password(validated_data['new_pass'])
        instance.save()
        return instance
