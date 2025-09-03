from rest_framework import serializers
from .models import FeedBackModel, FeedBackResponseModel, FeedBackAttachmentModel
# from projectapp.serializers import AllLocationsSerializers


class FeedBackAttachmentSerializer(serializers.ModelSerializer):
    file = serializers.SerializerMethodField() # برای نمایش url به ضورت کامل استفاده میشه
    class Meta:
        model = FeedBackAttachmentModel
        fields = ['id', 'file']


    def get_file(self, obj):
        '''
        http://localhost:8000/media/profiles_image/image.jpg
        '''
        if obj.file:
            return self.context['request'].build_absolute_uri(obj.file.url)
        return None


class FeedBackSerializer(serializers.ModelSerializer):
    attachments = FeedBackAttachmentSerializer(many=True, read_only=True)
    class Meta:
        model = FeedBackModel
        fields = ['name', 'phone_number', 'through', 'date', 'message', 'attachments']

