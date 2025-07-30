from datetime import datetime
class Complaint:
    def __init__(self, id: int | None, category: str, resident_id: str, status: str = "pending",
                 assigned_technician_id: int | None = None, description: str = "",
                 created_at: datetime | None = None, updated_at: datetime | None = None):
        self.id = id
        self.category = category
        self.status = status
        self.resident_id = resident_id
        self.assigned_technician_id = assigned_technician_id
        self.description = description
        self.created_at = created_at if created_at else datetime.now()
        self.updated_at = updated_at if updated_at else datetime.now()
        self.assigned_technician_name_for_display = None 

    def __str__(self):
        tech_info = ""
        if self.assigned_technician_id:
            tech_display_name = (self.assigned_technician_name_for_display 
                                 if self.assigned_technician_name_for_display else str(self.assigned_technician_id))
            tech_info = f", Assigned: {tech_display_name}"
        
        return (f"  Complaint ID: {self.id}\n"
                f"  Category: {self.category}\n"
                f"  Resident ID: {self.resident_id}\n"
                f"  Status: {self.status}{tech_info}\n"
                f"  Description: {self.description}\n"
                f"  Created At: {self.created_at.strftime('%Y-%m-%d %H:%M:%S')}\n"
                f"  Last Updated: {self.updated_at.strftime('%Y-%m-%d %H:%M:%S')}")

    def to_dict(self):
        return {
            'id': self.id,
            'category': self.category,
            'status': self.status,
            'resident_id': self.resident_id,
            'assigned_technician_id': self.assigned_technician_id,
            'description': self.description,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }


class Technician:
    def __init__(self, id: int | None, name: str, created_at: datetime | None = None):
        self.id = id
        self.name = name
        self.created_at = created_at if created_at else datetime.now()

    def __str__(self):
        return (f"  Technician ID: {self.id}\n"
                f"  Name: {self.name}\n"
                f"  Added On: {self.created_at.strftime('%Y-%m-%d %H:%M:%S')}")

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'created_at': self.created_at
        }


CREATE_TECHNICIANS_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS technicians (
    id INT AUTO_INCREMENT PRIMARY KEY, 
    name VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""

CREATE_COMPLAINTS_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS complaints (
    id INT AUTO_INCREMENT PRIMARY KEY,
    category VARCHAR(255) NOT NULL,
    status VARCHAR(50) NOT NULL DEFAULT 'pending',
    resident_id VARCHAR(255) NOT NULL,
    assigned_technician_id INT, -- Changed to INT
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (assigned_technician_id) REFERENCES technicians(id) ON DELETE SET NULL
);
"""