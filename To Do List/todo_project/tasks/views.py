from rest_framework import generics, status, filters
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone
from django.db.models import Q, Count
from datetime import datetime, timedelta
import django_filters

from .models import Task, Category
from .serializers import TaskSerializer, CategorySerializer, TaskStatsSerializer


# Task Filtering
class TaskFilter(django_filters.FilterSet):
    priority = django_filters.ChoiceFilter(choices=Task.PRIORITY_CHOICES)
    category = django_filters.NumberFilter(field_name='category__id')
    is_done = django_filters.BooleanFilter()
    overdue = django_filters.BooleanFilter(method='filter_overdue')
    due_today = django_filters.BooleanFilter(method='filter_due_today')
    due_this_week = django_filters.BooleanFilter(method='filter_due_this_week')
    
    class Meta:
        model = Task
        fields = ['priority', 'category', 'is_done']
    
    def filter_overdue(self, queryset, name, value):
        if value:
            return queryset.filter(
                due_date__lt=timezone.now(),
                is_done=False
            )
        return queryset
    
    def filter_due_today(self, queryset, name, value):
        if value:
            today = timezone.now().date()
            return queryset.filter(due_date__date=today)
        return queryset
    
    def filter_due_this_week(self, queryset, name, value):
        if value:
            today = timezone.now().date()
            week_end = today + timedelta(days=7)
            return queryset.filter(
                due_date__date__range=[today, week_end]
            )
        return queryset


# Task Views
class TaskListCreateView(generics.ListCreateAPIView):
    serializer_class = TaskSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = TaskFilter
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'due_date', 'priority', 'order']
    ordering = ['order', '-created_at']
    permission_classes = [AllowAny]
    
    def get_queryset(self):
        return Task.objects.all().select_related('category')


class TaskRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TaskSerializer
    lookup_field = 'id'
    permission_classes = [AllowAny]
    
    def get_queryset(self):
        return Task.objects.all().select_related('category')


# Category Views
class CategoryListCreateView(generics.ListCreateAPIView):
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]
    
    def get_queryset(self):
        return Category.objects.all().prefetch_related('tasks')


class CategoryRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CategorySerializer
    lookup_field = 'id'
    permission_classes = [AllowAny]
    
    def get_queryset(self):
        return Category.objects.all().prefetch_related('tasks')


# Task Statistics
@api_view(['GET'])
@permission_classes([AllowAny])
def task_stats(request):
    total = Task.objects.count()
    completed = Task.objects.filter(is_done=True).count()
    pending = total - completed
    
    # Calculate overdue tasks
    overdue = Task.objects.filter(
        due_date__lt=timezone.now(),
        is_done=False
    ).count()
    
    # Calculate completion rate
    completion_rate = (completed / total * 100) if total > 0 else 0
    
    # Today's completed tasks
    today = timezone.now().date()
    today_completed = Task.objects.filter(
        completed_at__date=today
    ).count()
    
    # This week's completed tasks
    week_start = today - timedelta(days=today.weekday())
    this_week_completed = Task.objects.filter(
        completed_at__date__gte=week_start
    ).count()
    
    stats = {
        'total': total,
        'completed': completed,
        'pending': pending,
        'overdue': overdue,
        'completion_rate': round(completion_rate, 1),
        'today_completed': today_completed,
        'this_week_completed': this_week_completed,
    }
    
    serializer = TaskStatsSerializer(stats)
    return Response(serializer.data)


# Bulk Operations
@api_view(['PATCH'])
@permission_classes([AllowAny])
def bulk_update_tasks(request):
    task_ids = request.data.get('task_ids', [])
    update_data = request.data.get('update_data', {})
    
    if not task_ids:
        return Response(
            {'error': 'task_ids is required'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    tasks = Task.objects.filter(id__in=task_ids)
    
    if not tasks.exists():
        return Response(
            {'error': 'No tasks found'}, 
            status=status.HTTP_404_NOT_FOUND
        )
    
    # Update tasks
    updated_count = tasks.update(**update_data)
    
    return Response({
        'message': f'Updated {updated_count} tasks',
        'updated_count': updated_count
    })
