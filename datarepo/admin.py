from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser, Newsfeed


# Register your models here.


class CustomUserAdmin(UserAdmin):
    list_display = ('id', 'phone_number')


UserAdmin.fieldsets += (
    (
        'custom_fields', {
            'fields': ('phone_number',)
        }
    ),
)

admin.site.register(CustomUser, CustomUserAdmin)


@admin.register(Newsfeed)
class NewsfeedAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'news')

