from django.contrib import admin
from account.models import FarmerAccount, ExpertAccount


class FarmerAdmin(admin.ModelAdmin):
    model = FarmerAccount
    list_display = ('__str__', 'state', 'major_crop_list', 'email_confirmed', 'phone_confirmed')
    list_filter = ('email_confirmed', 'phone_confirmed')
    list_editable = ('email_confirmed', 'phone_confirmed')


class ExpertAdmin(admin.ModelAdmin):
    model = ExpertAccount
    list_display = ('__str__', 'state', 'skills_list', 'email_confirmed', 'phone_confirmed')
    list_filter = ('email_confirmed', 'phone_confirmed')
    list_editable = ('email_confirmed', 'phone_confirmed')


admin.site.register(FarmerAccount, FarmerAdmin)
admin.site.register(ExpertAccount, ExpertAdmin)
