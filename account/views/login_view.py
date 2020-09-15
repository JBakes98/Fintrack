from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from account.serializers import LoginSerializer, TokenSerializer
from account.services import AccountService


class LoginView(GenericAPIView):
    """
    Check the credentials and return the REST Token
    if the credentials are valid and authenticated.

    Accept the following POST parameters: username, password
    Return the REST Framework Token Object's key.
    """
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer
    token_model = Token

    def dispatch(self, *args, **kwargs):
        return super(LoginView, self).dispatch(*args, **kwargs)

    def get_response_serializer(self):
        response_serializer = TokenSerializer
        return response_serializer

    def login(self):
        self.user = self.serializer.validated_data['user']
        self.token = AccountService(email=self.user.email).create_user_token()

    def get_response(self):
        serializer_class = self.get_response_serializer()
        serializer = serializer_class(
            instance=self.token,
            context={'request': self.request}
        )
        response = Response(serializer.data, status=status.HTTP_200_OK)

        return response

    def post(self, request, *args, **kwargs):
        self.request = request
        self.serializer = self.get_serializer(data=self.request.data, context={'request': request})
        self.serializer.is_valid(raise_exception=True)
        self.login()

        return self.get_response()
