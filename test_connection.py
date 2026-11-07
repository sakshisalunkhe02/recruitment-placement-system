import mysql.connector

try:
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Sakshi@2004",  # Replace with your MySQL root password
        database="recruitment_db"
    )
    
    if db.is_connected():
        print("Successfully connected to recruitment_db!")
        
        cursor = db.cursor()
        cursor.execute("SHOW TABLES;")
        print("Tables found:")
        for table in cursor:
            print(f" - {table[0]}")
            
        cursor.close()
        db.close()

except mysql.connector.Error as err:
    print(f"Error connecting to MySQL: {err}")