class StorageInterface:
    def save_complaint(self, complaint): raise NotImplementedError
    def get_complaint(self, complaint_id): raise NotImplementedError
    def update_complaint(self, complaint_id, updates): raise NotImplementedError
    def get_all_complaints(self): raise NotImplementedError
    def save_technician(self, technician): raise NotImplementedError
    def get_all_technicians(self): raise NotImplementedError
    def get_technician(self, technician_id): raise NotImplementedError
