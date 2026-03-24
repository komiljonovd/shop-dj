# userapp/serializers.py
from rest_framework import serializers
from .models import User
from django.contrib.auth import authenticate

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ['full_name', 'phone_number', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            full_name=validated_data['full_name'],
            phone_number=validated_data['phone_number'],
            password=validated_data['password']
        )
        return user


class LoginSerializer(serializers.Serializer):
    full_name = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    exclude = ['phone_number']
    def validate(self, data):
        full_name = data.get('full_name')
        password = data.get('password')
        if full_name and password:
            user = authenticate(username=full_name, password=password)
            if not user:
                raise serializers.ValidationError("Неправильное ФИО или пароль")
        else:
            raise serializers.ValidationError("ФИО и пароль обязательны")
        data['user'] = user
        print(data['user'])
        return data