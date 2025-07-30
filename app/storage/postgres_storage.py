from storage.interface import StorageInterface
from datetime import datetime

class PostgreSQLStorage(StorageInterface):
    def __init__(self, config):
        self.config = config
        try:
            import psycopg2
            from psycopg2.extras import RealDictCursor
            self.psycopg2 = psycopg2
            self.RealDictCursor = RealDictCursor
            self._initialize_tables() 
        except ImportError:
            self.psycopg2 = None
            print("psycopg2 not installed, simulation only.")

    def _get_connection(self):
        if self.psycopg2:
            return self.psycopg2.connect(**self.config)
        return None

    def _initialize_tables(self):
        with self._get_connection() as conn:
            with conn.cursor() as cur:
                # Technicians table
                cur.execute("""
                CREATE TABLE IF NOT EXISTS technicians (
                    id UUID PRIMARY KEY,
                    name TEXT NOT NULL,
                    specializations TEXT[] NOT NULL,
                    is_available BOOLEAN NOT NULL DEFAULT TRUE
                );
                """)
                # Complaints table
                cur.execute("""
                CREATE TABLE IF NOT EXISTS complaints (
                    id UUID PRIMARY KEY,
                    category TEXT NOT NULL,
                    description TEXT,
                    status TEXT NOT NULL,
                    resident_id TEXT NOT NULL,
                    technician_id UUID NULL REFERENCES technicians(id),
                    created_at TIMESTAMP NOT NULL,
                    updated_at TIMESTAMP NOT NULL
                );
                """)
                conn.commit()

    def save_complaint(self, complaint):
        if not self.psycopg2:
            print("[PostgreSQL] Save complaint: Simulation only.")
            return
        with self._get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO complaints (
                        id, category, description, status, resident_id,
                        technician_id, created_at, updated_at
                    ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
                """, (
                    complaint.id,
                    complaint.category.value,
                    complaint.description,
                    complaint.status.value,
                    complaint.resident_id,
                    complaint.technician_id,
                    complaint.created_at,
                    complaint.updated_at
                ))
                conn.commit()

    def get_complaint(self, complaint_id):
        if not self.psycopg2:
            print("[PostgreSQL] Get complaint: Simulation only.")
            return None
        with self._get_connection() as conn:
            with conn.cursor(cursor_factory=self.RealDictCursor) as cur:
                cur.execute("SELECT * FROM complaints WHERE id=%s", (complaint_id,))
                return cur.fetchone()

    def update_complaint(self, complaint_id, updates):
        if not self.psycopg2:
            print("[PostgreSQL] Update complaint: Simulation only.")
            return
        updates_to_set = updates.copy()
        if "status" in updates:
            updates_to_set["updated_at"] = datetime.now() 

        set_clause = ", ".join([f"{key}=%s" for key in updates_to_set])
        params = list(updates_to_set.values()) + [complaint_id]

        with self._get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(f"UPDATE complaints SET {set_clause} WHERE id=%s", params)
                conn.commit()

    def get_all_complaints(self):
        if not self.psycopg2:
            print("[PostgreSQL] Get all complaints: Simulation.")
            return []
        with self._get_connection() as conn:
            with conn.cursor(cursor_factory=self.RealDictCursor) as cur:
                cur.execute("SELECT * FROM complaints;")
                return cur.fetchall()

    def save_technician(self, technician):
        if not self.psycopg2:
            print("[PostgreSQL] Save technician: Simulation only.")
            return
        with self._get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO technicians (
                        id, name, specializations, is_available
                    ) VALUES (%s,%s,%s,%s)
                    ON CONFLICT (id) DO NOTHING
                """, (
                    technician.id,
                    technician.name,
                    [spec.value for spec in technician.specializations],
                    technician.is_available
                ))
                conn.commit()

    def get_all_technicians(self):
        if not self.psycopg2:
            print("[PostgreSQL] Get all techs: Simulation.")
            return []
        with self._get_connection() as conn:
            with conn.cursor(cursor_factory=self.RealDictCursor) as cur:
                cur.execute("SELECT * FROM technicians;")
                return cur.fetchall()

    def get_technician(self, technician_id):
        if not self.psycopg2:
            print("[PostgreSQL] Get technician: Simulation only.")
            return None
        with self._get_connection() as conn:
            with conn.cursor(cursor_factory=self.RealDictCursor) as cur:
                cur.execute("SELECT * FROM technicians WHERE id=%s", (technician_id,))
                return cur.fetchone()
