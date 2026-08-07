
from rest_framework import serializers
from .models import User
from django.contrib.auth import authenticate


class SupervisorDropdownSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username"]


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [ "username", "phone","password","role"]
        extra_kwargs = {
            "password": {"write_only": True}
        }

    
    def create(self, validated_data):

        #validate role
        role = validated_data.get("role", "supervisor")

        if role not in ["manager", "supervisor"]:
            role = "supervisor"

        validated_data["role"] = role

        password = validated_data.pop("password")
        user = User.objects.create_user(password=password, 
                                        **validated_data)
        return user
    
    def validate_password(self, value):
        if len(value) < 6:
            raise serializers.ValidationError("Password too short")
        return value



class LoginSerializer(serializers.Serializer):
    phone = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        phone = data.get("phone")
        password = data.get("password")

        try:
            user = User.objects.get(phone=phone)
        except User.DoesNotExist:
            raise serializers.ValidationError("خطأ في بيانات تسجيل الدخول")

        if not user.check_password(password):
            raise serializers.ValidationError("خطأ في بيانات تسجيل الدخول")

        if not user.is_active:
            raise serializers.ValidationError("حساب المستخدم قيد التفعيل")

        data["user"] = user
        return data