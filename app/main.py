from config import get_storage_choice
from dotenv import load_dotenv
from core.complaint_system import ComplaintSystem
from utils.enums import ComplaintCategory, ComplaintStatus

load_dotenv()
# task: removing hardcoding 
# push redundant messages to .env file
def main():
    storage = get_storage_choice()
    system = ComplaintSystem(storage)

    while True:
        print("\n=== Complaint Management Menu ===")
        print("1. Raise a complaint")
        print("2. Update complaint status")
        print("3. View complaint details")
        print("4. List all complaints")
        print("5. List all technicians")
        print("6. Exit")

        choice = input("\nEnter your choice (1-6): ").strip()
        if choice == "1":
            print("\nAvailable categories:")
            for i, category in enumerate(ComplaintCategory, 1):
                print(f"{i}. {category.value.title()}")
            try:
                cat_choice = int(input("Choose category (1-5): "))
                category = list(ComplaintCategory)[cat_choice - 1]
                description = input("Enter complaint description: ")
                resident_id = input("Enter resident ID: ")
                complaint_id = system.raise_complaint(category, description, resident_id)
                print(f"\nComplaint raised successfully! ID: {complaint_id}")
            except (ValueError, IndexError):
                print("Invalid category choice!")
        elif choice == "2":
            complaint_id = input("Enter complaint ID: ")
            print("\nAvailable statuses:")
            for i, status in enumerate(ComplaintStatus, 1):
                print(f"{i}. {status.value.title()}")
            try:
                status_choice = int(input("Choose status (1-4): "))
                status = list(ComplaintStatus)[status_choice - 1]
                system.update_complaint_status(complaint_id, status)
            except (ValueError, IndexError):
                print("Invalid status choice!")
        elif choice == "3":
            complaint_id = input("Enter complaint ID: ")
            complaint = system.get_complaint_details(complaint_id)
            if complaint:
                print(f"\n--- Complaint Details ---")
                print(f"ID: {complaint['id']}")
                print(f"Category: {complaint['category']}")
                print(f"Description: {complaint['description']}")
                print(f"Status: {complaint['status']}")
                print(f"Resident ID: {complaint['resident_id']}")
                print(f"Technician: {complaint.get('technician_name', 'Not assigned')}")
                print(f"Created: {complaint['created_at']}")
                print(f"Updated: {complaint['updated_at']}")
            else:
                print("Complaint not found!")
        elif choice == "4":
            complaints = system.list_all_complaints()
            if complaints:
                print(f"\n--- All Complaints ({len(complaints)}) ---")
                for complaint in complaints:
                    print(f"ID: {complaint['id'][:8]}... | "
                          f"Category: {complaint['category']} | "
                          f"Status: {complaint['status']} | "
                          f"Technician: {complaint.get('technician_name', 'Not assigned')}")
            else:
                print("No complaints found!")
        elif choice == "5":
            import os
            import json

            # Adjust this path as needed if your file is elsewhere:
            json_path = os.path.join(os.path.dirname(__file__), "storage", "technicians.json")
            if os.path.exists(json_path):
                with open(json_path, "r") as f:
                    technicians = json.load(f)
                if technicians:
                    print(f"\n--- All Technicians ({len(technicians)}) ---")
                    for tech in technicians:
                        print(f"Name: {tech['name']} | "
                            f"Specializations: {', '.join(tech['specializations'])} | "
                            f"Available: {tech['is_available']}")
                else:
                    print("No technicians found in technicians.json!")
            else:
                print("technicians.json file not found!")

        elif choice == "6":
            print("Thank you for using Apartment Complaint Tracker!")
            break
        else:
            print("Invalid choice! Please enter 1-6.")

if __name__ == "__main__":
    main()
