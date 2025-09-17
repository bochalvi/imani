from django.contrib import admin
from .models import Member
from django.utils.translation import gettext_lazy as _


class MemberAdmin(admin.ModelAdmin):
    list_display = ('member_id', 'first_name', 'last_name',
                    'email', 'phone', 'member_type', 'is_active')
    search_fields = ('first_name', 'last_name', 'phone_number')
    list_filter = ('is_active', 'member_type')
    prepopulated_fields = {'slug': ('first_name', 'last_name')}


# Register your models here.

admin.site.register(Member, MemberAdmin)
