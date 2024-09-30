from rest_framework import viewsets
from artigo.models import Artigo
from artigo.serializers import UserSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework import status
from django.contrib.auth import authenticate



class ArtigoViewSets(viewsets.ModelViewSet):
    queryset = Artigo.objects.all().order_by('-data')
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]  # Garante que só usuários autenticados possam acessar a API


class ObtainAuthTokenView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)

        if user is not None:
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_200_OK)
        return Response({'error': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)

