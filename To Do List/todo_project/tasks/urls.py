from django.urls import path
from . import views

urlpatterns = [
    # Tasks
    path('tasks/', views.TaskListCreateView.as_view(), name='task-list-create'),
    path('tasks/<int:id>/', views.TaskRetrieveUpdateDestroyView.as_view(), name='task-detail'),
    path('tasks/stats/', views.task_stats, name='task-stats'),
    path('tasks/bulk/', views.bulk_update_tasks, name='bulk-update-tasks'),
    
    # Categories
    path('categories/', views.CategoryListCreateView.as_view(), name='category-list-create'),
    path('categories/<int:id>/', views.CategoryRetrieveUpdateDestroyView.as_view(), name='category-detail'),
]
