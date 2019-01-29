from django.contrib import admin
from oauth.models import Farmer


class FarmerAdmin(admin.ModelAdmin):
    model = Farmer
    list_display = ('__str__', )


admin.site.register(Farmer, FarmerAdmin)
