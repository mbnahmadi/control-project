from django.contrib import admin
from import_export.admin import ExportMixin, ExportActionMixin
from import_export import resources, fields
from .models import CompanyModel, DayFormatModel, ProjectModel
from .forms import ProjectFilterForm
from rangefilter.filters import DateRangeFilter
from django.template.response import TemplateResponse
from django.utils.html import format_html

# Register your models here.
class ProjectResource(resources.ModelResource):
    company_name = fields.Field(
        column_name='company',
        attribute='company_name__name',
        readonly=True
    )
    description = fields.Field(
        column_name='description',
        attribute='description'
    )
    # image_description = fields.Field(
    #     column_name='image uploaded',
    #     attribute='image_description.url'
    # )
    start_date = fields.Field(
        column_name='start date',
        attribute='start_date'
    )
    end_date = fields.Field(
        column_name='end date',
        attribute='end_date'
    )
    # total_days_display = fields.Field(
    #     column_name='total days',
    #     attribute='total_days',
    #     readonly=True
    # )
    location = fields.Field(
        column_name='location',
        attribute='location'
    )
    start_cycle_display = fields.Field(
        column_name='start cycle',
        attribute='start_cycle',
        readonly=True
    )
    end_cycle_display = fields.Field(
        column_name='end cycle',
        attribute='end_cycle',
        readonly=True
    )
    # total_cycle_display = fields.Field(
    #     column_name='total cycle',
    #     attribute='total_cycle',
    #     readonly=True
    # )
    days_format = fields.Field(
        column_name='day format',
        attribute='days_format__format_name',
        readonly=True
    )

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


# --------------- filter -----------------


@admin.register(ProjectModel)
class projectModelAdmin(ExportActionMixin, ExportMixin, admin.ModelAdmin):
    resource_class = ProjectResource
    list_display = ('company_name', 'location', 'start_date', 'end_date', 'total_cycle', 'total_days', 'days_format', 'is_active_now')
    # list_filter = ['company_name', 'location', 'start_date', 'end_date']
    list_filter = (
        'company_name',
        'location',
        ('start_date', DateRangeFilter),
        ('end_date', DateRangeFilter),
    )
    search_fields = ('company_name__name', 'start_date', 'end_date')
    readonly_fields = ('total_cycle', 'total_days', 'is_active_now')


# @admin.register(ProjectModel)
# class ProjectAdmin(admin.ModelAdmin):
#     list_display = ('company_name', 'start_date', 'end_date', 'total_cycle')
#     change_list_template = 'admin/project_change_list.html'  # در مرحله بعد می‌سازیم اینو

#     def changelist_view(self, request, extra_context=None):
#         form = ProjectFilterForm(request.GET or None)

#         qs = self.get_queryset(request)

#         if form.is_valid():
#             company_name = form.cleaned_data.get('company_name')
#             start_date = form.cleaned_data.get('start_date')
#             end_date = form.cleaned_data.get('end_date')

#             if company_name:
#                 qs = qs.filter(company_name__icontains=company_name)

#             if start_date:
#                 qs = qs.filter(start_date__gte=start_date)

#             if end_date:
#                 qs = qs.filter(end_date__lte=end_date)

#         extra_context = extra_context or {}
#         extra_context['filter_form'] = form
#         extra_context['cl'] = self.get_changelist_instance(request)  # برای نمایش جدول
#         return TemplateResponse(request, self.change_list_template, extra_context)


@admin.register(CompanyModel)
class CompanyModelAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(DayFormatModel)
class DayFormatModelAdmin(admin.ModelAdmin):
    list_display = ('format_name',) 

