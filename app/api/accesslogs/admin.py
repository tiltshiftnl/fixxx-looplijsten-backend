from django.contrib import admin

from api.accesslogs.models import LogEntry


@admin.register(LogEntry)
class LogEntryAdmin(admin.ModelAdmin):
    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False

    search_fields = ('request_user_email', 'request_uri',)

    list_display = ('request_uri', 'request_method', 'response_status_code',
                    'request_user_email', 'created_at')

    fields = ('request_user_email', 'request_user_id',
              'request_uri', 'request_method', 'request_meta', 'response_status_code', 'created_at')

    readonly_fields = fields
