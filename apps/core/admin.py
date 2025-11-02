from django.contrib import admin

from apps.core.models import ApiKey

@admin.register(ApiKey)
class ApiKeyAdmin(admin.ModelAdmin):
    pass