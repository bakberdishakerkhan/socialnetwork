from django.contrib import admin
from .models import News, PostAttachment
# Register your models here.

@admin.register(PostAttachment)
class PostAttachmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'post', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name', 'post__title')
    raw_id_fields = ('post',)
    
    fields = ('name', 'image', 'post')

@admin.register(News)
class CustomPostAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Основная информация', {'fields' : ('title', 'content')}),
        ('Дополнительные поля', {'fields' : ('edited', 'publication_date')}),
    )
    add_fieldsets = (
        ('Основная информация', {'fields' : ('title', 'content')}),
    )

    list_display = ('title', 'publication_date', 'edited')
    search_fields = ('title', 'content')
    ordering = ('-publication_date',)
    def get_fieldsets(self, request, obj = None):
        if obj:
            return self.fieldsets
        return self.add_fieldsets
    

