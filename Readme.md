# Apartment Complaint Tracker

A Python project for managing apartment maintenance complaints and technician assignments with support for JSON, PostgreSQL, MongoDB, and MySQL/MariaDB storage.

---

## Features

- Raise and track maintenance complaints
- Automatic technician assignment based on specialization and availability
- Complaint status: pending, assigned, in progress, resolved
- Choose from JSON, PostgreSQL, MongoDB, or MySQL/MariaDB file/database storage
- Intuitive, menu-driven CLI
- Sample technician data auto-initialized

---

## Tech Stack

- **Python 3.8+**
- **Backends:** JSON, PostgreSQL, MongoDB, MySQL/MariaDB
- **Key libraries:** `psycopg2-binary`, `pymongo`, `mysql-connector-python`, `python-dotenv`

---



## Setup

1. **Clone the project**

    ```
    git clone https://github.com/neilplus21/aptcomplainttracker
    cd apartment_complaint_tracker
    ```

2. **Install Python dependencies**

    ```
    pip install -r requirements.txt
    ```

3. **Configure your environment variables**

    Create a `.env` file in the project root directory with the following content (edit as needed):

    ```
    # PostgreSQL
    POSTGRES_HOST=localhost
    POSTGRES_PORT=5432
    POSTGRES_DB=apartment_tracker
    POSTGRES_USER=your_pg_user
    POSTGRES_PASSWORD=your_pg_password

    # MongoDB
    MONGO_URI=mongodb://localhost:27017/
    MONGO_DB=apartment_tracker

    # MySQL
    MYSQL_HOST=localhost
    MYSQL_PORT=3306
    MYSQL_DB=apartment_tracker
    MYSQL_USER=your_mysql_user
    MYSQL_PASSWORD=your_mysql_password

    SECRET_KEY=your_random_secret_key_here
    ```

4. **(For SQL Backends) Prepare your empty database**

    With your MySQL/PostgreSQL server running, create the `apartment_tracker` database:

    **PostgreSQL:**
    ```
    CREATE DATABASE apartment_tracker;
    ```

    **MySQL:**
    ```
    CREATE DATABASE apartment_tracker;
    ```

    (No need for manual tables; the app creates them if needed.)

---

## Usage

1. **Launch the app:**

    ```
    python app/main.py
    ```

2. **Choose your storage backend:**  
    - `1` – Local JSON files
    - `2` – PostgreSQL
    - `3` – MongoDB
    - `4` – MySQL/MariaDB

3. **Manage complaints and technicians via the menu:**
    - Raise complaints
    - Update complaint status
    - List/view all complaints
    - View all technicians

---

## Data Storage

- **JSON:** Data is stored in `app/storage/complaints.json` and `app/storage/technicians.json`.
- **PostgreSQL / MongoDB / MySQL:** Data is saved in your database (tables/collections are auto-created).

---

## Environment Variables

Sensitive DB credentials and configuration are stored in the `.env` file. Never commit this file to version control!

---

## Troubleshooting

- **Can't connect:** Ensure DB server is running and credentials are correct in `.env`.
- **Table/relation does not exist:** Create the database ("CREATE DATABASE ...") first; restart the app to auto-create tables.
- **Permission errors:** Ensure the DB user has privileges to create tables and modify data.
- **MongoDB auth:** For authentication, update the URI in `.env` as needed.

---

## License

MIT

---

Enjoy tracking and resolving apartment maintenance complaints your way!
