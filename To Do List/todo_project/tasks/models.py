from django.db import models
from django.utils import timezone
from django.core.validators import MaxLengthValidator


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    color = models.CharField(max_length=7, default='#3B82F6', help_text="Hex color code")
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']


class Task(models.Model):
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]
    
    title = models.CharField(max_length=200, validators=[MaxLengthValidator(200)])
    description = models.TextField(blank=True, null=True)
    is_done = models.BooleanField(default=False)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    due_date = models.DateTimeField(null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='tasks')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    order = models.PositiveIntegerField(default=0)
    
    def save(self, *args, **kwargs):
        if self.is_done and not self.completed_at:
            self.completed_at = timezone.now()
        elif not self.is_done:
            self.completed_at = None
        super().save(*args, **kwargs)
    
    @property
    def is_overdue(self):
        if self.due_date and not self.is_done:
            return timezone.now() > self.due_date
        return False
    
    @property
    def days_until_due(self):
        if self.due_date and not self.is_done:
            delta = self.due_date - timezone.now()
            return delta.days
        return None
    
    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['order', '-created_at']
        indexes = [
            models.Index(fields=['is_done']),
            models.Index(fields=['category']),
            models.Index(fields=['due_date']),
        ]
