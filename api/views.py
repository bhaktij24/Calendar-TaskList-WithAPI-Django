from django.shortcuts import render
from rest_framework import generics, permissions
from .serializers import TodoSerializer, TodoCompleteSerializer
from django.contrib.auth import authenticate
from todo.models import TodoList
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http import JsonResponse
from django.db import IntegrityError
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

@csrf_exempt
def signup(request):
    if request.method == "POST":
        try:
            data = JSONParser().parse(request)
            user = User.objects.create_user(data['username'], password=data['password'])
            user.save()
            token = Token.objects.create(user=user)
            return JsonResponse({'token':str(token)}, status=201)

        except IntegrityError:
            return JsonResponse({'error': "Username already taken. Please try some other username or login with the same username."}, status=400)



@csrf_exempt
def login(request):
    if request.method == "POST":
            data = JSONParser().parse(request)
            user = authenticate(request, username=data['username'], password=data['password'])
            if user is None:
                return JsonResponse({'error': "Please check username or password is entered correctly"}, status=400)
            else:
                try:
                    token = Token.objects.get(user=user)
                except:
                    token = Token.objects.create(user=user)
                return JsonResponse({'token':str(token)}, status=201)

# Create your views here.

class TodoCompleted(generics.ListAPIView):
    serializer_class = TodoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return TodoList.objects.filter(user=user, dateCompleted__isnull=False).order_by('-dateCompleted')

class TodoListCreate(generics.ListCreateAPIView):
    serializer_class = TodoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return TodoList.objects.filter(user=user, dateCompleted__isnull=True) 

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class TodoListModify(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TodoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return TodoList.objects.filter(user=user) 

class TodoComplete(generics.UpdateAPIView):
    serializer_class = TodoCompleteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return TodoList.objects.filter(user=user) 

    def perform_update(self, serializer):
        serializer.instance.dateCompleted = timezone.now()
        serializer.save()
