from rest_framework import serializers

from accounts.models import Account


class RegistrationSerializer(serializers.ModelSerializer):

    password2 = serializers.CharField(style={'input_type': 'password'}, write_only = True)

    class Meta:
        model = Account
        fields = ['email', 'username', 'password', 'password2']
        extra_kwargs = { 
            'password' : {'write_only': True} ,
            }

    def save(self):
        account = Account(
            email = self.validated_data['email'],
            username = self.validated_data['username']
        )

        password = self.validated_data['password']
        password2 = self.validated_data['password2']

        if password != password2:
            raise serializers.ValidationError({'password': 'passwords must match'})

        account.set_password(password)
        account.save()

        return account






#######################################################################
#new code for authorization
######################################################################


# from django.contrib.auth import get_user_model
# from rest_framework import serializers
# from rest_auth.serializers import LoginSerializer

# try:
#     from allauth.utils import email_address_exists
#     from allauth.account.adapter import get_adapter
#     from allauth.account.utils import setup_user_email
# except ImportError:
#     raise ImportError("allauth needs to be added to INSTALLED_APPS.")

# User = get_user_model()




# class CustomRegisterSerializer(serializers.Serializer):
#     """
#     Modified RegisterSerializer class from rest_auth
#     """

#     username = None
#     first_name = serializers.CharField(required=True)
#     last_name = serializers.CharField(required=True)
#     email = serializers.EmailField(required=True)
#     password1 = serializers.CharField(write_only=True, style={"input_type": "password"})
#     password2 = serializers.CharField(write_only=True, style={"input_type": "password"})

#     def validate_email(self, email):
#         email = get_adapter().clean_email(email)
#         if email and email_address_exists(email):
#             raise serializers.ValidationError(
#                 "A user is already registered with this e-mail address."
#             )
#         return email

#     def validate_password1(self, password):
#         return get_adapter().clean_password(password)

#     def validate(self, data):
#         if data["password1"] != data["password2"]:
#             raise serializers.ValidationError("The two password fields didn't match.")
#         return data

#     def get_cleaned_data(self):
#         return {
#             "first_name": self.validated_data.get("first_name", ""),
#             "last_name": self.validated_data.get("last_name", ""),
#             "password1": self.validated_data.get("password1", ""),
#             "email": self.validated_data.get("email", ""),
#         }

#     def save(self, request):
#         adapter = get_adapter()
#         user = adapter.new_user(request)
#         self.cleaned_data = self.get_cleaned_data()
#         adapter.save_user(request, user, self)
#         setup_user_email(request, user, [])
#         return user
