import streamlit as st
import requests

st.set_page_config(page_title="AI Resume Builder", page_icon="📄", layout="centered")

st.title("📄 AI Resume Builder")

API_URL = "http://127.0.0.1:5000"

if "resume_generated" not in st.session_state:
    st.session_state.resume_generated = False

if not st.session_state.resume_generated:
    # Top section
    st.subheader("👤 Personal Information")
    name = st.text_input("Full Name")
    email = st.text_input("Email Address")
    phone = st.text_input("Phone Number")
    linkedin = st.text_input("LinkedIn Profile URL")
    github = st.text_input("GitHub Profile URL")

    # Summary
    st.subheader("🧠 Professional Summary")
    summary = st.text_area("Write a short professional summary")

    # Education
    st.subheader("🎓 Education")
    education = st.text_area("Education Details (Degree, University, Year)")

    # Skills & Tools
    st.subheader("🛠️ Skills & Tools")
    skills = st.text_area("Skills (comma separated)")
    technologies = st.text_area("Technologies & Tools (comma separated)")

    # Experience
    st.subheader("💼 Work / Internship Experience")
    experience = st.text_area("Details of Work or Internship Experience")

    # Awards & Certifications
    st.subheader("🏅 Awards & Certifications")
    awards = st.text_area("Awards and Certifications (if any)")

    if st.button("Generate Resume"):
        data = {
            "name": name,
            "email": email,
            "phone": phone,
            "linkedin": linkedin,
            "github": github,
            "summary": summary,
            "education": education,
            "skills": skills,
            "technologies": technologies,
            "experience": experience,
            "awards": awards
        }

        response = requests.post(f"{API_URL}/generate", json=data)
        result = response.json()

        if "resume" in result:
            st.session_state.resume_generated = True
            st.session_state.resume_text = result["resume"]
            st.rerun()
        else:
            st.error(result.get("error", "Error generating resume."))

else:
    st.markdown("### 📄 Generated Resume")
    st.write(st.session_state.resume_text)

    if st.button("Download as DOCX"):
        save_response = requests.post(f"{API_URL}/save", json={"resume": st.markdown(st.session_state.resume_text, unsafe_allow_html=True)
})
        save_data = save_response.json()
        filename = save_data.get("filename", "resume.docx")
        with open(filename, "rb") as f:
            st.download_button("⬇️ Download Resume", f, file_name=filename)

    if st.button("🔄 Create Another Resume"):
        st.session_state.resume_generated = False
        st.session_state.resume_text = ""
        st.rerun()
