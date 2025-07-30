from utils.enums import ComplaintStatus, ComplaintCategory
import uuid
from datetime import datetime

class Complaint:
    def __init__(self, category, description, resident_id):
        self.id = str(uuid.uuid4())
        self.category = category
        self.description = description
        self.status = ComplaintStatus.PENDING
        self.resident_id = resident_id
        self.technician_id = None
        self.created_at = datetime.now().isoformat()
        self.updated_at = datetime.now().isoformat()
    def to_dict(self):
        return {
            'id': self.id,
            'category': self.category.value,
            'description': self.description,
            'status': self.status.value,
            'resident_id': self.resident_id,
            'technician_id': self.technician_id,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
