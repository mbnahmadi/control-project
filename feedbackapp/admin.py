from django.contrib import admin
from django.contrib.admin import ModelAdmin
from .models import FeedBackModel, FeedBackResponseModel
# Register your models here.

@admin.register(FeedBackModel)
class FeedBackAdmin(admin.ModelAdmin):
    list_display = ['pk', 'through', 'date']
    # list_filter = ['project', 'through', 'date']

# def get_company_name(self, obj):
#     return obj.project.company_name
# get_company_name.short_description = 'company'

# def get_location(self, obj):
#     return obj.project.location
# get_location.short_description = 'location'

@admin.register(FeedBackResponseModel)
class FeedBackResponseAdmin(admin.ModelAdmin):
    list_display = ['pk', 'through', 'date']
    # list_filter = ['project', 'through', 'date']