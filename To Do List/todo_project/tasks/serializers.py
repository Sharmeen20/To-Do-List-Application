from rest_framework import serializers
from .models import Task, Category


class CategorySerializer(serializers.ModelSerializer):
    task_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Category
        fields = ['id', 'name', 'color', 'task_count', 'created_at']
        read_only_fields = ['id', 'created_at']
    
    def get_task_count(self, obj):
        return obj.tasks.filter(is_done=False).count()


class TaskSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    category_color = serializers.CharField(source='category.color', read_only=True)
    is_overdue = serializers.ReadOnlyField()
    days_until_due = serializers.ReadOnlyField()
    
    class Meta:
        model = Task
        fields = [
            'id', 'title', 'description', 'is_done', 'priority',
            'due_date', 'category', 'category_name', 'category_color',
            'created_at', 'updated_at', 'completed_at', 'is_overdue',
            'days_until_due', 'order'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'completed_at']


class TaskStatsSerializer(serializers.Serializer):
    total = serializers.IntegerField()
    completed = serializers.IntegerField()
    pending = serializers.IntegerField()
    overdue = serializers.IntegerField()
    completion_rate = serializers.FloatField()
    today_completed = serializers.IntegerField()
    this_week_completed = serializers.IntegerField()
