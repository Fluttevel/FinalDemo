from django.contrib import admin

from .models import Profile, ServiceProviders, Services, LastCounterReading, \
    HistoryElectricityCR, HistoryWaterCR, HistoryGasCR

admin.site.register(Profile)
admin.site.register(ServiceProviders)
admin.site.register(Services)
admin.site.register(LastCounterReading)
admin.site.register(HistoryElectricityCR)
admin.site.register(HistoryWaterCR)
admin.site.register(HistoryGasCR)
