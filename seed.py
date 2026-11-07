from operations import register_user, add_company, add_job

def seed_database():
    print("🌱 Seeding database with initial data...")

    # 1. Register Sample Users
    register_user("admin_user", "admin@recruitment.com", "admin123", "admin")
    register_user("tech_recruiter", "recruiter@techcorp.com", "rec123", "recruiter")
    register_user("john_candidate", "john@example.com", "john123", "candidate")
    register_user("sarah_candidate", "sarah@example.com", "sarah123", "candidate")

    # 2. Add Sample Companies
    # (Note: In your MySQL database, these will get company_id 1 and 2)
    add_company("Google India", "Information Technology", "Bangalore / Remote")
    add_company("TCS Digital", "Software Services", "Pune, Maharashtra")

    # 3. Add Sample Job Openings
    # Assuming Google India is ID 1 and TCS Digital is ID 2
    add_job(1, "Python Full Stack Developer", "Develop and maintain scalable web applications using Python, Django/Flask, and MySQL.", "$80k - $110k")
    add_job(1, "Machine Learning Engineer", "Design and train predictive machine learning models using Scikit-learn and TensorFlow.", "$95k - $130k")
    add_job(2, "Graduate Engineer Trainee", "Entry-level software development role focusing on enterprise software automation.", "4.5 LPA - 6.5 LPA")

    print("✅ Database seeding complete! You can now refresh your Streamlit app.")

if __name__ == "__main__":
    seed_database()