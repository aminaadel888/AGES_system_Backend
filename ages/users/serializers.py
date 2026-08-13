
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


#############################################################################
##################### Admin  ##########################
########################################################################################
class AdminUserSerializer(serializers.ModelSerializer):

    password = serializers.CharField(
        write_only=True,
        required=False,
        min_length=6
    )

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "phone",
            "role",
            "is_active",
            "is_staff",
            "password",
        ]

        read_only_fields = [
            "id",
            "is_staff",
        ]

    def validate_password(self, value):
        if len(value) < 6:
            raise serializers.ValidationError(
                "Password must be at least 6 characters."
            )

        return value

    def create(self, validated_data):
        password = validated_data.pop("password", None)

        if not password:
            raise serializers.ValidationError({
                "password": "Password is required."
            })

        user = User.objects.create_user(
            password=password,
            **validated_data
        )

        return user

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if password:
            instance.set_password(password)

        instance.save()

        return instance


class AdminChangePasswordSerializer(serializers.Serializer):
    password = serializers.CharField(
        write_only=True,
        min_length=6
    )

    def validate_password(self, value):
        if len(value) < 6:
            raise serializers.ValidationError(
                "Password must be at least 6 characters."
            )

        return value

###### change my own password ###########
class ChangeOwnPasswordSerializer(serializers.Serializer):

    old_password = serializers.CharField(
        write_only=True
    )

    new_password = serializers.CharField(
        write_only=True,
        min_length=6
    )

    def validate_old_password(self, value):
        user = self.context["request"].user

        if not user.check_password(value):
            raise serializers.ValidationError(
                "Old password is incorrect."
            )

        return value

    def validate_new_password(self, value):
        if len(value) < 6:
            raise serializers.ValidationError(
                "Password must be at least 6 characters."
            )

        return value