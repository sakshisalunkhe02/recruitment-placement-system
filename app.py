import streamlit as st
from operations import (
    register_user,
    get_all_users,
    add_company,
    add_job,
    get_open_jobs,
    apply_for_job,
    update_application_status,
    get_candidate_applications,
    get_all_applications
)

st.set_page_config(page_title="Recruitment & Placement System", page_icon="💼", layout="wide")

st.title("💼 Recruitment & Placement Management System")
st.write("Welcome to the campus placement and recruitment portal. Manage users, job postings, and applications seamlessly.")

# Sidebar navigation
menu = st.sidebar.selectbox("Navigation", [
    "View Open Jobs", 
    "Apply for a Job", 
    "My Applications", 
    "Recruiter Dashboard",
    "Analytics & Reports",
    "Post a Job (Recruiters)", 
    "Register User", 
    "Admin: View Users"
])

# ==================== VIEW OPEN JOBS ====================
if menu == "View Open Jobs":
    st.header("📋 Current Open Job Listings")
    jobs = get_open_jobs()
    
    if not jobs:
        st.info("No open job listings available right now.")
    else:
        # Search & Filter controls
        col1, col2 = st.columns(2)
        with col1:
            search_query = st.text_input("🔍 Search by Job Title", "").lower()
        with col2:
            locations = ["All"] + list(set(job['location'] for job in jobs))
            selected_location = st.selectbox("📍 Filter by Location", locations)
            
        # Filter logic
        filtered_jobs = jobs
        if search_query:
            filtered_jobs = [j for j in filtered_jobs if search_query in j['title'].lower()]
        if selected_location != "All":
            filtered_jobs = [j for j in filtered_jobs if j['location'] == selected_location]
            
        st.write(f"Showing **{len(filtered_jobs)}** open position(s)")
        st.divider()
        
        if not filtered_jobs:
            st.warning("No jobs match your search criteria.")
        else:
            for job in filtered_jobs:
                with st.container():
                    st.subheader(job['title'])
                    st.write(f"**Company:** {job['company_name']} | **Location:** {job['location']}")
                    st.write(f"**Salary Range:** {job['salary_range']}")
                    st.divider()

# ==================== APPLY FOR A JOB ====================
elif menu == "Apply for a Job":
    st.header("📝 Submit Job Application")
    
    jobs = get_open_jobs()
    users = get_all_users()
    
    # Filter candidates only
    candidates = [u for u in users if u['role'] == 'candidate']
    
    if not jobs:
        st.warning("No jobs available to apply for.")
    elif not candidates:
        st.warning("No candidate accounts found. Please register a candidate user first.")
    else:
        job_options = {f"{j['title']} at {j['company_name']} (ID: {j['job_id']})": j['job_id'] for j in jobs}
        candidate_options = {f"{c['username']} (ID: {c['user_id']})": c['user_id'] for c in candidates}
        
        selected_job_label = st.selectbox("Select Job", list(job_options.keys()))
        selected_candidate_label = st.selectbox("Select Candidate", list(candidate_options.keys()))
        
        if st.button("Submit Application"):
            job_id = job_options[selected_job_label]
            user_id = candidate_options[selected_candidate_label]
            apply_for_job(job_id, user_id)
            st.success("Application submitted successfully!")

# ==================== MY APPLICATIONS ====================
elif menu == "My Applications":
    st.header("📄 My Job Applications")
    
    users = get_all_users()
    candidates = [u for u in users if u['role'] == 'candidate']
    
    if not candidates:
        st.info("No candidate accounts found.")
    else:
        candidate_options = {f"{c['username']} (ID: {c['user_id']})": c['user_id'] for c in candidates}
        selected_candidate_label = st.selectbox("Select Candidate Profile", list(candidate_options.keys()))
        
        user_id = candidate_options[selected_candidate_label]
        applications = get_candidate_applications(user_id)
        
        if not applications:
            st.info("You haven't applied to any jobs yet.")
        else:
            for app in applications:
                with st.container():
                    st.subheader(app['title'])
                    st.write(f"**Company:** {app['company_name']}")
                    st.write(f"**Status:** `{app['status'].capitalize()}`")
                    st.divider()

# ==================== RECRUITER DASHBOARD ====================
elif menu == "Recruiter Dashboard":
    st.header("👔 Recruiter Dashboard: Manage Applications")
    
    applications = get_all_applications()
    
    if not applications:
        st.info("No applications submitted yet.")
    else:
        for app in applications:
            with st.container():
                st.subheader(f"Application ID: {app['application_id']} - {app['job_title']}")
                st.write(f"**Candidate:** {app['candidate_name']} ({app['candidate_email']}) | **Company:** {app['company_name']}")
                st.write(f"**Current Status:** `{app['status'].capitalize()}`")
                
                with st.form(key=f"status_form_{app['application_id']}"):
                    new_status = st.selectbox(
                        "Update Status", 
                        ["applied", "shortlisted", "rejected", "hired"],
                        index=["applied", "shortlisted", "rejected", "hired"].index(app['status'])
                    )
                    update_button = st.form_submit_button("Save Status")
                    
                    if update_button:
                        update_application_status(app['application_id'], new_status)
                        st.success(f"Application {app['application_id']} updated to '{new_status}'!")
                        st.rerun()
                st.divider()

# ==================== ANALYTICS & REPORTS ====================
elif menu == "Analytics & Reports":
    st.header("📊 Placement Analytics & System Metrics")
    
    users = get_all_users()
    jobs = get_open_jobs()
    applications = get_all_applications()
    
    total_users = len(users)
    candidates = [u for u in users if u['role'] == 'candidate']
    total_jobs = len(jobs)
    total_apps = len(applications)
    
    status_counts = {"applied": 0, "shortlisted": 0, "rejected": 0, "hired": 0}
    for app in applications:
        status = app['status'].lower()
        if status in status_counts:
            status_counts[status] += 1
            
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Users", total_users, f"{len(candidates)} Candidates")
    with col2:
        st.metric("Active Jobs", total_jobs)
    with col3:
        st.metric("Total Applications", total_apps)
    with col4:
        st.metric("Hired Candidates", status_counts["hired"])
        
    st.divider()
    
    st.subheader("📌 Application Status Breakdown")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Applied", status_counts["applied"])
    c2.metric("Shortlisted", status_counts["shortlisted"])
    c3.metric("Rejected", status_counts["rejected"])
    c4.metric("Hired", status_counts["hired"])
    
    if total_apps > 0:
        st.divider()
        st.subheader("📋 Recent Applications Overview")
        st.dataframe(applications, use_container_width=True)

# ==================== POST A JOB ====================
elif menu == "Post a Job (Recruiters)":
    st.header("🏢 Post a New Job / Add Company")
    
    with st.form("job_form"):
        st.subheader("1. Company Details")
        company_name = st.text_input("Company Name")
        industry = st.text_input("Industry")
        location = st.text_input("Location")
        
        st.subheader("2. Job Details")
        company_id = st.number_input("Company ID (If company already exists, enter ID)", min_value=0, step=1)
        title = st.text_input("Job Title")
        description = st.text_area("Job Description")
        salary_range = st.text_input("Salary Range (e.g., $60k - $80k)")
        
        submitted = st.form_submit_button("Post Job")
        if submitted:
            if company_name:
                add_company(company_name, industry, location)
            if title and company_id > 0:
                add_job(company_id, title, description, salary_range)
                st.success(f"Job '{title}' posted successfully!")
            else:
                st.error("Please provide a valid Company ID and Job Title.")

# ==================== REGISTER USER ====================
elif menu == "Register User":
    st.header("👤 User Registration")
    
    with st.form("reg_form"):
        username = st.text_input("Username")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        role = st.selectbox("Role", ["candidate", "recruiter", "admin"])
        
        submit_reg = st.form_submit_button("Register")
        if submit_reg:
            if username and email and password:
                register_user(username, email, password, role)
                st.success(f"User {username} registered successfully as {role}!")
            else:
                st.error("Please fill in all fields.")

# ==================== ADMIN: VIEW USERS ====================
elif menu == "Admin: View Users":
    st.header("Admin Dashboard: System Users")
    users = get_all_users()
    
    if not users:
        st.info("No registered users found.")
    else:
        st.dataframe(users, use_container_width=True)