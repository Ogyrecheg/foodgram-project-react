from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

from .models import User
from .pagination import CustomUserPagination
from .serializers import CustomUserSerializer, EmailTokenObtainSerializer, CustomAuthTokenSerializer, FollowSerializer


class CustomUserViewSet(UserViewSet):
    pagination_class = CustomUserPagination
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = EmailTokenObtainSerializer


class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        tokens = OutstandingToken.objects.filter(user_id=request.user.id)
        for token in tokens:
            t, _ = BlacklistedToken.objects.get_or_create(token=token)

        return Response(status=status.HTTP_204_NO_CONTENT)


class CustomObtainAuthToken(ObtainAuthToken):
    serializer_class = CustomAuthTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        content = {'auth_token': token.key}

        return Response(content, status=status.HTTP_201_CREATED)


class Logout(APIView):
    def post(self, request):
        # simply delete the token to force a login
        request.user.auth_token.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class Follow(APIView):
    def post(self, request, id):
        user_id = request.user.id
        author_id = id
        data = {'user': user_id, 'author': author_id}
        serializer = FollowSerializer(data=data, context={'request': request}
                                      )
        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
