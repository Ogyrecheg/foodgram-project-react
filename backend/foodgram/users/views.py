from djoser.views import UserViewSet
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import api_view, permission_classes

from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView

from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

from .models import User, Follow
from .pagination import CustomUserPagination
from .serializers import CustomUserSerializer, EmailTokenObtainSerializer, CustomAuthTokenSerializer, FollowSerializer, \
    CustomFollowUserSerializer, SubscriptionsSerializer


class CustomUserViewSet(UserViewSet):
    pagination_class = CustomUserPagination
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = EmailTokenObtainSerializer


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
        request.user.auth_token.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


class FollowView(APIView):
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

    def delete(self, request, id):
        user_id = request.user.id
        author_id = id
        follow = Follow.objects.filter(user=user_id, author=author_id)

        if not follow.exists():

            return Response('Вы не подписаны на данного автора!', status=status.HTTP_400_BAD_REQUEST)

        follow.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
@permission_classes([AllowAny])
def subscriptions(request):
    user = request.user
    follows = User.objects.filter(author__user=user)
    paginator = CustomUserPagination()
    result = paginator.paginate_queryset(follows, request, view=None)

    serializer = SubscriptionsSerializer(
        result,
        many=True,
        context={'request': request},
    )

    return paginator.get_paginated_response(serializer.data)

