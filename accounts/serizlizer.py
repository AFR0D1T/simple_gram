from rest_framework import serializers
from django.contrib.auth import get_user_model

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = get_user_model()
        fields = ('first_name', 'last_name', 'username', 'password', 'email', 'avatar')


    def create(self, validated_data):
        return self.Meta.model.objects.create_user(**validated_data)


class UserNestedSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('first_name', 'last_name', 'username')
