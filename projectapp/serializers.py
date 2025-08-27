from rest_framework import serializers
from .models import CompanyModel, ProjectModel

class ActiveLocationsSerializers(serializers.ModelSerializer):
    company_name = serializers.CharField(source='company_name.name')
    class Meta:
        model = ProjectModel
        fields = ['pk', 'company_name', 'lat', 'lon', 'location', 'is_active_now']


class AllLocationsSerializers(serializers.ModelSerializer):
    company_name = serializers.CharField(source='company_name.name')
    class Meta:
        model = ProjectModel
        fields = ['pk', 'company_name', 'lat', 'lon', 'location', 'is_active_now', 'start_date', 'end_date']



# class AllLocationsSerializer(serializers.ModelSerializer):
#     # company_name = serializers.CharField(source='company_name.name')
#     class Meta:
#         model = CompanyModel
#         fields = '__all__'



# class ActiveDaysSerializer(serializers.Serializer):
#     company_id = serializers.IntegerField()
#     company_name = serializers.CharField()
#     active_days = serializers.IntegerField()



class PointActivitySerializer(serializers.Serializer):
    location_name = serializers.CharField()
    pk = serializers.IntegerField()
    lat = serializers.FloatField()
    lon = serializers.FloatField()
    start_date = serializers.CharField()
    end_date = serializers.CharField()
    days_format = serializers.CharField()
    is_active_now = serializers.BooleanField()
    active_days = serializers.IntegerField()


class CompanyPointsActivitySerializer(serializers.Serializer):
    # company_id = serializers.IntegerField()
    company_name = serializers.CharField()
    points = PointActivitySerializer(many=True)
    total_days = serializers.IntegerField()
    total_location = serializers.IntegerField()