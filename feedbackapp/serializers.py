from rest_framework import serializers
from projectapp.models import ProjectModel
from .models import FeedBackModel, FeedBackResponseModel, FeedBackAttachmentModel
from rest_framework_gis.fields import GeometryField
from rest_framework_gis.serializers import GeoFeatureModelSerializer

# from projectapp.serializers import AllLocationsSerializers


class FeedBackAttachmentModelSerializer(serializers.ModelSerializer):
    file = serializers.SerializerMethodField() # برای نمایش url به ضورت کامل استفاده میشه
    class Meta:
        model = FeedBackAttachmentModel
        fields = ['id', 'file']


    def get_file(self, obj):
        '''
        http://localhost:8000/media/feedbacks/image.jpg
        '''
        if obj.file:
            return self.context['request'].build_absolute_uri(obj.file.url)
        return None


class FeedBackModelSerializer(serializers.ModelSerializer):
    attachments = FeedBackAttachmentModelSerializer(many=True, read_only=True)
    class Meta:
        model = FeedBackModel
        fields = ['name', 'phone_number', 'through', 'date', 'message', 'attachments']



class ProjectFeedBackSerializer(GeoFeatureModelSerializer):
    feedbacks = FeedBackModelSerializer(many=True, read_only=True)
    company_name = serializers.CharField(source='company_name.name')
    days_format = serializers.CharField(source='days_format.format_name')
    class Meta:
        model = ProjectModel
        geo_field = 'geometry'
        fields = ['pk', 'company_name', 'geometry', 'location', 'is_active_now', 'days_format', 'start_date', 'end_date', 'feedbacks']


class FeedBackAttachmentSerializer(serializers.Serializer):
    # file = serializers.SerializerMethodField()
    file = serializers.CharField()

    # def get_file(self, obj):
    #     '''
    #     http://localhost:8000/media/feedbacks/image.jpg
    #     '''
    #     request = self.context.get['request']
    #     if request and obj.file:
    #         return request.build_absolute_uri(obj.file.url)
    #     return None
            
class FeedBackResponseSerializer(serializers.Serializer):
    through = serializers.CharField()
    date = serializers.CharField()
    message = serializers.CharField()
    iso_form = serializers.CharField()


class FeedBackSerializer(serializers.Serializer):
    name = serializers.CharField()
    phone_number = serializers.CharField()
    through = serializers.CharField()
    date = serializers.CharField()
    message = serializers.CharField()
    attachments = FeedBackAttachmentSerializer(many=True, read_only=True)
    feedback_responses = FeedBackResponseSerializer(many=True, read_only=True)
    


class PointFeedBackSerializer(serializers.Serializer):
    pk = serializers.IntegerField()
    location_name = serializers.CharField()
    geometry = GeometryField()
    start_date = serializers.CharField()
    end_date = serializers.CharField()
    days_format = serializers.CharField()
    is_active_now = serializers.BooleanField()
    feedbacks = FeedBackSerializer(many=True, read_only=True)


class CompanyFeedbackSerializer(serializers.Serializer):
    company_name = serializers.CharField()
    detail = PointFeedBackSerializer(many=True)