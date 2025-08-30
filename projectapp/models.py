from django.db import models
from datetime import timedelta
from django.core.exceptions import ValidationError
from core.files_path import location_file_path
from django.utils.translation import gettext_lazy as _

# Create your models here.
class CompanyModel(models.Model):
    name = models.CharField(verbose_name=_('Company name'), max_length=255, unique=True)

    class Meta:
        verbose_name = _('Company')
        verbose_name_plural = _('companies')

    def __str__(self) -> str:
        return self.name
    

class DayFormatModel(models.Model):
    format_name = models.CharField(verbose_name=_('day format'), max_length=255, unique=True)

    class Meta:
        verbose_name = _('day format')
        verbose_name_plural = _('day formats')
        
    def __str__(self) -> str:
        return self.format_name



class ActiveLocationsManager(models.Manager):
    def get_queryset(self):
        # فقط کوئری هایی که end_date, end_cycle انها خالی هست
        return super().get_queryset().filter(is_active_now=True)
        # return super().get_queryset().filter(end_date__isnull=True, end_cycle__isnull=True)



CYCLES_CHOICES = [
    ('1', _('cycle 1')),
    ('2', _('cycle 2'))
]
class ProjectModel(models.Model):
    company_name = models.ForeignKey('CompanyModel', on_delete=models.CASCADE, related_name='project')
    lat = models.FloatField(verbose_name=_('lat'), null=False, blank=False)
    lon = models.FloatField(verbose_name=_('lon'), null=False, blank=False)
    description = models.TextField(verbose_name=_('Description'), null=True, blank=True)
    image_description = models.FileField(upload_to=location_file_path, verbose_name=_('Image'), null=True, blank=True)
    start_date = models.DateField(verbose_name=_('Start dateTime'))
    end_date = models.DateField(verbose_name=_('End dateTime'), null=True, blank=True)
    total_days = models.PositiveIntegerField(verbose_name=_('Total number of days'), default=0, editable=False)
    start_cycle = models.CharField(verbose_name=_('Start cycle'), choices=CYCLES_CHOICES, max_length=5, null=False, blank=False)
    end_cycle = models.CharField(verbose_name=_('End cycle'), choices=CYCLES_CHOICES, max_length=5,null=True, blank=True)
    total_cycle = models.PositiveIntegerField(verbose_name=_('Total cycle'), default=0, editable=False)
    location = models.CharField(verbose_name=_('Location'), max_length=255)
    days_format = models.ForeignKey('DayFormatModel', on_delete=models.CASCADE, related_name='format')
    is_active_now = models.BooleanField(verbose_name=_('is_active_now'), default=False, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # latest_pdf_url = models.URLField(verbose_name=_('Latest PDF URL'), null=True, blank=True, editable=False)

    latest_pdf_path = models.CharField(verbose_name=_('Latest PDF path'), max_length=512,  null=True, blank=True)
    # editable=False

    objects = models.Manager() # اصلی و شامل همه پروژه ها
    active_locations = ActiveLocationsManager() # فقط پروژه‌های بدون end_date و end_cycle


    def clean(self):
        if self.start_date and self.end_date:
            if self.end_date < self.start_date:
                raise ValidationError({
                    'end_date': _('End date cannot be before start date.')
                })

        if (
            self.start_date and self.end_date and
            self.start_cycle and self.end_cycle
        ):
            delta_days = (self.end_date - self.start_date).days
            start_cycle_num = int(self.start_cycle)
            end_cycle_num = int(self.end_cycle)

            if delta_days == 0 and end_cycle_num < start_cycle_num:
                raise ValidationError({
                    'end_cycle': _('End cycle cannot be before start cycle on the same day.')
                })


    def save(self, *args, **kwargs):

        if self.end_date and self.end_cycle:
            self.is_active_now = False
        else:
            self.is_active_now = True

        # total days
        if self.start_date and self.end_date:
            self.total_days = (self.end_date - self.start_date).days + 1
        else:
            self.total_days = 0

        #total cycle
        if (
            self.start_date and self.end_date and 
            self.start_cycle and self.end_cycle
        ):
            
            delta_days = (self.end_date - self.start_date).days
            start_cycle_num = int(self.start_cycle)
            end_cycle_num = int(self.end_cycle)


            self.total_cycle = delta_days * 2 + end_cycle_num - (start_cycle_num - 1)

        else:
            self.total_cycle = 0
        

        # is active
        # self.is_active = True if self.end_date and self.end_cycle is None else False

        super().save(*args, **kwargs)

    class Meta:
        verbose_name = _('Projects')
        verbose_name_plural = _('Projects')

    def __str__(self) -> str:
        return f"{self.company_name} - {self.location} - {self.start_date} - {self.end_date}"

