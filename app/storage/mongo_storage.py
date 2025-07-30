from storage.interface import StorageInterface

class MongoDBStorage(StorageInterface):
    def __init__(self, config):
        try:
            from pymongo import MongoClient
            self.client = MongoClient(config['uri'])
            self.db = self.client[config['database']]
            self.complaints = self.db.complaints
            self.technicians = self.db.technicians
        except ImportError:
            self.client = None
            print("pymongo not installed. Simulation mode.")
    def save_complaint(self, complaint):
        if self.client: self.complaints.insert_one(complaint.to_dict())
        else: print("[MongoDB] Save complaint: Simulation.")
    def get_complaint(self, complaint_id):
        if self.client:
            res = self.complaints.find_one({"id": complaint_id})
            if res: res.pop('_id', None)
            return res
        print("[MongoDB] Get complaint: Simulation.")
        return None
    def update_complaint(self, complaint_id, updates):
        if self.client:
            from datetime import datetime
            updates['updated_at'] = datetime.now().isoformat()
            self.complaints.update_one({"id": complaint_id}, {"$set": updates})
        else: print("[MongoDB] Update complaint: Simulation.")
    def get_all_complaints(self):
        if self.client:
            res = list(self.complaints.find())
            [r.pop('_id', None) for r in res]
            return res
        print("[MongoDB] Get all complaints: Simulation.")
        return []
    def save_technician(self, technician):
        if self.client: self.technicians.insert_one(technician.to_dict())
        else: print("[MongoDB] Save technician: Simulation.")
    def get_all_technicians(self):
        if self.client:
            res = list(self.technicians.find())
            [r.pop('_id', None) for r in res]
            return res
        print("[MongoDB] Get all techs: Simulation.")
        return []
    def get_technician(self, technician_id):
        if self.client:
            res = self.technicians.find_one({"id": technician_id})
            if res: res.pop('_id', None)
            return res
        print("[MongoDB] Get technician: Simulation.")
        return None
