from operations import (
    register_user,
    get_all_users,
    add_company,
    add_job,
    get_open_jobs,
    apply_for_job,
    update_application_status
)

def main_menu():
    while True:
        print("\n=== RECRUITMENT & PLACEMENT MANAGEMENT SYSTEM ===")
        print("1. Register New User")
        print("2. List All Users")
        print("3. Add Company")
        print("4. Post a New Job")
        print("5. View Open Jobs")
        print("6. Apply for a Job")
        print("7. Update Application Status")
        print("8. Exit")
        
        choice = input("Enter choice (1-8): ").strip()

        if choice == '1':
            username = input("Enter username: ")
            email = input("Enter email: ")
            password = input("Enter password: ")
            role = input("Enter role (admin/recruiter/candidate): ")
            register_user(username, email, password, role)
        elif choice == '2':
            users = get_all_users()
            print("\n--- Registered Users ---")
            for u in users:
                print(f"ID: {u['user_id']} | User: {u['username']} | Role: {u['role']} | Email: {u['email']}")
        elif choice == '3':
            name = input("Enter company name: ")
            ind = input("Enter industry: ")
            loc = input("Enter location: ")
            add_company(name, ind, loc)
        elif choice == '4':
            cid = input("Enter company ID: ")
            title = input("Enter job title: ")
            desc = input("Enter job description: ")
            sal = input("Enter salary range: ")
            add_job(cid, title, desc, sal)
        elif choice == '5':
            jobs = get_open_jobs()
            print("\n--- Open Job Listings ---")
            for j in jobs:
                print(f"ID: {j['job_id']} | Title: {j['title']} | Company: {j['company_name']} | Location: {j['location']}")
        elif choice == '6':
            jid = input("Enter job ID: ")
            uid = input("Enter user (candidate) ID: ")
            apply_for_job(jid, uid)
        elif choice == '7':
            aid = input("Enter application ID: ")
            status = input("Enter new status (applied/shortlisted/rejected/hired): ")
            update_application_status(aid, status)
        elif choice == '8':
            print("Exiting system. Goodbye!")
            break
        else:
            print("Invalid choice, please try again.")

if __name__ == "__main__":
    main_menu()