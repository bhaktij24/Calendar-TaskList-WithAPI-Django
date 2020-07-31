"""TodoTasklist URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from todo import views

urlpatterns = [
    path('admin/', admin.site.urls),
    #signup,login, logout
    path('signup/', views.signup_user, name='signupUser'),
    path('login/', views.login_user, name='loginUser'),
    path('logout/', views.logout_user, name='logoutUser'),

    #todos, create, view & upadte
    path('', views.home_page, name='homePage'),
    path('currenttodos/', views.currenttodos, name='currenttodos'),    
    path('newItem/', views.create_todo, name='createTodo'),
    path('todo/<int:todo_pk>', views.view_todos, name='viewtodos'),
    path('todo/<int:todo_pk>/complete', views.complete_todos, name='completetodos'),
    path('completed/', views.completed_todos, name='completedtodos'),
    path('todo/<int:todo_pk>/delete', views.delete_todos, name='deletetodos'),

    #API
    path('api/',include('api.urls')),

]
