from rest_framework import serializers
from .models import Todo, InventoryFile


class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = ["task", "completed", "timestamp", "updated", "user", "id", "finish_date"]
        read_only_fields = ('id',)

    def validate_start_date(self, value):
        if self.instance and self.instance.start_date < value:
            raise serializers.ValidationError(
                "After create poll you can't change start date"
            )

        return value


class InventoryFile_Serializer(serializers.ModelSerializer):

    class Meta:
        model = InventoryFile
        fields = ('shop_inventory', 'todo')


class FileSerializer(serializers.Serializer):
    file_name = serializers.CharField()
    file_name_to_server = serializers.CharField()
    url = serializers.URLField()
