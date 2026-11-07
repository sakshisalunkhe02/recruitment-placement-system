import mysql.connector
from db import get_db_connection

# ==================== USER OPERATIONS ====================

def register_user(username, email, password, role):
    conn = get_db_connection()
    if conn is None:
        return
    cursor = conn.cursor()
    query = "INSERT INTO users (username, email, password, role) VALUES (%s, %s, %s, %s)"
    try:
        cursor.execute(query, (username, email, password, role))
        conn.commit()
        print(f"User '{username}' registered successfully as {role}!")
    except mysql.connector.Error as err:
        print(f"Error registering user: {err}")
    finally:
        cursor.close()
        conn.close()

def get_all_users():
    conn = get_db_connection()
    if conn is None:
        return []
    cursor = conn.cursor(dictionary=True)
    query = "SELECT user_id, username, email, role, created_at FROM users"
    cursor.execute(query)
    users = cursor.fetchall()
    cursor.close()
    conn.close()
    return users

# ==================== COMPANY OPERATIONS ====================

def add_company(company_name, industry, location):
    conn = get_db_connection()
    if conn is None:
        return
    cursor = conn.cursor()
    query = "INSERT INTO companies (company_name, industry, location) VALUES (%s, %s, %s)"
    try:
        cursor.execute(query, (company_name, industry, location))
        conn.commit()
        print(f"Company '{company_name}' added successfully!")
    except mysql.connector.Error as err:
        print(f"Error adding company: {err}")
    finally:
        cursor.close()
        conn.close()

# ==================== JOB OPERATIONS ====================

def add_job(company_id, title, description, salary_range):
    conn = get_db_connection()
    if conn is None:
        return
    cursor = conn.cursor()
    query = "INSERT INTO jobs (company_id, title, description, salary_range) VALUES (%s, %s, %s, %s)"
    try:
        cursor.execute(query, (company_id, title, description, salary_range))
        conn.commit()
        print(f"Job posting '{title}' added successfully!")
    except mysql.connector.Error as err:
        print(f"Error adding job: {err}")
    finally:
        cursor.close()
        conn.close()

def get_open_jobs():
    conn = get_db_connection()
    if conn is None:
        return []
    cursor = conn.cursor(dictionary=True)
    query = """
        SELECT j.job_id, j.title, j.salary_range, c.company_name, c.location
        FROM jobs j
        JOIN companies c ON j.company_id = c.company_id
        WHERE j.status = 'open'
    """
    cursor.execute(query)
    jobs = cursor.fetchall()
    cursor.close()
    conn.close()
    return jobs

# ==================== APPLICATION OPERATIONS ====================

def apply_for_job(job_id, user_id):
    conn = get_db_connection()
    if conn is None:
        return
    cursor = conn.cursor()
    query = "INSERT INTO applications (job_id, user_id) VALUES (%s, %s)"
    try:
        cursor.execute(query, (job_id, user_id))
        conn.commit()
        print(f"Application submitted successfully for Job ID {job_id}!")
    except mysql.connector.Error as err:
        print(f"Error applying for job: {err}")
    finally:
        cursor.close()
        conn.close()

def update_application_status(application_id, status):
    conn = get_db_connection()
    if conn is None:
        return
    cursor = conn.cursor()
    query = "UPDATE applications SET status = %s WHERE application_id = %s"
    try:
        cursor.execute(query, (status, application_id))
        conn.commit()
        print(f"Application ID {application_id} updated to status '{status}'!")
    except mysql.connector.Error as err:
        print(f"Error updating application status: {err}")
    finally:
        cursor.close()
        conn.close()
        
def get_candidate_applications(user_id):
    conn = get_db_connection()
    if conn is None:
        return []
    cursor = conn.cursor(dictionary=True)
    query = """
        SELECT a.application_id, j.title, c.company_name, a.status
        FROM applications a
        JOIN jobs j ON a.job_id = j.job_id
        JOIN companies c ON j.company_id = c.company_id
        WHERE a.user_id = %s
    """
    cursor.execute(query, (user_id,))
    applications = cursor.fetchall()
    cursor.close()
    conn.close()
    return applications

def get_all_applications():
    conn = get_db_connection()
    if conn is None:
        return []
    cursor = conn.cursor(dictionary=True)
    query = """
        SELECT a.application_id, u.username AS candidate_name, u.email AS candidate_email,
               j.title AS job_title, c.company_name, a.status
        FROM applications a
        JOIN users u ON a.user_id = u.user_id
        JOIN jobs j ON a.job_id = j.job_id
        JOIN companies c ON j.company_id = c.company_id
    """
    cursor.execute(query)
    applications = cursor.fetchall()
    cursor.close()
    conn.close()
    return applications