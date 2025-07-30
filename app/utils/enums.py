from enum import Enum
class StorageType(Enum):
    JSON = "json"
    POSTGRESQL = "postgresql"
    MONGODB = "mongodb"
class ComplaintStatus(Enum):
    PENDING = "pending"
    ASSIGNED = "assigned"
    IN_PROGRESS = "in_progress"
    RESOLVED = "resolved"
class ComplaintCategory(Enum):
    PLUMBING = "plumbing"
    ELECTRICAL = "electrical"
    HVAC = "hvac"
    APPLIANCE = "appliance"
    GENERAL = "general"
