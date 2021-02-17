from rest_framework import serializers
from .models import Todo


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
