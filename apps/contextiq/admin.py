from django.contrib import admin

from .models import Document, queryLog

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'user', 'parse_content_status', 'created_at')
    list_filter = ('parse_content_status', 'created_at', 'user')
    search_fields = ('title', 'user__email', 'parse_content')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(queryLog)
class QueryLogAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'short_query_text', 'short_response_text', 'created_at')
    list_filter = ('created_at', 'user')
    search_fields = ('query_text', 'response_text', 'user__email')
    readonly_fields = ('created_at', 'updated_at')
    exclude = ['is_active'] 

    # response or query in shortented form
    def short_response_text(self, obj):
        return (obj.response_text[:75] + '...') if len(obj.response_text) > 75 else obj.response_text   
    short_response_text.short_description = 'Response Text'
    
    def short_query_text(self, obj):
        return (obj.query_text[:75] + '...') if len(obj.query_text) > 75 else obj.query_text
    short_query_text.short_description = 'Query Text'