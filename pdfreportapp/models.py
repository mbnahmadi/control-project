from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from projectapp.models import DayFormatModel
# Create your models here.

class CompanyModel(models.Model):
    name = models.CharField(verbose_name=_('Company name'), max_length=255, unique=True)

    class Meta:
        verbose_name = _('Company name')
        verbose_name_plural = _('companies name')

    def __str__(self) -> str:
        return self.name
    


CYCLES_CHOICES = [
    ('1', _('cycle 1')),
    ('2', _('cycle 2'))
]


class PdfReportModel(models.Model):
    company_name = models.ForeignKey('CompanyModel', on_delete=models.CASCADE, related_name='project')
    # description = models.TextField(verbose_name=_('Description'), null=True, blank=True)
    pdf_file = models.FileField(upload_to='pdf_files', verbose_name=_('PDF'), null=False, blank=False)
    start_date = models.DateField(verbose_name=_('Start dateTime'))
    # end_date = models.DateField(verbose_name=_('End dateTime'), null=True, blank=True)
    # total_days = models.PositiveIntegerField(verbose_name=_('Total number of days'), default=0, editable=False)
    # start_cycle = models.CharField(verbose_name=_('Start cycle'), choices=CYCLES_CHOICES, max_length=5, null=False, blank=False)
    cycle = models.CharField(verbose_name=_('cycle'), choices=CYCLES_CHOICES, max_length=5)
    # total_cycle = models.PositiveIntegerField(verbose_name=_('Total cycle'), default=0, editable=False)
    location = models.CharField(verbose_name=_('Location'), max_length=255)
    days_format = models.ForeignKey(DayFormatModel, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



    def clean(self): # برای ولیدیت در مدل استفاده میشه
        if self.start_date and self.end_date:
            if self.end_date < self.start_date:
                raise ValidationError({
                    'end_date': _('End date cannot be before start date.')
                })


    class Meta:
        verbose_name = _('Pdf')
        verbose_name_plural = _('Pdf')

    def __str__(self) -> str:
        return f"{self.company_name}"

    
