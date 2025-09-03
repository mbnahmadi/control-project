import os
from datetime import date
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import FeedBackAttachmentModel, FeedBackModel, FeedBackResponseModel
from .serializers import FeedBackAttachmentSerializer
from projectapp.serializers import ProjectFeedBackSerializer
from projectapp.models import ProjectModel
from rest_framework import status
from django.contrib.auth.decorators import login_required
from django.http import FileResponse, HttpResponseNotFound




class ProjectsFeedBack(APIView):
    def get(self, request):
        projects = ProjectModel.objects.filter(feedbacks__isnull=False).distinct()
        # serializer = ProjectseFeedBackSerializer(project, many=True)
        serializer = ProjectFeedBackSerializer(projects, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

