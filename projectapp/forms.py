from django import forms
from django.contrib.gis.geos import Point, LineString
from .models import ProjectModel


class LineStringTextArea(forms.Textarea):
    """
    Widget for manually entering LineString as 'lat1,lon1; lat2,lon2; ...'
    """
    # Widget -> در واقع کنترل می‌کنه چطور داده به کاربر نشون داده بشه و ازش گرفته بشه
    # برای نقطه و لاین و غیره  ویجت پیش فرض نقشه است
    def format_value(self, value):
        if isinstance(value, LineString):
            return "; ".join([f"{p.y},{p.x}" for p in value])
        return value
    def value_from_datadict(self, data, files, name):
        raw = data.get(name)
        if not raw:
            return None
        try:
            points = []
            for pair in raw.split(";"):
                lat, lon = pair.strip().split(",")
                points.append(Point(float(lon), float(lat)))  # توجه: ترتیب (lon, lat)
            return LineString(points)
        except Exception:
            raise forms.ValidationError("format is wrong. example -> 35.7,51.4; 35.8,51.5")

class ProjectAdminForm(forms.ModelForm):
    class Meta:
        model = ProjectModel
        fields = "__all__"
        widgets = {
            "location": forms.TextInput(attrs={"placeholder": "lat,lon"}),
            "path": LineStringTextArea(attrs={"rows": 3, "cols": 40}),
        }



# class ProjectFilterForm(forms.Form):
#     company_name = forms.CharField(required=False, label='Company Name')
#     start_date = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
#     end_date = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
