import json
import os

def initialize_dummy_technicians(storage):
    json_path = os.path.join(os.path.dirname(__file__), '../storage/technicians.json')
    with open(json_path, "r") as f:
        technicians = json.load(f)

    existing = storage.get_all_technicians()
    # Optional: avoid duplicates based on IDs
    existing_ids = {tech['id'] for tech in existing}
    for tech in technicians:
        if tech['id'] not in existing_ids:
            storage.save_technician_from_dict(tech)
