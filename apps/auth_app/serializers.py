from dj_rest_auth.registration.serializers import RegisterSerializer
from dj_rest_auth.serializers import LoginSerializer
from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import authenticate
from django.conf import settings
from .models import User, UserRole
from allauth.account.adapter import get_adapter
from rest_framework.validators import UniqueValidator
from allauth.account.models import EmailAddress




# ---------------------
# Register Serializer
# ---------------------
class CustomRegisterSerializer(RegisterSerializer):
    username = None  # remove username

    # extra fields
    name = serializers.CharField(max_length=255, required=False)
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    phone_number = serializers.CharField(max_length=20, required=False, allow_blank=True)
    profile_picture = serializers.ImageField(required=False, allow_null=True)

    # optional role
    if getattr(settings, "USE_ROLE", False):
        role = serializers.ChoiceField(choices=UserRole.choices, required=True)

    class Meta:
        model = User
        fields = (
            "email",
            "name",
            "phone_number",
            "profile_picture",
        ) + (("role",) if getattr(settings, "USE_ROLE", False) else ())

    # ---------------------
    # Validate email for duplicates
    # ---------------------
    def validate_email(self, email):
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError("A user with that email already exists.")
        return email

    # ---------------------
    # Collect cleaned data
    # ---------------------
    def get_cleaned_data(self):
        data = super().get_cleaned_data()
        data["email"] = self.validated_data.get("email", "")
        data["name"] = self.validated_data.get("name", "")
        data["phone_number"] = self.validated_data.get("phone_number", "")
        data["profile_picture"] = self.validated_data.get("profile_picture", None)
        if getattr(settings, "USE_ROLE", False):
            data["role"] = self.validated_data.get("role", UserRole.USER)
        return data

    # ---------------------
    # Save user via adapter
    # ---------------------
    def save(self, request):
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()
        adapter.save_user(request, user, self)

        # set extra fields
        user.name = self.cleaned_data.get("name", "")
        user.phone_number = self.cleaned_data.get("phone_number", "")
        user.profile_picture = self.cleaned_data.get("profile_picture", None)
        if getattr(settings, "USE_ROLE", False):
            user.role = self.cleaned_data.get("role", UserRole.USER)
        else:
            user.role = UserRole.USER

        user.save()
        return user


# ---------------------
# Login Serializer
# ---------------------
class CustomLoginSerializer(LoginSerializer):
    username = None
    email = serializers.EmailField(required=True)

    def validate(self, attrs):
        request = self.context.get("request")
        email = attrs.get("email")
        password = attrs.get("password")

        if not email or not password:
            raise serializers.ValidationError(
                _('Must include "email" and "password".'),
                code='authorization'
            )

        user = authenticate(request, email=email, password=password)
        if not user:
            raise serializers.ValidationError(
                _('Unable to log in with provided credentials.'),
                code='authorization'
            )

        # ----------- CHECK EMAIL VERIFICATION -----------
        if getattr(settings, "ACCOUNT_EMAIL_VERIFICATION", None) == "mandatory":
            email_address = EmailAddress.objects.filter(user=user, email=user.email).first()
            if not email_address or not email_address.verified:
                raise serializers.ValidationError(
                    _('Email address is not verified. Please verify your email first.'),
                    code='authorization'
                )

        attrs["user"] = user
        return attrs

# ---------------------
# User Response Serializer
# ---------------------
class UserResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'email',
            'name',
            'phone_number',
            'profile_picture',
            'role',
        ]
        read_only_fields = fields

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if not getattr(settings, 'USE_ROLE', False):
            data.pop('role', None)
        return data
