from django.contrib import admin
from .models import Farmer, Expert


class something(admin.ModelAdmin):
    fieldsets = [
        ('Name', {'fields': ['first_name', 'last_name']}),
    ]


admin.site.register(Expert)
admin.site.register(Farmer, something)
