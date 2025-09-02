from django import forms
from django.contrib.gis.db import models as gis_models
from django.contrib.gis.forms import PointField, LineStringField
from django.contrib.gis.geos import Point, LineString
from .models import ProjectModel


class GeometryTextArea(forms.Textarea):
    """
    Widget for manually entering LineString as 'lat1,lon1; lat2,lon2; ...'
    """
    # Widget -> در واقع کنترل می‌کنه چطور داده به کاربر نشون داده بشه و ازش گرفته بشه
    # برای نقطه و لاین و غیره  ویجت پیش فرض نقشه است
    def format_value(self, value):
        if isinstance(value, Point):
            return f"{value.y},{value.x}"
        elif isinstance(value, list):
            return "; ".join([f"{p.y},{p.x}" for p in value])
        return value

    def value_from_datadict(self, data, files, name):
        raw = data.get(name)
        if not raw:
            return None

        try:
            pairs = [p.strip() for p in raw.split(";") if p.strip()]
            points = []

            for pair in pairs:
                lat, lon = pair.split(",")
                points.append((float(lon), float(lat)))  

            if len(points) == 1:
                return Point(points[0]) 
            else:
                return LineString(points)  

        except Exception as e:
            raise forms.ValidationError(
                "Format is wrong. Example: "
                "Point → Lat,Lon | Line → Lat1,Lon1; Lat2,Lon2; Lat3,Lon3; ..."
                + str(e)
            )

class ProjectAdminForm(forms.ModelForm):

    class Meta:
        model = ProjectModel
        fields = "__all__"
        widgets = {
            'geometry': GeometryTextArea(attrs={"rows": 3, "cols": 40}),
        }
