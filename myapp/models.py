from django.db import models
from django.contrib.auth.models import User

class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    address = models.TextField()
    password = models.CharField(max_length=128)#  default=True


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    # def __str__(self):
    #     return self.name
    


class Client(models.Model):
    client_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name='created_clients', on_delete=models.SET_NULL, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    # def __str__(self):
    #     return self.client_name

class Project(models.Model):
    name = models.CharField(max_length=255)
    user = models.ForeignKey(User, related_name='projects', on_delete=models.CASCADE)
    client = models.ForeignKey(Client, related_name='projects', on_delete=models.CASCADE)

    # client = models.ForeignKey(Client, related_name='projects', on_delete=models.CASCADE)
    # created_by = models.ForeignKey(User, related_name='created_projects', on_delete=models.SET_NULL, null=True)

    
    # def __str__(self):
    #     return self.name



