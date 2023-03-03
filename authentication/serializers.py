from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class WyseTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user: User):
        token = super().get_token(user)

        # Add custom claims
        token['id'] = user.id
        token['email'] = user.email
        token['username'] = user.username
        token['first_name'] = user.first_name
        token['last_name'] = user.last_name
        token['designation'] = user.profile.system_role_id.SystemRole

        return token


class ChangePasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    confirm_password = serializers.CharField(write_only=True, required=True)
    old_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('old_password', 'password', 'confirm_password')

    def validate(self, attrs):
        """
        Raise error if password and confirm_password fields are different.
        """
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError(
                {
                    'password': "Password fields didn't match."
                }
            )

        return attrs

    def validate_old_password(self, value):
        """
        Check if old password is correct.
        """
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError(
                {
                    "old_password": "Old password is not correct."
                }
            )
        return value

    def update(self, instance, validated_data):
        """
        Update user password
        """
        instance.set_password(validated_data['password'])
        instance.save()
        return instance
