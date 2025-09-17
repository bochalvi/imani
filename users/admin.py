
from django.contrib import admin
from .models import Invitation


# Register your models here.


class InvitationAdmin(admin.ModelAdmin):
    list_display = ('inviter', 'email', 'token',
                    'created_at', 'expires_at', 'is_used')
    search_fields = ('inviter__username', 'email')
    list_filter = ('is_used', 'created_at')


admin.site.register(Invitation, InvitationAdmin)


class PasswordResetAdmin(admin.ModelAdmin):
    list_display = ('user', 'reset_id', 'created_when')
    search_fields = ('user__username',)
    list_filter = ('created_when',)
