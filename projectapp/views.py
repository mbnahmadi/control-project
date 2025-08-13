from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
import projectapp
from .models import ProjectModel
from .serializers import ActiveLocationsSerializers

# Create your views here.

def show_active_points(request):
    active = ProjectModel.active_locations.all()
    print(active)
    return render(request, 'projectapp/active_points.html')


class ShowActiveLocations(APIView):
    def get(self, request):
        try:
            active = ProjectModel.active_locations.all()
            serializer = ActiveLocationsSerializers(active, many=True)
            return Response(serializer.data)
        except ProjectModel.DoesNotExist:
            return Response({"error": "no active location found."}, status=404)