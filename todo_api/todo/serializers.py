from rest_framework import serializers
from .models import Todo


class TodoSerializer(serializers.ModelSerializer):
    """
    Serializer for Todo.
    Read only fields = id, history
    """

    class Meta:
        model = Todo
        fields = ["task", "completed", "timestamp", "updated", "id", "finish_date", "user", "category"]
        read_only_fields = ('id', 'history',)


class FileSerializer(serializers.Serializer):
    """
    Serializer for data about file to send to remote server
    """
    file_name = serializers.CharField()
    file_name_to_server = serializers.CharField()
    url = serializers.URLField()


class FileTodbSerializer(serializers.Serializer):
    """
    Serializer for data about file to send to remote server
    """
    file_name = serializers.CharField()