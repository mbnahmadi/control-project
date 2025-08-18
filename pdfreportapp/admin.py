import os
import zipfile
from django.conf import settings
from django.http import HttpResponse
from django.contrib import admin
from .models import PdfReportModel, CompanyModel
from rangefilter.filters import DateRangeFilter


# Register your models here.




def download_pdf_files_as_zip(modeladmin, request, queryset):

    # نام فایل zip خروجی
    zip_filename = "files_export.zip"

    # مسیر موقت برای ذخیره zip
    zip_path = os.path.join(settings.MEDIA_ROOT, zip_filename)

    # ساخت فایل zip
    with zipfile.ZipFile(zip_path, 'w') as zipf:
        for obj in queryset:
            if obj.pdf_file:
                file_path = obj.pdf_file.path

                if os.path.exists(file_path):
                    # نام فایل در داخل zip
                    zipf.write(file_path, os.path.basename(file_path))

    with open(zip_path, 'rb') as zipf:
        response = HttpResponse(zipf.read(), content_type="application/zip")
        response['Content-Disposition'] = f'attachment; filename={zip_filename}'
        return response


download_pdf_files_as_zip.short_description = "Download selected files as ZIP"


@admin.register(PdfReportModel)
class PdfRepoerModelAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'start_date', 'cycle', 'location', 'days_format')
    list_filter = (
        'company_name',
        'location',
        ('start_date', DateRangeFilter),
    )
    actions = [download_pdf_files_as_zip]


@admin.register(CompanyModel)
class CompanyModelAdmin(admin.ModelAdmin):
    list_display = ('name',)