import json
from django.contrib.gis.geos import Point

with open('projects.json', encoding="utf8") as f:
    data = json.load(f)

new_data = []
for obj in data:
    fields = obj["fields"]

    # Build geometry field
    lat = fields.pop("lat", None)
    lon = fields.pop("lon", None)
    if lat is not None and lon is not None:
        fields["geometry"] = str(Point(lon, lat))  # "POINT(lon lat)"

    # Rename file field
    fields["attachment"] = fields.pop("image_description", None)

    # Add latest_pdf_path (empty for now)
    fields["latest_pdf_path"] = None

    obj["fields"] = fields
    new_data.append(obj)

with open("new_projects.json", "w") as f:
    json.dump(new_data, f, indent=2)