import json
from storage.interface import StorageInterface
from datetime import datetime

class JSONStorage(StorageInterface):
    complaints_file = "app/storage/complaints.json"
    technicians_file = "app/storage/technicians.json"

    def __init__(self):
        self._initialize_files()
    def _initialize_files(self):
        for file in [self.complaints_file, self.technicians_file]:
            try:
                with open(file, 'r'): pass
            except FileNotFoundError:
                with open(file, 'w') as f: json.dump([], f)

    def save_complaint(self, complaint):
        complaints = self._load_complaints()
        complaints.append(complaint.to_dict())
        self._save_complaints(complaints)
    def get_complaint(self, complaint_id):
        complaints = self._load_complaints()
        return next((c for c in complaints if c['id'] == complaint_id), None)
    def update_complaint(self, complaint_id, updates):
        complaints = self._load_complaints()
        for complaint in complaints:
            if complaint['id'] == complaint_id:
                complaint.update(updates)
                complaint['updated_at'] = datetime.now().isoformat()
                break
        self._save_complaints(complaints)
    def get_all_complaints(self):
        return self._load_complaints()
    def save_technician(self, technician):
        technicians = self._load_technicians()
        technicians.append(technician.to_dict())
        self._save_technicians(technicians)
    def get_all_technicians(self):
        return self._load_technicians()
    def get_technician(self, technician_id):
        technicians = self._load_technicians()
        return next((t for t in technicians if t['id'] == technician_id), None)
    def _load_complaints(self):
        with open(self.complaints_file, 'r') as f: return json.load(f)
    def _save_complaints(self, complaints):
        with open(self.complaints_file, 'w') as f: json.dump(complaints, f, indent=2)
    def _load_technicians(self):
        with open(self.technicians_file, 'r') as f: return json.load(f)
    def _save_technicians(self, technicians):
        with open(self.technicians_file, 'w') as f: json.dump(technicians, f, indent=2)
