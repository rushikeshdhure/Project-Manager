from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework import generics,status
from rest_framework.decorators import api_view
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .serializers import UserSerializer, ClientSerializer,ClientCreateSerializer,ProjectCreateSerializer,ClientUpdateSerializer
from .models import User, Client, Project
from datetime import datetime
import datetime
from django.http import JsonResponse

from rest_framework.permissions import AllowAny



import jwt
from functools import wraps
from rest_framework.exceptions import AuthenticationFailed

from .models import User



def jwt_authentication_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            raise AuthenticationFailed('Unauthenticated!')

        try:
            token = token.split(" ")[1]
            decoded_token = jwt.decode(token, 'secret', algorithms=['HS256'])
            user_id = decoded_token.get('id')
            user = User.objects.get(pk=user_id)
            request.user = user
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')
        except jwt.InvalidTokenError:
            raise AuthenticationFailed('Invalid token!')
        except User.DoesNotExist:
            raise AuthenticationFailed('User not found!')

        return view_func(request, *args, **kwargs)

    return wrapper




class UserRegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        # return Response(serializer.data)
        return Response({
            'message': 'User registered successfully',
            'user': serializer.data
        })
    
from .serializers import UserCreateSerializer

class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    print(queryset)
    serializer_class = UserCreateSerializer



from .models import User
class UserLoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        phone_number = request.data.get('phone_number')
        password = request.data.get('password')

        if not (email or phone_number):
            raise AuthenticationFailed('Email or phone number is required!')

        if email:
            # If email is provided, search for the user by email
            user = User.objects.filter(email=email).first()
        else:
            # If email is not provided but phone number is, search for the user by phone number
            user = User.objects.filter(phone_number=phone_number).first()

        if user is None:
            raise AuthenticationFailed('User not found!')

        # if not user.check_password(password):
        #     raise AuthenticationFailed('Incorrect password!')

        # Create a JWT token
        payload = {
            'id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=30),
            'iat': datetime.datetime.utcnow()
        }
        token = jwt.encode(payload, 'secret', algorithm='HS256')

        # Return the JWT token in the response
        response_data = {
            'message': 'Login successful',
            'token': token,
            'user_id': user.id
        }
        response = JsonResponse(response_data)

        # Set the JWT token as a cookie
        response.set_cookie(key='jwt', value=token, httponly=True)

        return response

class UserLogoutView(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message': 'logout success'
        }
        return response



from .models import Client
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated

class ClientRegisterView(generics.CreateAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientCreateSerializer

class ClientListView(generics.ListAPIView):
    queryset = Client.objects.all()
    print(queryset)
    serializer_class = ClientCreateSerializer

class ClientDetailView(generics.RetrieveAPIView):
    queryset = Client.objects.all()
    print(queryset)
    serializer_class = ClientSerializer

class ClientUpdateView(generics.UpdateAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientUpdateSerializer
    permission_classes = [AllowAny]

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return ClientUpdateSerializer
        return ClientSerializer

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        updated_instance = ClientSerializer(instance)
        return Response(updated_instance.data, status=status.HTTP_200_OK)

class ClientDeleteView(generics.DestroyAPIView):
    queryset = Client.objects.all()
    permission_classes = [AllowAny]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

# class ProjectCreateView(generics.CreateAPIView):
#     queryset = Project.objects.all()
#     print(queryset)
#     serializer_class = ProjectSerializer
from rest_framework.permissions import AllowAny
class ProjectCreateView(generics.CreateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectCreateSerializer
    permission_classes = [AllowAny] 

    def perform_create(self, serializer):
        serializer.save() 

class ProjectListView(generics.ListAPIView):
    queryset = Project.objects.all()
    print(queryset)
    serializer_class = ProjectCreateSerializer


@api_view(['GET'])
@jwt_authentication_required
def get_all_data(request):
    data = User.objects.all()
    print(data)