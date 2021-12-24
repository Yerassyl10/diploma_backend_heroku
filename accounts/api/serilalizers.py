from rest_framework import serializers
from accounts.models import Users

class RegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = Users
        fields = ['email', 'password', 'password2']
        extra_kwargs = {'password': {'write_only': True} }

    def save(self):
        account = Users(email=self.validated_data['email'],)
        password1 = self.validated_data['password']
        password2 = self.validated_data['password2']

        if password1 != password2:
            raise serializers.ValidationError({'password: Passwords must match.'})
        account.set_password(password1)
        account.save()
        return account


class ChangePasswordSerializer(serializers.Serializer):
    model = Users

    oldPassword = serializers.CharField(required=True)
    newPassword = serializers.CharField(required=True)


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = Users
        fields = ('id',
                  'email',
                  'first_name',
                  'last_name',
                  'birthday',
                  'zipcode',
                  'contact_number',
                  'prof_image',
                  'prof_cv'
                  )

