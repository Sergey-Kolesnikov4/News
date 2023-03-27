from django.contrib import admin
from .models import Category,News,Comment,Author

class NewsAdmin(admin.ModelAdmin):
    list_display = ('title','author')
    list_filter = ('category', 'title')
    search_fields = ('title', 'category__name')

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']

admin.site.register(Category,CategoryAdmin)
admin.site.register(News,NewsAdmin)
admin.site.register(Comment)
admin.site.register(Author)


