from datetime import date
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.views import View
from projectapp.admin import projectModelAdmin
from .models import CompanyModel, ProjectModel
from django.db.models import Q
from .filters import ProjectFilter
from .services.project_service import get_company_points_activity
from rest_framework import generics
from rest_framework import status
from django.contrib.auth.decorators import login_required
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import ActiveLocationsSerializers, CompanyPointsActivitySerializer, AllLocationsSerializers


# Create your views here.
@login_required
def home_view(request):
    return render(request, 'projectapp/home.html')


class GetActiveLocations(APIView):
    def get(self, request):
        try:
            active = ProjectModel.active_locations.all()
            serializer = ActiveLocationsSerializers(active, many=True)
            return Response(serializer.data)
        except ProjectModel.DoesNotExist:
            return Response({"error": "no active location found."}, status=404)

class GetAllLocationsView(APIView):
    def get(self, request):
        try:
            locations = ProjectModel.objects.all()
            serializer = AllLocationsSerializers(locations, many=True)
            return Response(serializer.data)
        except ProjectModel.DoesNotExist:
            return Response({"error": "no active location found."}, status=404)

from django.http import FileResponse, HttpResponseNotFound
from .models import ProjectModel
import os

def download_latest_pdf(request, project_id):
    project = ProjectModel.active_locations.get(id=project_id)
    if project.latest_pdf_path and os.path.exists(project.latest_pdf_path):
        # استخراج filename از مسیر برای دانلود
        filename = os.path.basename(project.latest_pdf_path)
        response = FileResponse(open(project.latest_pdf_path, 'rb'), content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response
    return HttpResponseNotFound("No PDF available")

# class ShowAllProjectsView(generics.ListAPIView):
#     queryset = ProjectModel.objects.all()
#     serializer_class = AllProjectsSerializer
#     filterset_class = ProjectFilter
#     filter_backends = [DjangoFilterBackend]
    # filterset_fields = ['company_name', 'location']



# class CompanyActiveDaysAPIView(APIView):
#     pass
#     """
#     API برای محاسبه تعداد روزهای یکتای فعال بودن هر شرکت در بازه داده شده
#     """

    # def get(self, request, *args, **kwargs):
    #     start = request.query_params.get("start")
    #     end = request.query_params.get("end")

    #     if not start or not end:
    #         return Response(
    #             {"error": "start and end are required (YYYY-MM-DD)"},
    #             status=status.HTTP_400_BAD_REQUEST
    #         )

    #     try:
    #         start_date = date.fromisoformat(start)
    #         end_date = date.fromisoformat(end)
    #     except ValueError:
    #         return Response(
    #             {"error": "Invalid date format. Use YYYY-MM-DD."},
    #             status=status.HTTP_400_BAD_REQUEST
    #         )

    #     # result = get_unique_active_days_by_company(start_date, end_date)
    #     # serializer = ActiveDaysSerializer(result, many=True)

    #     return Response(serializer.data, status=status.HTTP_200_OK)




class CompanyLocationDateRangeAPIView(APIView):
    """
    API برای محاسبه تعداد روزهای یکتای فعال بودن هر شرکت در بازه داده شده
    """

    def get(self, request, *args, **kwargs):
        start = request.query_params.get("start", None)
        end = request.query_params.get("end", None)
        company_name = request.query_params.get("company_name", None)  # تک شرکت یا رشته CSV
        location_name = request.query_params.get("location_name", None)  # تک شرکت یا رشته CSV
        # company_names = [company_name] if company_name else []
        # print('start', start)
        # print('end', end)

        # if not start or not end or not company_name or location_name:
        #     return Response(
        #         {"error": "start, or and company_name or location_name are required (YYYY-MM-DD)"},
        #         status=status.HTTP_400_BAD_REQUEST
        #     )
        if start or end:
            try:
                start = date.fromisoformat(start)
                end = date.fromisoformat(end)
            except ValueError:
                return Response(
                    {"error": "Invalid date format. Use YYYY-MM-DD."},
                    status=status.HTTP_400_BAD_REQUEST
                )
        # else:
        #     start_date, end_date = None

        result = get_company_points_activity(company_name, location_name, start, end)
        serializer = CompanyPointsActivitySerializer(result, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)



# class CompanyPointsActivityAPIView(APIView):
#     pass
#     """
#     API برای مشاهده نقاط فعال هر شرکت در یک بازه زمانی
#     """

#     def get(self, request, *args, **kwargs):
#         start = request.query_params.get("start")
#         end = request.query_params.get("end")
#         company_name = request.query_params.getlist("company_name")

#         if not start or not end or not company_name:
#             return Response(
#                 {"error": "start, end and company_id(s) are required (YYYY-MM-DD)"},
#                 status=status.HTTP_400_BAD_REQUEST
#             )

#         try:
#             start_date = date.fromisoformat(start)
#             end_date = date.fromisoformat(end)
#             company_name = [name for name in company_name]
#         except ValueError:
#             return Response(
#                 {"error": "Invalid date or company_id format."},
#                 status=status.HTTP_400_BAD_REQUEST
#             )

#         results = []

#         companies = CompanyModel.objects.filter(name__in=company_name)

#         for company in companies:
#             company_projects = ProjectModel.objects.filter(
#                 company_name=company,
#                 start_cycle__lte=end_date,
#             ).filter(
#                 Q(end_cycle__gte=start_date) | Q(end_cycle__isnull=True)
#             )

#             points_data = []
#             total_days = 0

#             for proj in company_projects:
#                 proj_start = max(proj.start_date, start)
#                 proj_end = min(proj.end_date or end_date, end_date)
#                 active_days = (proj_end - proj_start).days + 1

#                 points_data.append({
#                     "location_name": proj.location_name,
#                     "active_days": active_days
#                 })

#                 total_days += active_days

#             results.append({
#                 "company_id": company.id,
#                 "company_name": company.name,
#                 "points": points_data,
#                 "total_days": total_days
#             })

#         serializer = CompanyPointsActivitySerializer(results, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)