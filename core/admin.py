from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User
from .models import ChatbotLog

class UserAdmin(BaseUserAdmin):
    fieldsets = BaseUserAdmin.fieldsets + (
        (None, {'fields': ('role', 'phone')}),
    )

admin.site.register(User, UserAdmin)


@admin.register(ChatbotLog)
class ChatbotLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'message_short', 'response_short', 'created_at')
    list_filter = ('created_at', 'user')
    search_fields = ('message', 'response', 'user__username')
    ordering = ('-created_at',)

    def message_short(self, obj):
        return (obj.message[:50] + '...') if len(obj.message) > 50 else obj.message
    message_short.short_description = 'Message'

    def response_short(self, obj):
        return (obj.response[:50] + '...') if len(obj.response) > 50 else obj.response
    response_short.short_description = 'Réponse'
