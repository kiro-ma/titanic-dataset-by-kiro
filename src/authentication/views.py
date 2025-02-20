from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.db import IntegrityError, transaction
from django.contrib.auth.models import User
from .serializers import UserSerializer


class Home(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        content = {'message': 'Você está autenticado!'}
        return Response(content)
    
    def post(self, request):
        user_obj = request.data

        try:
            with transaction.atomic():
                User.objects.create_user(**user_obj)

            return Response(status=201)

        except IntegrityError as e:
            print(f"Integrity error: {e}")
            return Response({"detail": "Dados inválidos ou duplicados."}, status=400)

        except Exception as e:
            print(f"Error: {e}")
            return Response({"detail": "Ocorreu um erro ao criar o usuário."}, status=500)


class UserViewSet(ViewSet):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return User.objects.all()

    def list(self, request):
        queryset = self.get_queryset()
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def self(self, request):
        user = self.get_queryset().filter(username=request.user.username).first()
        serializer = UserSerializer(user)
        return Response(serializer.data)
