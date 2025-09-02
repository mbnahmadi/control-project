from django.contrib.gis.db import models as gis_models
from django.db import models
from django.core.exceptions import ValidationError
from django.db.models import constraints
from core.files_path import location_file_path
from django.db.models import Q, F
from django.utils.translation import gettext_lazy as _

# ================== Reference Models ========================
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

# =========================================================

# =================== Manager =============================
class ActiveLocationsManager(models.Manager):
    def get_queryset(self):
        # فقط کوئری هایی که end_date, end_cycle انها خالی هست
        # return super().get_queryset().filter(is_active_now=True)
        return super().get_queryset().filter(end_date__isnull=True, end_cycle__isnull=True)


# =========== Project Model =============
class ProjectModel(models.Model):
    CYCLES_CHOICES = [
        ('1', _('cycle 1')),
        ('2', _('cycle 2'))
    ]
    company_name = models.ForeignKey('CompanyModel', on_delete=models.CASCADE, related_name='project')
    geometry = gis_models.GeometryField(verbose_name=_('Geometry'), srid=4326, spatial_index=True, blank=False, null=False, 
    help_text=_('format Input: Point → Lat,Lon | Line → Lat1,Lon1; Lat2,Lon2; Lat3,Lon3; ...')) # این میتونه هم لاین باشه هم پوینت
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
    is_active_now = models.BooleanField(verbose_name=_('is_active_now'), default=False, editable=False, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    latest_pdf_path = models.CharField(verbose_name=_('Latest PDF path'), max_length=512,  null=True, blank=True)
    # editable=False

    # -------------------------------- Managers ----------------------------------------
    objects = models.Manager() # اصلی و شامل همه پروژه ها
    active_locations = ActiveLocationsManager() # فقط پروژه‌های بدون end_date و end_cycle

    # --------------------------- Helpers for geometry ---------------------------------
    def is_point(self):
        return self.geometry.geom_type == 'Point'

    def is_line(self):
        return self.geometry.geom_type == 'LineString'
    # ----------------------------------------------------------------------------------
    @property
    def display_point(self):
        if not self.geometry:
            return None
        if self.is_point():
            return self.geometry
        # for LineString -> it's alwayes put in centroid
        return self.geometry.centroid
    
    @property
    def lat(self):
        dp = self.display_point
        return None if dp is None else dp.y

    @property
    def lon(self):
        dp = self.display_point
        return None if dp is None else dp.x

    
    # ----------------------- Validations -----------------------------
    def clean(self):
        errors = {}
        # چیزی به جز لاین و پوینت نمیتونیم داشته باشیم
        if self.geometry and self.geometry.geom_type not in ('Point', 'LineString'):
            errors['geometry'] = _('Geometry must be Point or LineString.')

        if self.start_date and self.end_date and self.end_date < self.start_date:
            errors['end_date'] = _('End date cannot be before start date.')

        end_date_isnull = self.end_date is None
        end_cycle_isnull = self.end_cycle in (None, '')
        if (end_date_isnull != end_cycle_isnull):
            errors['end_date'] = _('end_date and end_cycle must be both null or both set.')
            errors['end_cycle'] = _('end_date and end_cycle must be both null or both set.')


        if (self.start_date and self.end_date and self.start_date == self.end_date
            and self.start_cycle and self.end_cycle):
            if int(self.end_cycle) < int(self.start_cycle):
                errors['end_cycle'] = _('End cycle cannot be before start cycle on the same day.')

        if errors:
            raise ValidationError(errors)

    # ----------------------- Save ------------------------------
    def save(self, *args, **kwargs):

        end_date_isnull = self.end_date is None
        end_cycle_isnull = self.end_cycle in (None, '')
        self.is_active_now = end_date_isnull and end_cycle_isnull

        # total_days
        if self.start_date and self.end_date:
            self.total_days = (self.end_date - self.start_date).days + 1
        else:
            self.total_days = 0

        # total_cycle
        if (self.start_date and self.end_date and self.start_cycle and self.end_cycle):
            delta_days = (self.end_date - self.start_date).days
            start_cycle_num = int(self.start_cycle)
            end_cycle_num = int(self.end_cycle)
            self.total_cycle = delta_days * 2 + end_cycle_num - (start_cycle_num - 1)
        else:
            self.total_cycle = 0

        super().save(*args, **kwargs)

    class Meta:
        verbose_name = _('Projects')
        verbose_name_plural = _('Projects')

        indexes = [
            models.Index(fields=['company_name']),
            models.Index(fields=['location']),
            models.Index(fields=['is_active_now']),
            models.Index(fields=['company_name', 'location']),
        ]
        # Constraint ->  یعنی محدودیت دیتابیسی که مستقیم روی جدول در دیتابیس enforce میشه(نه فقط در کد جنگو)
        constraints = [
            models.CheckConstraint(
                name='end_not_befor_start',
                check=Q(end_date__isnull=True) | Q(end_date__gte=F('start_date')),
            ),
            # Q -> وقتی بخوایم شرطی رو  بسازیم
            # F -> ارجاع به مقدار یک فیلد دیگه در همان رکورد
            models.CheckConstraint(
                name='end_date_cycle_pair_nullity',
                check=(Q(end_date__isnull=True, end_cycle__isnull=True) |
                       Q(end_date__isnull=False, end_cycle__isnull=False)),
            ),
            models.CheckConstraint(
                name='end_cycle_gte_start_cycle_same_day',
                check=(Q(end_date__isnull=True) |
                       Q(end_cycle__isnull=True) |
                       ~Q(end_date=F('start_date')) |
                       Q(end_cycle__gte=F('start_cycle'))),
            )
        ]

    def __str__(self) -> str:
        return f"{self.company_name} - {self.location} - {self.start_date} - {self.end_date}"

