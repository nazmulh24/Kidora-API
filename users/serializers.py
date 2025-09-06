from djoser.serializers import (
    UserCreateSerializer as BaseUserCreateSerializer,
    UserSerializer as BaseUserSerializer,
)


class UserCreateSerializer(BaseUserCreateSerializer):
    """Serializer for user registration"""

    class Meta(BaseUserCreateSerializer.Meta):
        fields = (
            "id",
            "first_name",
            "last_name",
            "email",
            "address",
            "phone_number",
            "password",
        )


class UserSerializer(BaseUserSerializer):
    """Complete user serializer for authenticated users"""

    class Meta(BaseUserSerializer.Meta):
        ref_name = "CustomUser"
        fields = (
            "id",
            "email",
            "profile_picture",
            "first_name",
            "last_name",
            "address",
            "phone_number",
            "is_staff",
        )
        read_only_fields = ("id", "email", "password", "is_staff")
