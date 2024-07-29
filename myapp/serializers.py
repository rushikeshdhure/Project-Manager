from rest_framework import serializers
from django.contrib.auth.models import User
from .models import User, Client, Project

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['name', 'email' ]
        extra_kwargs = {'password': {'write_only': True}}


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'  # Or specify the fields you want to include, e.g., ['client_name', 'name', 'email']



class ProjectSerializer(serializers.ModelSerializer):
     class Meta:
        model = Project
        fields = ['id', 'name']

# class ProjectCreateSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Project
#         fields = ['name', 'user', 'client']     

class ProjectCreateSerializer(serializers.ModelSerializer):
    client_id = serializers.IntegerField(write_only=True)
    users = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), many=True)

    class Meta:
        model = Project
        fields = ['name', 'client_id', 'users']
    
    def create(self, validated_data):
        client_id = validated_data.pop('client_id')
        client = Client.objects.get(id=client_id)
        users = validated_data.pop('users')
        project = Project.objects.create(client=client, **validated_data)
        project.users.set(users)
        return project






class ClientSerializer(serializers.ModelSerializer):
    created_by = serializers.SerializerMethodField()
    projects = ProjectSerializer(many=True, read_only=True)
    class Meta:
        model = Client
        fields = ['id', 'client_name', 'projects', 'created_at', 'created_by', 'updated_at']


    def get_created_by(self, obj):
            return obj.created_by.name if obj.created_by else None
    
class ClientCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ['client_name', 'created_by']


class ClientUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ['client_name']
