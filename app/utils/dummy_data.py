from models.technician import Technician
from utils.enums import ComplaintCategory

def initialize_dummy_technicians(storage):
    existing = storage.get_all_technicians()
    if not existing:
        dummy = [
            Technician("John Smith", [ComplaintCategory.PLUMBING, ComplaintCategory.GENERAL]),
            Technician("Maria Garcia", [ComplaintCategory.ELECTRICAL]),
            Technician("David Wilson", [ComplaintCategory.HVAC]),
            Technician("Sarah Johnson", [ComplaintCategory.APPLIANCE, ComplaintCategory.ELECTRICAL]),
            Technician("Mike Brown", [ComplaintCategory.PLUMBING, ComplaintCategory.HVAC]),
        ]
        for tech in dummy:
            storage.save_technician(tech)
