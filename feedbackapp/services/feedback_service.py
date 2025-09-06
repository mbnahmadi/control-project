from datetime import date, timedelta
from django.db.models import Q
from projectapp.models import ProjectModel, CompanyModel


def get_company_feedback_activity(company_name=None, location_name=None, start_range=None, end_range=None):
    results = []

    qs = ProjectModel.has_feedback.all().prefetch_related("feedbacks").distinct()
    # for proj in qs:
    #     for fb in proj.feedbacks.all():
    # # feedback = qs.feedbacks.all()
    #         print(fb.name)
    


    # فیلتر بر اساس شرکت
    if company_name:
        qs = qs.filter(company_name__name__iexact=company_name)

    # فیلتر بر اساس لوکیشن
    if location_name:
        qs = qs.filter(location__iexact=location_name)

    # فیلتر بر اساس بازه زمانی
    if start_range and end_range:
        qs = qs.filter(start_date__lte=end_range).filter(Q(end_date__gte=start_range) | Q(end_date__isnull=True))
    

    # گروه‌بندی بر اساس شرکت
    companies = {}
    for proj in qs:
        # for fb in proj:
        #     print(fb)
        company = proj.company_name.name
        if company not in companies:
            companies[company] = {
                "company_name": company,
                "detail": []
            }

        # if start_range and end_range:


        feedbacks = []
        for fb in proj.feedbacks.all().distinct():
            if start_range or end_range:
                if not (start_range <= fb.date <= end_range):
                    continue
            try:
                res = fb.responses
            except Exception as e:
                res = None
            responses = []
            if res:
                responses.append({
                    "through": res.through,
                    "date": res.date,
                    "message": res.message,
                    "iso_form": getattr(res.iso_form, 'url', None),
                })

            attachments = []
            for attach in fb.attachments.all().distinct():
                attachments.append({
                    "file": attach.file
                })
            feedbacks.append({
                "name": fb.name,
                "phone_number": fb.phone_number,
                "through": fb.through,
                "date": fb.date,
                "message": fb.message,
                "attachments": attachments,
                "feedback_responses": responses

            })

        companies[company]["detail"].append({
            "location_name": proj.location,
            "pk": proj.pk,
            "geometry": proj.geometry,
            "start_date": proj.start_date,
            "end_date": proj.end_date,
            "days_format": proj.days_format.format_name,
            "is_active_now": proj.is_active_now,
            "feedbacks": feedbacks
        })
        

    results = list(companies.values())
    return results