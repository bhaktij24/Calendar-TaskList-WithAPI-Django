from rest_framework import serializers
from todo.models import TodoList

class TodoSerializer(serializers.ModelSerializer):

    created = serializers.ReadOnlyField()
    dateCompleted = serializers.ReadOnlyField()
    class Meta:
        model = TodoList
        fields = ['id','title','memo','created','dateCompleted','important']


class TodoCompleteSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = TodoList
        fields = ['id']
        read_only_fields = ['title','memo','created','dateCompleted','important']
