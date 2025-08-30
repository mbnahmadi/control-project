from django.contrib import admin
from import_export.admin import ExportMixin, ExportActionMixin
from import_export import resources, fields
from .models import CompanyModel, DayFormatModel, ProjectModel
from feedbackapp.models import FeedBackModel, FeedBackResponseModel, FeedBackAttachment
from rangefilter.filters import DateRangeFilter
from feedbackapp.filters import HasFeedBackFilter

from nested_admin import NestedTabularInline, NestedModelAdmin

# Register your models here.
class ProjectResource(resources.ModelResource):
    company_name = fields.Field(column_name='company', attribute='company_name__name', readonly=True)
    description = fields.Field(column_name='description', attribute='description')
    # image_description = fields.Field(
    #     column_name='image uploaded',
    #     attribute='image_description.url'
    # )
    start_date = fields.Field(column_name='start date', attribute='start_date')
    end_date = fields.Field(column_name='end date', attribute='end_date')
    # total_days_display = fields.Field(
    #     column_name='total days',
    #     attribute='total_days',
    #     readonly=True
    # )
    location = fields.Field(column_name='location', attribute='location')
    start_cycle_display = fields.Field(column_name='start cycle', attribute='start_cycle', readonly=True)
    end_cycle_display = fields.Field(column_name='end cycle', attribute='end_cycle', readonly=True)
    # total_cycle_display = fields.Field(
    #     column_name='total cycle',
    #     attribute='total_cycle',
    #     readonly=True
    # )
    days_format = fields.Field(column_name='day format', attribute='days_format__format_name', readonly=True)

    class Meta:
        model = ProjectModel
        fields = (
            'id',
            'company_name',
            'description',
            # 'image_description',
            'start_date',
            'end_date',
            'total_days',
            'location',
            'start_cycle_display',
            'end_cycle_display',
            'total_cycle',
            'days_format',
            # 'is_active'
        )
        export_order = (
            'id',
            'company_name',
            'description',
            # 'image_description',
            'start_date',
            'end_date',
            'total_days',
            'location',
            'start_cycle_display',
            'end_cycle_display',
            'total_cycle',
            'days_format'
        )

    def dehydrate_start_cycle_display(self, obj):
        return obj.get_start_cycle_display()

    def dehydrate_end_cycle_display(self, obj):
        return obj.get_end_cycle_display()


# --------------- model admin -----------------
# class FeedBackInline(admin.TabularInline):
#     model = FeedBackModel
#     extra = 0
#     max_num = 1

class FeedBackAttachmentInline(NestedTabularInline):
    model = FeedBackAttachment
    extra = 1
    max_num = 10

class FeedBackResponseInline(NestedTabularInline):
    model = FeedBackResponseModel
    extra = 0
    max_num = 1

class FeedBackInline(NestedTabularInline):
    model = FeedBackModel
    inlines = [FeedBackAttachmentInline, FeedBackResponseInline]
    extra = 0
    max_num = 1


@admin.register(ProjectModel)
class projectModelAdmin(ExportActionMixin, ExportMixin, NestedModelAdmin):
    inlines = [FeedBackInline]
    resource_class = ProjectResource
    list_display = ('company_name', 'location', 'start_date', 'end_date', 'total_days', 'days_format', 'is_active_now', 'has_feedback')
    list_filter = (('start_date', DateRangeFilter), ('end_date', DateRangeFilter), 'company_name', 'location', HasFeedBackFilter)
    search_fields = ('company_name__name', 'start_date', 'end_date')
    readonly_fields = ('total_cycle', 'total_days', 'is_active_now')

    def has_feedback(self, obj):
        return obj.feedbacks.exists()
    
    has_feedback.boolean = True  
    has_feedback.short_description = "Feed back?"

@admin.register(CompanyModel)
class CompanyModelAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(DayFormatModel)
class DayFormatModelAdmin(admin.ModelAdmin):
    list_display = ('format_name',) 

