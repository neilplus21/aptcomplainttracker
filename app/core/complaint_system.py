from models.complaint import Complaint
from utils.dummy_data import initialize_dummy_technicians
import random

class ComplaintSystem:
    def __init__(self, storage):
        self.storage = storage
        initialize_dummy_technicians(self.storage)
    def raise_complaint(self, category, description, resident_id):
        complaint = Complaint(category, description, resident_id)
        technician = self._find_suitable_technician(category)
        if technician:
            complaint.technician_id = technician['id']
            complaint.status = complaint.status.ASSIGNED
            print(f"Complaint assigned to: {technician['name']}.")
        self.storage.save_complaint(complaint)
        return complaint.id
    def _find_suitable_technician(self, category):
        technicians = self.storage.get_all_technicians()
        suitable = [
            t for t in technicians
            if category.value in t['specializations'] and t['is_available'] is True
        ]
        if suitable:
            return random.choice(suitable)
        avails = [t for t in technicians if t['is_available'] is True]

        return random.choice(avails) if avails else None
    def update_complaint_status(self, complaint_id, status):
        self.storage.update_complaint(complaint_id, {'status': status.value})
        print(f"Updated complaint {complaint_id} to {status.value}.")
    def get_complaint_details(self, complaint_id):
        complaint = self.storage.get_complaint(complaint_id)
        if complaint and complaint['technician_id']:
            tech = self.storage.get_technician(complaint['technician_id'])
            complaint['technician_name'] = tech['name'] if tech else "Unknown"
        return complaint
    def list_all_complaints(self):
        complaints = self.storage.get_all_complaints()
        for c in complaints:
            if c['technician_id']:
                tech = self.storage.get_technician(c['technician_id'])
                c['technician_name'] = tech['name'] if tech else "Unknown"
        return complaints
    def list_all_technicians(self):
        return self.storage.get_all_technicians()
