from django.contrib import admin
from account.models import FarmerAccount, ExpertAccount


class FarmerAdmin(admin.ModelAdmin):
    model = FarmerAccount


class ExpertAdmin(admin.ModelAdmin):
    model = ExpertAccount


admin.site.register(FarmerAccount, FarmerAdmin)
admin.site.register(ExpertAccount, ExpertAdmin)
