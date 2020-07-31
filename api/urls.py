from django.urls import path
from . import views


urlpatterns = [
    path('todos/', views.TodoListCreate.as_view()),
    path('todos/completed', views.TodoCompleted.as_view()),
    path('todos/<int:pk>', views.TodoListModify.as_view()),
    path('todos/<int:pk>/complete', views.TodoComplete.as_view()),

    #signup a user
    path('signup/', views.signup),
    path('login/', views.login),
]