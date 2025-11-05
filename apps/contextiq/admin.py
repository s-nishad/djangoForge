from django.contrib import admin

from .models import Document

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'user', 'parse_content_status', 'created_at')
    list_filter = ('parse_content_status', 'created_at', 'user')
    search_fields = ('title', 'user__username', 'parse_content')
    readonly_fields = ('created_at', 'updated_at')
