from rest_framework import serializers
# from feedbackapp.serializers import FeedBackAttachmentSerializer
from .models import CompanyModel, ProjectModel
from rest_framework_gis.serializers import GeoFeatureModelSerializer
from rest_framework_gis.fields import GeometryField
from feedbackapp.serializers import FeedBackSerializer

class ActiveLocationsSerializers(GeoFeatureModelSerializer):
    company_name = serializers.CharField(source='company_name.name')
    days_format = serializers.CharField(source='days_format.format_name')
    class Meta:
        model = ProjectModel
        geo_field = 'geometry'
        fields = ['pk', 'company_name', 'geometry', 'location', 'is_active_now', 'start_date', 'end_date', 'days_format']


class AllLocationsSerializers(GeoFeatureModelSerializer):
    company_name = serializers.CharField(source='company_name.name')
    days_format = serializers.CharField(source='days_format.format_name')
    class Meta:
        model = ProjectModel
        geo_field = 'geometry'
        fields = ['pk', 'company_name', 'geometry', 'location', 'is_active_now', 'start_date', 'end_date', 'days_format']


class PointActivitySerializer(serializers.Serializer):
    pk = serializers.IntegerField()
    location_name = serializers.CharField()
    geometry = GeometryField()
    # lat = serializers.FloatField()
    # lon = serializers.FloatField()
    start_date = serializers.CharField()
    end_date = serializers.CharField()
    days_format = serializers.CharField()
    is_active_now = serializers.BooleanField()
    active_days = serializers.IntegerField()


class CompanyPointsActivitySerializer(serializers.Serializer):
    # company_id = serializers.IntegerField()
    company_name = serializers.CharField()
    detail = PointActivitySerializer(many=True)
    total_days = serializers.IntegerField()
    total_location = serializers.IntegerField()







