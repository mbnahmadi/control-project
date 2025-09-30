import time
from celery import shared_task
from .models import ProjectModel
from django.core.cache import cache


@shared_task
def update_active_projects_pdfs():
    qs = ProjectModel.active_locations.only('id', 'project_address', 'latest_pdf_path').iterator()
    companies = set()
    for p in qs:
        if p.project_address:
            companies.add(p.project_address.split('/', 1)[0])
    for company in companies:
        cache.delete(f'latest_gfs_{company}')
    active_projects = ProjectModel.active_locations.only('id', 'project_address', 'latest_pdf_path').iterator()
    for project in active_projects:
        new_path = project.generate_latest_pdf_address()
        if new_path and new_path != project.latest_pdf_path:
            ProjectModel.objects.filter(id=project.id).update(latest_pdf_path=new_path)
