import streamlit as st
from recruitment.crew import RecruitmentCrew

def build_job_yaml(title, description, responsibilities, requirements, preferred_qualifications, perks_and_benefits):
    return f"""
        job_requirement:
          title: >
            {title}
          description: >
            {description}
          responsibilities: >
            {responsibilities}
          requirements: >
            {requirements}
          preferred_qualifications: >
            {preferred_qualifications}
          perks_and_benefits: >
            {perks_and_benefits}
    """

def run_recruitment_ai(job_yaml: str):
    inputs = {"job_requirements": job_yaml}
    crew = RecruitmentCrew().crew()
    return crew.kickoff(inputs=inputs)

def render_tab3():
    st.title("🤖 Recruitment Assistant")
    st.markdown("Use autonomous AI agents to streamline your hiring process.")

    with st.form("job_form"):
        st.subheader("Job Requirement Input")
        title = st.text_input("Job Title", value="Ruby on Rails and React Engineer")

        description = st.text_area(
            "Job Description", 
            value=(
                "We are seeking a skilled Ruby on Rails and React engineer to join our team.\n"
                "The ideal candidate will have experience in both backend and frontend development,\n"
                "with a passion for building high-quality web applications."
            ), 
            height=150
        )

        responsibilities = st.text_area(
            "Responsibilities", 
            value=(
                "- Develop and maintain web applications using Ruby on Rails and React.\n"
                "- Collaborate with teams to define and implement new features.\n"
                "- Write clean, maintainable, and efficient code.\n"
                "- Ensure application performance and responsiveness.\n"
                "- Identify and resolve bottlenecks and bugs."
            ), 
            height=100
        )

        requirements = st.text_area(
            "Requirements", 
            value=(
                "- Proven experience with Ruby on Rails and React.\n"
                "- Strong understanding of object-oriented programming.\n"
                "- Proficiency with JavaScript, HTML, CSS, and React.\n"
                "- Experience with SQL or NoSQL databases.\n"
                "- Familiarity with code versioning tools, such as Git."
            ), 
            height=100
        )

        preferred_qualifications = st.text_area(
            "Preferred Qualifications", 
            value=(
                "- Experience with cloud services (AWS, Google Cloud, or Azure).\n"
                "- Familiarity with Docker and Kubernetes.\n"
                "- Knowledge of GraphQL.\n"
                "- Bachelor's degree in Computer Science or a related field."
            ), 
            height=100
        )

        perks_and_benefits = st.text_area(
            "Perks and Benefits", 
            value=(
                "- Competitive salary and bonuses.\n"
                "- Health, dental, and vision insurance.\n"
                "- Flexible working hours and remote work options.\n"
                "- Professional development opportunities."
            ), 
            height=100
        )

        submitted = st.form_submit_button("Run Recruitment AI")


    if submitted:
        job_yaml = build_job_yaml(
            title, description, responsibilities,
            requirements, preferred_qualifications, perks_and_benefits
        )

        with st.spinner("⏳ Running recruitment agents..."):
            try:
                result = run_recruitment_ai(job_yaml)
                st.success("🎉 Recruitment process completed!")
                st.subheader("📋 AI Generated Candidate Report")
                st.markdown(result)
            except Exception as e:
                st.error(f"❌ Error running recruitment crew: {e}")
