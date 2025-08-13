from pyexpat import model
from rest_framework import serializers
from .models import ProjectModel

class ActiveLocationsSerializers(serializers.ModelSerializer):
    company_name = serializers.CharField(source='company_name.name')
    class Meta:
        model = ProjectModel
        fields = ['company_name', 'lat', 'lon', 'location', 'days_format']