import os
from datetime import date
from django.shortcuts import render
from django.template import context
from rest_framework.views import APIView
from rest_framework.response import Response
from django.views import View
from .models import CompanyModel, ProjectModel
from .services.project_service import get_company_points_activity
from rest_framework import status
from django.http import FileResponse, HttpResponseNotFound
from .serializers import ActiveLocationsSerializers, CompanyPointsActivitySerializer, AllLocationsSerializers
from django.db.models import CharField, Func

class GeometryType(Func):
    function = 'ST_GeometryType' 
    output_field = CharField()

# Create your views here.

class GetActiveLocations(APIView):
    '''
    get all active locations
    '''
    def get(self, request):
        try:
            active = ProjectModel.active_locations.all()
            serializer = ActiveLocationsSerializers(active, many=True)
            return Response(serializer.data)
        except ProjectModel.DoesNotExist:
            return Response({"error": "no active location found."}, status=404)

class GetAllLocationsView(APIView):
    '''
    get all locations
    '''
    def get(self, request):
        try:
            locations = ProjectModel.objects.all()
            serializer = AllLocationsSerializers(locations, many=True)
            return Response(serializer.data)
        except ProjectModel.DoesNotExist:
            return Response({"error": "no active location found."}, status=404)

class GetAllRoutesView(APIView):
    '''
    get all routes
    '''
    def get(self, request):
        try:
            routes = ProjectModel.objects.annotate(
                geom_type=GeometryType('geometry')
            ).filter(geom_type='ST_LineString')
            serializer = AllLocationsSerializers(routes, many=True)

            return Response(serializer.data)
        except ProjectModel.DoesNotExist:
            return Response({"error": "no route found."}, status=404)


def download_latest_pdf(request, project_id):
    '''
    download latest pdf of active project
    '''
    project = ProjectModel.active_locations.get(id=project_id)
    if project.latest_pdf_path and os.path.exists(project.latest_pdf_path):
        # استخراج filename از مسیر برای دانلود
        filename = os.path.basename(project.latest_pdf_path)
        response = FileResponse(open(project.latest_pdf_path, 'rb'), content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response
    return HttpResponseNotFound("No PDF available")

class CompanyLocationDateRangeAPIView(APIView):
    """
    API برای محاسبه تعداد روزهای یکتای فعال بودن هر شرکت در بازه داده شده
    """

    def get(self, request, *args, **kwargs):
        start = request.query_params.get("start")
        end = request.query_params.get("end")
        company_name = request.query_params.get("company_name")
        location_name = request.query_params.get("location_name")

        if start or end:
            try:
                start = date.fromisoformat(start)
                end = date.fromisoformat(end)
            except ValueError:
                return Response(
                    {"error": "Invalid date format. Use YYYY-MM-DD."},
                    status=status.HTTP_400_BAD_REQUEST
                )

        result = get_company_points_activity(company_name, location_name, start, end)
        # print(result)

        serializer = CompanyPointsActivitySerializer(result, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
