import os
import mysql.connector
from dotenv import load_dotenv
from model import Complaint, Technician
load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")


MSG_COMPLAINT_RAISED_SUCCESS = os.getenv("MSG_COMPLAINT_RAISED_SUCCESS")
MSG_TECH_ADDED_SUCCESS = os.getenv("MSG_TECH_ADDED_SUCCESS")
MSG_COMPLAINT_ASSIGNED_SUCCESS = os.getenv("MSG_COMPLAINT_ASSIGNED_SUCCESS")
MSG_COMPLAINT_STATUS_UPDATED_SUCCESS = os.getenv("MSG_COMPLAINT_STATUS_UPDATED_SUCCESS")
MSG_ERROR_DB_CONNECTION = os.getenv("MSG_ERROR_DB_CONNECTION")
MSG_ERROR_COMPLAINT_NOT_FOUND = os.getenv("MSG_ERROR_COMPLAINT_NOT_FOUND")
MSG_ERROR_TECH_NOT_FOUND = os.getenv("MSG_ERROR_TECH_NOT_FOUND")
MSG_ERROR_ASSIGN_RESOLVED = os.getenv("MSG_ERROR_ASSIGN_RESOLVED")
MSG_ERROR_INVALID_STATUS = os.getenv("MSG_ERROR_INVALID_STATUS")
MSG_ERROR_INPUT_EMPTY = os.getenv("MSG_ERROR_INPUT_EMPTY")
MSG_ERROR_GENERAL_DB = os.getenv("MSG_ERROR_GENERAL_DB")
MSG_NO_COMPLAINTS = os.getenv("MSG_NO_COMPLAINTS")
MSG_NO_TECHNICIANS = os.getenv("MSG_NO_TECHNICIANS")
MSG_EXIT = os.getenv("MSG_EXIT")
MSG_INVALID_CHOICE = os.getenv("MSG_INVALID_CHOICE")
MSG_ERROR_TECH_ALREADY_ASSIGNED = os.getenv("MSG_ERROR_TECH_ALREADY_ASSIGNED")
MSG_ERROR_INVALID_ID_INPUT = os.getenv("MSG_ERROR_INVALID_ID_INPUT")



def get_int_input(prompt: str) -> int | None:
    while True:
        try:
            value = input(prompt).strip()
            if not value:
                return None
            return int(value)
        except ValueError:
            print(MSG_ERROR_INVALID_ID_INPUT)

def get_db_connection():
    try:
        conn = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        return conn
    except mysql.connector.Error as err:
        print(MSG_ERROR_DB_CONNECTION.format(error=err))
        return None


def insert_complaint_to_db(complaint: Complaint) -> bool:
    conn = get_db_connection()
    if not conn:
        return False
    

    sql = "INSERT INTO complaints (category, resident_id, description, status) VALUES (%s, %s, %s, %s)"
    cursor = conn.cursor()
    try:
        cursor.execute(sql, (complaint.category, complaint.resident_id, complaint.description, complaint.status))
        conn.commit()
        complaint.id = cursor.lastrowid
        print(MSG_COMPLAINT_RAISED_SUCCESS.format(category=complaint.category, id=complaint.id))
        return True
    except mysql.connector.Error as err:
        print(MSG_ERROR_GENERAL_DB.format(error=err))
        return False
    finally:
        cursor.close()
        conn.close()

def insert_technician_to_db(technician: Technician) -> bool:
    conn = get_db_connection()
    if not conn:
        return False
    sql = "INSERT INTO technicians (name) VALUES (%s)"
    cursor = conn.cursor()
    try:
        cursor.execute(sql, (technician.name,))
        conn.commit()
        technician.id = cursor.lastrowid
        print(MSG_TECH_ADDED_SUCCESS.format(name=technician.name, id=technician.id))
        return True
    except mysql.connector.Error as err:
        print(MSG_ERROR_GENERAL_DB.format(error=err))
        return False
    finally:
        cursor.close()
        conn.close()

def get_all_complaints_from_db() -> list[Complaint]:
    conn = get_db_connection()
    if not conn:
        return []
    
    sql = """
    SELECT c.id, c.category, c.status, c.resident_id, c.assigned_technician_id, 
           c.description, c.created_at, c.updated_at, t.name AS assigned_technician_name
    FROM complaints c
    LEFT JOIN technicians t ON c.assigned_technician_id = t.id
    ORDER BY c.created_at DESC
    """
    cursor = conn.cursor(dictionary=True) 
    complaints = []
    try:
        cursor.execute(sql)
        for row in cursor.fetchall():
            complaint = Complaint(
                id=row['id'], 
                category=row['category'],
                status=row['status'],
                resident_id=row['resident_id'],
                assigned_technician_id=row['assigned_technician_id'],
                description=row['description'],
                created_at=row['created_at'],
                updated_at=row['updated_at']
            )
            complaint.assigned_technician_name_for_display = row['assigned_technician_name']
            complaints.append(complaint)
        return complaints
    except mysql.connector.Error as err:
        print(MSG_ERROR_GENERAL_DB.format(error=err))
        return []
    finally:
        cursor.close()
        conn.close()

def get_all_technicians_from_db() -> list[Technician]:
    conn = get_db_connection()
    if not conn:
        return []
    
    sql = "SELECT id, name, created_at FROM technicians ORDER BY name"
    cursor = conn.cursor(dictionary=True)
    technicians = []
    try:
        cursor.execute(sql)
        for row in cursor.fetchall():
            technicians.append(Technician(
                id=row['id'], 
                name=row['name'],
                created_at=row['created_at']
            ))
        return technicians
    except mysql.connector.Error as err:
        print(MSG_ERROR_GENERAL_DB.format(error=err))
        return []
    finally:
        cursor.close()
        conn.close()

def get_complaint_by_id_from_db(complaint_id: int) -> Complaint | None:
    conn = get_db_connection()
    if not conn:
        return None
    
    sql = """
    SELECT c.id, c.category, c.status, c.resident_id, c.assigned_technician_id, 
           c.description, c.created_at, c.updated_at, t.name AS assigned_technician_name
    FROM complaints c
    LEFT JOIN technicians t ON c.assigned_technician_id = t.id
    WHERE c.id = %s
    """
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute(sql, (complaint_id,))
        row = cursor.fetchone()
        if row:
            complaint = Complaint(
                id=row['id'], 
                category=row['category'],
                status=row['status'],
                resident_id=row['resident_id'],
                assigned_technician_id=row['assigned_technician_id'], 
                description=row['description'],
                created_at=row['created_at'],
                updated_at=row['updated_at']
            )
            complaint.assigned_technician_name_for_display = row['assigned_technician_name']
            return complaint
        return None
    except mysql.connector.Error as err:
        print(MSG_ERROR_GENERAL_DB.format(error=err))
        return None
    finally:
        cursor.close()
        conn.close()

def get_active_assignment_for_technician_from_db(technician_id: int) -> dict | None:
    conn = get_db_connection()
    if not conn:
        return None
    
    sql = """
    SELECT id, category, status
    FROM complaints
    WHERE assigned_technician_id = %s AND status NOT IN ('resolved', 'closed');
    """
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute(sql, (technician_id,))
        active_complaint = cursor.fetchone()
        return active_complaint
    except mysql.connector.Error as err:
        print(MSG_ERROR_GENERAL_DB.format(error=err))
        return None
    finally:
        cursor.close()
        conn.close()


def update_complaint_assignment_in_db(complaint_id: int, technician_id: int, current_complaint_status: str) -> bool: # Expect int IDs
    conn = get_db_connection()
    if not conn:
        return False

    all_technicians = get_all_technicians_from_db()
    selected_technician = next((t for t in all_technicians if t.id == technician_id), None)
    
    if not selected_technician:
        print(MSG_ERROR_TECH_NOT_FOUND.format(id=technician_id))
        return False
    active_assignment = get_active_assignment_for_technician_from_db(technician_id)
    if active_assignment:
        if active_assignment['id'] != complaint_id:
            print(MSG_ERROR_TECH_ALREADY_ASSIGNED.format(
                tech_name=selected_technician.name,
                complaint_id=active_assignment['id'],
                complaint_category=active_assignment['category']
            ))
            return False

    current_complaint_db = get_complaint_by_id_from_db(complaint_id)
    if not current_complaint_db:
        print(MSG_ERROR_COMPLAINT_NOT_FOUND.format(id=complaint_id))
        return False
    
    if current_complaint_db.status in ["resolved", "closed"]:
        print(MSG_ERROR_ASSIGN_RESOLVED.format(status=current_complaint_db.status, id=complaint_id))
        return False
    status_to_set = "assigned" if current_complaint_db.status == "pending" else current_complaint_db.status
    
    sql = "UPDATE complaints SET assigned_technician_id = %s, status = %s, updated_at = CURRENT_TIMESTAMP WHERE id = %s"
    cursor = conn.cursor()
    try:
        cursor.execute(sql, (technician_id, status_to_set, complaint_id))
        conn.commit()
        if cursor.rowcount == 0:
            print(MSG_ERROR_COMPLAINT_NOT_FOUND.format(id=complaint_id))
            return False
        
        print(MSG_COMPLAINT_ASSIGNED_SUCCESS.format(complaint_id=complaint_id, technician_name=selected_technician.name))
        return True
    except mysql.connector.Error as err:
        print(MSG_ERROR_GENERAL_DB.format(error=err))
        return False
    finally:
        cursor.close()
        conn.close()

def update_complaint_status_in_db(complaint_id: int, new_status: str) -> bool:
    conn = get_db_connection()
    if not conn:
        return False

    valid_statuses = {"pending", "assigned", "in_progress", "resolved", "closed"}
    if new_status.lower() not in valid_statuses:
        print(MSG_ERROR_INVALID_STATUS.format(status=new_status, valid_statuses=', '.join(valid_statuses)))
        return False

    sql = "UPDATE complaints SET status = %s, updated_at = CURRENT_TIMESTAMP WHERE id = %s"
    cursor = conn.cursor()
    try:
        cursor.execute(sql, (new_status.lower(), complaint_id))
        conn.commit()
        if cursor.rowcount == 0:
            print(MSG_ERROR_COMPLAINT_NOT_FOUND.format(id=complaint_id))
            return False
        print(MSG_COMPLAINT_STATUS_UPDATED_SUCCESS.format(complaint_id=complaint_id, new_status=new_status))
        return True
    except mysql.connector.Error as err:
        print(MSG_ERROR_GENERAL_DB.format(error=err))
        return False
    finally:
        cursor.close()
        conn.close()



def display_menu():
    print("\n" + "="*40)
    print("  Apartment Complaint Tracker Menu")
    print("="*40)
    print("1. Raise a New Complaint (Resident)")
    print("2. Add a New Technician (Admin)")
    print("3. Assign Technician to Complaint (Admin)")
    print("4. Update Complaint Status (Admin)")
    print("5. View All Complaints")
    print("6. View All Technicians")
    print("7. Get Details of a Specific Complaint")
    print("8. Exit")
    print("="*40)

def handle_raise_complaint():
    print("\n--- Raise a New Complaint ---")
    category = input("Enter complaint category: ").strip()
    resident_id = input("Enter your Resident ID: ").strip()
    description = input("Enter a brief description of the issue: ").strip()

    if not category:
        print(MSG_ERROR_INPUT_EMPTY.format(field_name="Category"))
        return
    if not resident_id:
        print(MSG_ERROR_INPUT_EMPTY.format(field_name="Resident ID"))
        return
    new_complaint = Complaint(id=None, category=category, resident_id=resident_id, description=description)
    insert_complaint_to_db(new_complaint)

def handle_add_technician():
    print("\n--- Add New Technician ---")
    name = input("Enter technician's name: ").strip()
    if not name:
        print(MSG_ERROR_INPUT_EMPTY.format(field_name="Technician name"))
        return
    new_technician = Technician(id=None, name=name)
    insert_technician_to_db(new_technician)

def handle_assign_technician():
    print("\n--- Assign Technician ---")
    
    complaints = get_all_complaints_from_db()
    technicians = get_all_technicians_from_db()

    if not complaints:
        print(MSG_NO_COMPLAINTS)
        return
    if not technicians:
        print(MSG_NO_TECHNICIANS)
        return

    print("\nAvailable Complaints:")
    for comp in complaints:
        assigned_tech = comp.assigned_technician_name_for_display if hasattr(comp, 'assigned_technician_name_for_display') and comp.assigned_technician_name_for_display else 'N/A'
        print(f"  ID: {comp.id}, Category: {comp.category}, Status: {comp.status}, Assigned: {assigned_tech}")

    print("\nAvailable Technicians:")
    for tech in technicians:
        print(f"  ID: {tech.id}, Name: {tech.name}")

    complaint_id = get_int_input("Enter the FULL Complaint ID to assign: ")
    technician_id = get_int_input("Enter the FULL Technician ID to assign: ")

    if complaint_id is None:
        print(MSG_ERROR_INPUT_EMPTY.format(field_name="Complaint ID"))
        return
    if technician_id is None:
        print(MSG_ERROR_INPUT_EMPTY.format(field_name="Technician ID"))
        return

    found_complaint = get_complaint_by_id_from_db(complaint_id)
    if not found_complaint:
        print(MSG_ERROR_COMPLAINT_NOT_FOUND.format(id=complaint_id))
        return
    update_complaint_assignment_in_db(complaint_id, technician_id, found_complaint.status) 


def handle_update_complaint_status():
    print("\n--- Update Complaint Status ---")
    
    complaints = get_all_complaints_from_db()
    if not complaints:
        print(MSG_NO_COMPLAINTS)
        return

    print("\nAvailable Complaints:")
    for comp in complaints:
        assigned_tech = comp.assigned_technician_name_for_display if hasattr(comp, 'assigned_technician_name_for_display') and comp.assigned_technician_name_for_display else 'N/A'
        print(f"  ID: {comp.id}, Category: {comp.category}, Status: {comp.status}, Assigned: {assigned_tech}") 

    complaint_id = get_int_input("Enter the FULL Complaint ID to update status: ")
    
    if complaint_id is None:
        print(MSG_ERROR_INPUT_EMPTY.format(field_name="Complaint ID"))
        return
    found_complaint_check = get_complaint_by_id_from_db(complaint_id)
    if not found_complaint_check:
        print(MSG_ERROR_COMPLAINT_NOT_FOUND.format(id=complaint_id))
        return

    print("\nValid statuses: pending, assigned, in_progress, resolved, closed")
    new_status = input(f"Enter new status for complaint {complaint_id}: ").strip()
    
    if not new_status:
        print(MSG_ERROR_INPUT_EMPTY.format(field_name="New status"))
        return
    
    update_complaint_status_in_db(complaint_id, new_status)

def handle_get_complaint_details():
    print("\n--- Get Specific Complaint Details ---")
    
    complaints = get_all_complaints_from_db()
    if not complaints:
        print(MSG_NO_COMPLAINTS)
        return

    print("\nAvailable Complaints:")
    for comp in complaints:
        print(f"  ID: {comp.id}, Category: {comp.category}, Status: {comp.status}")

    complaint_id = get_int_input("Enter the FULL Complaint ID to view details: ")
    
    if complaint_id is None:
        print(MSG_ERROR_INPUT_EMPTY.format(field_name="Complaint ID"))
        return        
    complaint = get_complaint_by_id_from_db(complaint_id)
    if complaint:
        print("\n--- Complaint Details ---")
        print(str(complaint))
        if hasattr(complaint, 'assigned_technician_name_for_display') and complaint.assigned_technician_name_for_display:
            print(f"  Assigned Technician Name: {complaint.assigned_technician_name_for_display}")
        print("-------------------------")
    else:
        print(MSG_ERROR_COMPLAINT_NOT_FOUND.format(id=complaint_id))

def display_all_complaints():
    complaints = get_all_complaints_from_db()
    if not complaints:
        print(MSG_NO_COMPLAINTS)
        return

    print("\n--- All Complaints ---")
    for comp in complaints:
        assigned_tech = comp.assigned_technician_name_for_display if hasattr(comp, 'assigned_technician_name_for_display') and comp.assigned_technician_name_for_display else 'N/A'
        print(f"ID: {comp.id}, Category: {comp.category}, Resident: {comp.resident_id}, Status: {comp.status}, Assigned To: {assigned_tech}")
        print("-" * 60)
    print("----------------------")

def display_all_technicians():
    technicians = get_all_technicians_from_db()
    if not technicians:
        print(MSG_NO_TECHNICIANS)
        return

    print("\n--- All Technicians ---")
    for tech in technicians:
        print(f"ID: {tech.id}, Name: {tech.name}")
    print("-----------------------")


if __name__ == "__main__":
    while True:
        display_menu()
        choice = input("Enter your choice (1-8): ").strip()

        if choice == '1':
            handle_raise_complaint()
        elif choice == '2':
            handle_add_technician()
        elif choice == '3':
            handle_assign_technician()
        elif choice == '4':
            handle_update_complaint_status()
        elif choice == '5':
            display_all_complaints()
        elif choice == '6':
            display_all_technicians()
        elif choice == '7':
            handle_get_complaint_details()
        elif choice == '8':
            print(MSG_EXIT)
            break
        else:
            print(MSG_INVALID_CHOICE)
        input("\nPress Enter to continue...")