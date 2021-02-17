from rest_framework import serializers
from .models import Todo


class TodoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Todo
        fields = ["task", "completed", "timestamp", "updated", "id", "finish_date", "user", "category"]
        read_only_fields = ('id', 'history',)

    def validate_start_date(self, value):
        if self.instance and self.instance.start_date < value:
            raise serializers.ValidationError(
                "After create poll you can't change start date"
            )

        return value


class FileSerializer(serializers.Serializer):
    file_name = serializers.CharField()
    file_name_to_server = serializers.CharField()
    url = serializers.URLField()