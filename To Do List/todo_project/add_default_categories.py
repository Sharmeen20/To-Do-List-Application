import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'todo_project.settings')
django.setup()

from tasks.models import Category

def add_default_categories():
    default_categories_data = [
        {'name': 'Personal', 'color': '#10B981'},
        {'name': 'Work', 'color': '#3B82F6'},
        {'name': 'Shopping', 'color': '#8B5CF6'},
        {'name': 'Health', 'color': '#EF4444'},
        {'name': 'Study', 'color': '#F59E0B'},
        {'name': 'Home', 'color': '#6B7280'},
    ]

    created_count = 0
    for cat_data in default_categories_data:
        category, created = Category.objects.get_or_create(
            name=cat_data['name'],
            defaults={'color': cat_data['color']}
        )
        if created:
            print(f"✅ Created category: {category.name}")
            created_count += 1
        else:
            print(f"⚠️  Category already exists: {category.name}")
    
    print(f"\n🎉 Added {created_count} new categories!")
    print(f"📊 Total categories: {Category.objects.count()}")

if __name__ == '__main__':
    add_default_categories()
