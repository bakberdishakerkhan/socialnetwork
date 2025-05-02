from django.contrib import admin
from .models import Chat

@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = ('id', 'sender', 'receiver', 'content', 'timestamp')
    list_filter = ('sender', 'receiver', 'timestamp')
    search_fields = ('sender__username', 'receiver__username', 'content')
    ordering = ('-timestamp',)
