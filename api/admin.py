from django.contrib import admin

from .models import Company, Opportunity, Subscription, Favourate, JobCategory


admin.site.register(Company)
admin.site.register(Opportunity)
admin.site.register(Subscription)
admin.site.register(Favourate)
admin.site.register(JobCategory)
