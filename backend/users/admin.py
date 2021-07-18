from django.contrib import admin

from .models import CustomUser


class CustomUserAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'username',
        'first_name',
        'last_name',
        'email',
        'password'
    )
    list_filter = ('email', 'username')


admin.site.register(CustomUser, CustomUserAdmin)
