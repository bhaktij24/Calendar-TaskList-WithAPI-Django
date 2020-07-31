from django.forms import ModelForm
from .models import TodoList

class TodoForm(ModelForm):
    class Meta:
        model = TodoList
        fields = ['title','memo','important']