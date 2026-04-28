from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = get_user_model()
        fields = ('email', 'username', 'password',)


    def create(self, validated_data):
        return self.Meta.model.objects.create_user(**validated_data)


class UserNestedSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('first_name', 'last_name', 'username')


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs, *args, **kwargs):
        user = authenticate(username=attrs.get('username'), password=attrs.get('password'))

        if not user:
            raise serializers.ValidationError()

        return user


class RefreshSerializer(serializers.Serializer):
    refresh = serializers.CharField()


class PasswordSerializer(serializers.ModelSerializer):
    password_old = serializers.CharField(write_only=True)
    password_new = serializers.CharField(write_only=True)

    class Meta:
        model = get_user_model()
        fields = ('password_old', 'password_new')

