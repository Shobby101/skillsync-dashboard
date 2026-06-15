
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import hashlib
import json
import os
import math
from datetime import datetime


# PAGE CONFIGURATION
st.set_page_config(
    page_title="Skill Sync Nigeria",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="collapsed"
)
 COLOR PALETTE
COLORS = {
    'primary': '#2C5F2D',
    'primary-light': '#4A7C59',
    'primary-dark': '#1E3A24',
    'primary-soft': '#E8F3E8',
    'secondary': '#D4A373',
    'secondary-light': '#EAD7C3',
    'success': '#2E7D32',
    'danger': '#C62828',
    'warning': '#ED6A2E',
    'info': '#2C7DA0',
    'dark': '#2D3A3A',
    'light': '#F5F7F5',
    'gray': '#6B7B6B',
    'gray-light': '#E2E6E2',
    'white': '#FFFFFF',
    'shadow': '0 4px 12px rgba(0,0,0,0.05)',
    'shadow-hover': '0 8px 24px rgba(0,0,0,0.1)',
    'gradient': 'linear-gradient(135deg, #2C5F2D 0%, #4A7C59 100%)',
    'gradient-soft': 'linear-gradient(135deg, #E8F3E8 0%, #F5F7F5 100%)'
}


#  CSS

st.markdown(f"""
<style>
    .main {{ background: {COLORS['light']}; }}
    
    .skillsync-header {{
        background: {COLORS['gradient']};
        padding: 16px 28px;
        border-radius: 16px;
        margin-bottom: 24px;
        box-shadow: {COLORS['shadow']};
    }}
    
    .logo-container {{
        display: flex;
        align-items: center;
        gap: 16px;
        flex-wrap: wrap;
    }}
    
    .logo-icon {{
        width: 48px;
        height: 48px;
        background: rgba(255,255,255,0.12);
        border-radius: 14px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.8em;
    }}
    
    .logo-text h1 {{
        margin: 0;
        font-size: 1.6em;
        letter-spacing: 0.5px;
        font-weight: 600;
    }}
    
    .logo-text .skill {{ color: {COLORS['white']}; }}
    .logo-text .sync {{ color: {COLORS['secondary']}; }}
    .logo-text .nigeria {{ color: {COLORS['white']}; opacity: 0.9; }}
    
    .tagline {{ margin-top: 8px; }}
    .tagline p {{ margin: 0; color: rgba(255,255,255,0.75); font-size: 0.75em; }}
    .tagline .separator {{ width: 50px; height: 2px; background: {COLORS['secondary']}; margin: 8px 0 0 0; border-radius: 2px; }}
    
    .top-nav {{
        background: {COLORS['white']};
        border-radius: 14px;
        padding: 6px 16px;
        margin-bottom: 24px;
        box-shadow: {COLORS['shadow']};
        border: 1px solid {COLORS['gray-light']};
    }}
    
    .stButton > button {{
        border-radius: 10px;
        background: {COLORS['gradient']};
        color: white;
        border: none;
        padding: 8px 16px;
        font-weight: 500;
        font-size: 0.85em;
        transition: all 0.2s ease;
    }}
    
    .stButton > button:hover {{
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(44, 95, 45, 0.3);
    }}
    
    div[data-testid="stMetric"] {{
        background: {COLORS['white']};
        padding: 16px;
        border-radius: 14px;
        box-shadow: {COLORS['shadow']};
        transition: all 0.2s ease;
        border: 1px solid {COLORS['gray-light']};
    }}
    
    div[data-testid="stMetric"]:hover {{
        transform: translateY(-2px);
        box-shadow: {COLORS['shadow-hover']};
    }}
    
    div[data-testid="stMetric"] label {{ color: {COLORS['gray']}; font-size: 0.8em; }}
    div[data-testid="stMetric"] div {{ color: {COLORS['primary']}; font-size: 1.6em; font-weight: 600; }}
    
    .stTabs [data-baseweb="tab-list"] {{
        gap: 4px;
        background: {COLORS['gray-light']};
        padding: 4px;
        border-radius: 10px;
    }}
    
    .stTabs [data-baseweb="tab"] {{
        border-radius: 8px;
        padding: 4px 14px;
        font-weight: 500;
        font-size: 0.8em;
    }}
    
    .stTabs [aria-selected="true"] {{
        background: {COLORS['gradient']};
        color: white;
    }}
    
    .streamlit-expanderHeader {{
        border-radius: 10px;
        background: {COLORS['primary-soft']};
        font-weight: 500;
        font-size: 0.85em;
        color: {COLORS['primary']};
    }}
    
    .stDataFrame {{
        border-radius: 12px;
        overflow: hidden;
        border: 1px solid {COLORS['gray-light']};
        font-size: 0.85em;
    }}
    
    h1 {{ font-size: 1.6em !important; font-weight: 600 !important; color: {COLORS['dark']} !important; margin-bottom: 16px !important; }}
    h2 {{ font-size: 1.3em !important; font-weight: 500 !important; color: {COLORS['dark']} !important; margin-bottom: 12px !important; }}
    h3 {{ font-size: 1.1em !important; font-weight: 500 !important; color: {COLORS['primary']} !important; margin-bottom: 10px !important; }}
    
    .profile-card {{
        background: {COLORS['white']};
        padding: 20px;
        border-radius: 16px;
        box-shadow: {COLORS['shadow']};
        margin-bottom: 16px;
        border: 1px solid {COLORS['gray-light']};
    }}
    
    .profile-avatar {{
        width: 80px;
        height: 80px;
        background: {COLORS['gradient-soft']};
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 2.5em;
        margin-bottom: 16px;
        border: 2px solid {COLORS['primary-light']};
    }}
    
    .activity-item {{
        padding: 8px 0;
        border-bottom: 1px solid {COLORS['gray-light']};
        font-size: 0.85em;
    }}
    
    .footer {{
        text-align: center;
        padding: 16px;
        margin-top: 32px;
        border-top: 1px solid {COLORS['gray-light']};
        color: {COLORS['gray']};
        font-size: 0.7em;
    }}
    
    @media (max-width: 768px) {{
        .logo-text h1 {{ font-size: 1.2em; }}
        .logo-icon {{ width: 40px; height: 40px; font-size: 1.4em; }}
        h1 {{ font-size: 1.3em !important; }}
        .stTabs [data-baseweb="tab"] {{ padding: 2px 10px; font-size: 0.7em; }}
    }}
</style>
""", unsafe_allow_html=True)

# USER AUTHENTICATION

USER_DB_FILE = 'users.json'
PROFILE_DB_FILE = 'profiles.json'

def init_user_db():
    if not os.path.exists(USER_DB_FILE):
        default_users = {
            "admin": {"password": hashlib.sha256("admin123".encode()).hexdigest(), "email": "admin@skillsync.com", "role": "admin", "created_at": datetime.now().strftime("%Y-%m-%d"), "full_name": "Administrator"},
            "student": {"password": hashlib.sha256("student123".encode()).hexdigest(), "email": "student@skillsync.com", "role": "user", "created_at": datetime.now().strftime("%Y-%m-%d"), "full_name": "Student User"}
        }
        with open(USER_DB_FILE, 'w') as f:
            json.dump(default_users, f)

def init_profile_db():
    if not os.path.exists(PROFILE_DB_FILE):
        with open(PROFILE_DB_FILE, 'w') as f:
            json.dump({}, f)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def verify_user(username, password):
    if not os.path.exists(USER_DB_FILE):
        init_user_db()
    with open(USER_DB_FILE, 'r') as f:
        users = json.load(f)
    return username in users and users[username]['password'] == hash_password(password)

def register_user(username, password, email, full_name=""):
    if not os.path.exists(USER_DB_FILE):
        init_user_db()
    with open(USER_DB_FILE, 'r') as f:
        users = json.load(f)
    if username in users:
        return False, "Username already exists"
    
    users[username] = {"password": hash_password(password), "email": email, "role": "user", "created_at": datetime.now().strftime("%Y-%m-%d"), "full_name": full_name}
    with open(USER_DB_FILE, 'w') as f:
        json.dump(users, f, indent=2)
    
    init_profile_db()
    with open(PROFILE_DB_FILE, 'r') as f:
        profiles = json.load(f)
    profiles[username] = {"full_name": full_name, "email": email, "avatar": "👤", "bio": "", "notification_preferences": {"email_updates": True, "market_alerts": True, "newsletter": False}}
    with open(PROFILE_DB_FILE, 'w') as f:
        json.dump(profiles, f, indent=2)
    return True, "Registration successful! Please log in."

def get_user_profile(username):
    init_profile_db()
    with open(PROFILE_DB_FILE, 'r') as f:
        profiles = json.load(f)
    return profiles.get(username, {})

def update_user_profile(username, profile_data):
    init_profile_db()
    with open(PROFILE_DB_FILE, 'r') as f:
        profiles = json.load(f)
    profiles[username] = profile_data
    with open(PROFILE_DB_FILE, 'w') as f:
        json.dump(profiles, f, indent=2)
    return True

def change_password(username, old_password, new_password):
    with open(USER_DB_FILE, 'r') as f:
        users = json.load(f)
    if users[username]['password'] != hash_password(old_password):
        return False, "Current password is incorrect"
    users[username]['password'] = hash_password(new_password)
    with open(USER_DB_FILE, 'w') as f:
        json.dump(users, f, indent=2)
    return True, "Password changed successfully"

init_user_db()
init_profile_db()

# SESSION STATE

def init_session_state():
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if 'username' not in st.session_state:
        st.session_state.username = None
    if 'page' not in st.session_state:
        st.session_state.page = "Dashboard"

init_session_state()

# HEADER & NAVIGATION

def show_skillsync_header():
    st.markdown(f"""
    <div class="skillsync-header">
        <div class="logo-container">
            <div class="logo-icon">🎯</div>
            <div class="logo-text">
                <h1><span class="skill">SKILL</span><span class="sync">SYNC</span><span class="nigeria"> NIGERIA</span></h1>
            </div>
        </div>
        <div class="tagline">
            <p>TECH SKILLS INTELLIGENCE PLATFORM</p>
            <div class="separator"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def show_top_navigation():
    nav_items = ["Dashboard", "Gap Analysis", "Technical Bundles", "Design Bundles", "Recommendations", "Data", "Profile"]
    cols = st.columns(len(nav_items))
    for idx, item in enumerate(nav_items):
        with cols[idx]:
            is_active = st.session_state.page == item
            if st.button(item, key=f"nav_{item}", use_container_width=True, type="primary" if is_active else "secondary"):
                st.session_state.page = item
                st.rerun()

def logout():
    st.session_state.logged_in = False
    st.session_state.username = None
    st.rerun()

# DATA LOADING

@st.cache_data
def load_gap_analysis():
    try:
        df = pd.read_csv('skills_gap_analysis.csv')
        return df
    except:
        return pd.DataFrame({
            'skill': ['Python', 'AWS', 'Docker', 'SQL', 'React', 'Java', 'JavaScript', 'Machine Learning', 
                      'Kubernetes', 'Terraform', 'Node.js', 'PostgreSQL', 'MongoDB', 'Django', 'Spring Boot',
                      'TypeScript', 'Go', 'Rust', 'GraphQL', 'Redis', 'Kafka', 'Spark', 'TensorFlow', 'PyTorch',
                      'Angular', 'Vue.js', 'C#', 'PHP', 'Ruby', 'Swift', 'Kotlin', 'Flutter'],
            'demand_percentage': [65, 45, 38, 55, 35, 40, 50, 28, 32, 25, 42, 30, 28, 33, 35, 30, 22, 15, 20, 25, 18, 22, 28, 25, 32, 28, 30, 20, 18, 15, 20, 22],
            'supply_percentage': [45, 12, 15, 50, 25, 30, 55, 10, 8, 6, 20, 15, 18, 12, 10, 15, 8, 3, 8, 10, 5, 6, 10, 8, 20, 15, 25, 30, 15, 8, 12, 10],
            'gap_score': [20, 33, 23, 5, 10, 10, -5, 18, 24, 19, 22, 15, 10, 21, 25, 15, 14, 12, 12, 15, 13, 16, 18, 17, 12, 13, 5, -10, 3, 7, 8, 12],
            'status': ['Shortage', 'Critical', 'Shortage', 'Balanced', 'Shortage', 'Shortage', 'Surplus', 'Shortage', 
                       'Critical', 'Shortage', 'Shortage', 'Shortage', 'Shortage', 'Shortage', 'Shortage', 'Shortage',
                       'Shortage', 'Shortage', 'Shortage', 'Shortage', 'Shortage', 'Shortage', 'Shortage', 'Shortage',
                       'Shortage', 'Shortage', 'Balanced', 'Surplus', 'Balanced', 'Shortage', 'Shortage', 'Shortage']
        })

@st.cache_data
def load_technical_skill_bundles():
    try:
        df = pd.read_csv('technical_skill_bundles.csv')
        if len(df) < 40:
            sample_bundles = pd.DataFrame({
                'antecedents': ['AWS', 'Docker', 'Python', 'React', 'Kubernetes', 'Git', 'TensorFlow', 'PostgreSQL', 
                               'Java', 'MongoDB', 'Node.js', 'Django', 'Linux', 'Jenkins', 'Spring Boot', 'Angular',
                               'TypeScript', 'GraphQL', 'Redis', 'Kafka', 'Spark', 'Go', 'Rust', 'PyTorch', 'Vue.js',
                               'Flutter', 'Swift', 'Kotlin', 'C#', 'PHP', 'Ruby', 'Terraform', 'Ansible', 'Prometheus'],
                'consequents': ['Docker', 'Kubernetes', 'SQL', 'Node.js', 'Terraform', 'CI/CD', 'Python', 'Django',
                               'Spring Boot', 'Node.js', 'React', 'PostgreSQL', 'AWS', 'Docker', 'Java', 'TypeScript',
                               'JavaScript', 'React', 'Python', 'Spark', 'Python', 'Docker', 'Python', 'TensorFlow',
                               'JavaScript', 'Dart', 'iOS', 'Android', '.NET', 'Laravel', 'Rails', 'AWS', 'Docker', 'Grafana'],
                'lift': [4.52, 4.21, 3.87, 3.65, 3.54, 3.48, 3.42, 3.21, 3.15, 2.95, 2.88, 2.76, 2.68, 2.54, 2.48, 2.35,
                        2.28, 2.18, 2.08, 1.98, 1.88, 1.78, 1.68, 1.58, 2.45, 2.38, 2.28, 2.18, 2.08, 1.98, 1.88, 2.78, 2.68, 2.58],
                'confidence': [0.78, 0.82, 0.75, 0.71, 0.83, 0.69, 0.88, 0.79, 0.74, 0.68, 0.72, 0.70, 0.76, 0.65, 0.71, 0.68,
                              0.73, 0.66, 0.69, 0.62, 0.64, 0.70, 0.72, 0.65, 0.70, 0.68, 0.65, 0.63, 0.66, 0.60, 0.58, 0.72, 0.70, 0.68]
            })
            df = pd.concat([df, sample_bundles], ignore_index=True)
        return df
    except:
        return pd.DataFrame({
            'antecedents': ['AWS', 'Docker', 'Python', 'React', 'Kubernetes', 'Git', 'TensorFlow', 'PostgreSQL', 'Java', 'MongoDB', 'Node.js', 'Django'],
            'consequents': ['Docker', 'Kubernetes', 'SQL', 'Node.js', 'Terraform', 'CI/CD', 'Python', 'Django', 'Spring Boot', 'Node.js', 'React', 'PostgreSQL'],
            'lift': [4.52, 4.21, 3.87, 3.65, 3.54, 3.48, 3.42, 3.21, 3.15, 2.95, 2.88, 2.76],
            'confidence': [0.78, 0.82, 0.75, 0.71, 0.83, 0.69, 0.88, 0.79, 0.74, 0.68, 0.72, 0.70]
        })

@st.cache_data
def load_design_skill_bundles():
    try:
        df = pd.read_csv('skill_bundles_apriori.csv')
        design_keywords = ['Figma', 'Adobe', 'Prototyping', 'Wireframing', 'User Research', 'Usability', 'Visual Design', 'Design Systems', 'Sketch', 'InVision']
        mask = df['antecedents'].str.contains('|'.join(design_keywords), case=False, na=False) | \
               df['consequents'].str.contains('|'.join(design_keywords), case=False, na=False)
        return df[mask].head(40)
    except:
        return pd.DataFrame({
            'antecedents': ['Figma', 'Adobe Xd', 'Prototyping', 'User Research', 'Wireframing', 'Visual Design', 'Usability Testing', 'Design Systems', 'Sketch', 'InVision', 'Miro', 'Zeplin'],
            'consequents': ['Adobe Xd', 'Figma', 'Usability Testing', 'Wireframing', 'Figma', 'Design Systems', 'User Research', 'Visual Design', 'Figma', 'Sketch', 'Figma', 'Figma'],
            'lift': [24.6, 23.7, 22.9, 21.5, 20.8, 19.2, 18.5, 17.8, 16.5, 15.2, 14.8, 14.2],
            'confidence': [0.97, 0.96, 0.95, 0.94, 0.93, 0.92, 0.91, 0.90, 0.89, 0.88, 0.87, 0.86]
        })

# LEARNING RESOURCES DATABASE

LEARNING_RESOURCES = {
    'Python': {
        'courses': ['Python for Everybody (Coursera)', '100 Days of Code (Udemy)', 'Google IT Automation with Python (Coursera)'],
        'certifications': ['PCEP - Certified Entry-Level Python Programmer', 'PCAP - Certified Associate in Python Programming'],
        'practice': ['LeetCode', 'HackerRank', 'CodeSignal'],
        'youtube': ['freeCodeCamp Python Course', 'Programming with Mosh'],
        'projects': ['Build a web scraper', 'Create a REST API with Django/Flask', 'Data analysis with Pandas']
    },
    'AWS': {
        'courses': ['AWS Certified Solutions Architect (Coursera)', 'AWS Cloud Practitioner (AWS Training)', 'Ultimate AWS Certified Solutions Architect (Udemy)'],
        'certifications': ['AWS Certified Cloud Practitioner', 'AWS Solutions Architect Associate', 'AWS Developer Associate'],
        'practice': ['AWS Skill Builder', 'A Cloud Guru', 'Tutorials Dojo'],
        'youtube': ['freeCodeCamp AWS Course', 'Stephane Maarek AWS Course'],
        'projects': ['Deploy a web app on EC2', 'Build a serverless API with Lambda', 'Create a static website on S3']
    },
    'Docker': {
        'courses': ['Docker Mastery (Udemy)', 'Docker for Beginners (Coursera)', 'Docker and Kubernetes (freeCodeCamp)'],
        'certifications': ['Docker Certified Associate (DCA)'],
        'practice': ['Play-with-Docker', 'Katacoda Docker Scenarios'],
        'youtube': ['TechWorld with Nana Docker Tutorial', 'freeCodeCamp Docker Course'],
        'projects': ['Containerize a web application', 'Set up multi-container with Docker Compose', 'Build a dev environment']
    },
    'SQL': {
        'courses': ['SQL for Data Science (Coursera)', 'The Complete SQL Bootcamp (Udemy)', 'SQL for Beginners (DataCamp)'],
        'certifications': ['Oracle SQL Certification', 'Microsoft SQL Server Certification'],
        'practice': ['SQLZoo', 'LeetCode Database Section', 'HackerRank SQL'],
        'youtube': ['freeCodeCamp SQL Course', 'CS50 SQL'],
        'projects': ['Design a database for an e-commerce site', 'Write complex queries for analytics', 'Build a reporting dashboard']
    },
    'React': {
        'courses': ['React - The Complete Guide (Udemy)', 'Frontend Masters React', 'Meta React Native Course (Coursera)'],
        'certifications': ['Meta Frontend Developer Professional Certificate'],
        'practice': ['React Official Tutorial', 'Scrimba React Course', 'Codecademy React'],
        'youtube': ['freeCodeCamp React Course', 'Traversy Media React'],
        'projects': ['Build a todo app', 'Create a portfolio website', 'Develop an e-commerce frontend']
    }
}


# COMPREHENSIVE LEARNING RECOMMENDATIONS 

LEARNING_RECOMMENDATIONS = {
    'Software Developer': {
        'priority_skills': ['Python', 'Java', 'JavaScript', 'Data Structures', 'Algorithms', 'Git', 'SQL', 'OOP', 'Debugging', 'REST APIs'],
        'skill_bundles': ['Python + SQL + Git', 'Java + Spring Boot + SQL', 'JavaScript + Node.js + Express'],
        'courses': ['CS50: Introduction to Computer Science (Harvard/edX)', 'Python for Everybody (Coursera)', 'Data Structures and Algorithms (Udacity)', 'The Complete Java Developer Course (Udemy)'],
        'certifications': ['Oracle Certified Professional', 'Microsoft Certified: Azure Developer', 'AWS Certified Developer']
    },
    'Frontend Developer': {
        'priority_skills': ['JavaScript', 'React', 'HTML5', 'CSS3', 'TypeScript', 'Git', 'Redux', 'Responsive Design', 'Tailwind CSS', 'Next.js'],
        'skill_bundles': ['React + Redux + JavaScript', 'HTML/CSS + JavaScript + React', 'TypeScript + React + Next.js'],
        'courses': ['The Complete JavaScript Course (Udemy)', 'React - The Complete Guide (Udemy)', 'Frontend Masters Bootcamp', 'Advanced CSS and Sass (Udemy)'],
        'certifications': ['Meta Frontend Developer Professional Certificate', 'FreeCodeCamp Frontend Certification']
    },
    'Backend Developer': {
        'priority_skills': ['Python', 'Node.js', 'SQL', 'REST APIs', 'Django', 'PostgreSQL', 'Git', 'Docker', 'MongoDB', 'Express.js'],
        'skill_bundles': ['Python + Django + PostgreSQL', 'Node.js + Express + MongoDB', 'Java + Spring Boot + SQL'],
        'courses': ['Django for Beginners (Real Python)', 'Node.js Advanced Concepts (Udemy)', 'API Design and Development (Pluralsight)', 'Backend Development with Spring Boot (Coursera)'],
        'certifications': ['MongoDB Certified Developer', 'Oracle Java Certification', 'PostgreSQL Certification']
    },
    'Full Stack Developer': {
        'priority_skills': ['JavaScript', 'Python', 'React', 'Node.js', 'SQL', 'Git', 'HTML/CSS', 'MongoDB', 'Docker', 'REST APIs'],
        'skill_bundles': ['React + Node.js + MongoDB', 'Python + Django + PostgreSQL', 'JavaScript + React + Express'],
        'courses': ['The Complete Full-Stack Web Development Bootcamp (Udemy)', 'Full Stack Open (University of Helsinki)', 'MERN Stack Front To Back (Udemy)', 'Full Stack Web Development with React (Coursera)'],
        'certifications': ['Meta Backend Developer Professional Certificate', 'IBM Full Stack Developer Certificate']
    },
    'Data Scientist': {
        'priority_skills': ['Python', 'Machine Learning', 'SQL', 'Statistics', 'Pandas', 'NumPy', 'Data Visualization', 'TensorFlow', 'Scikit-learn', 'Deep Learning'],
        'skill_bundles': ['Python + Pandas + NumPy', 'Machine Learning + Scikit-learn + Python', 'TensorFlow + Python + Deep Learning'],
        'courses': ['Machine Learning Specialization (Andrew Ng/Coursera)', 'Data Science Professional Certificate (Harvard/edX)', 'Deep Learning Specialization (DeepLearning.ai)', 'Python for Data Science (DataCamp)'],
        'certifications': ['TensorFlow Developer Certificate', 'AWS Certified Data Analytics', 'IBM Data Science Professional']
    },
    'Data Analyst': {
        'priority_skills': ['SQL', 'Excel', 'Python', 'Tableau', 'Power BI', 'Data Visualization', 'Statistics', 'Data Cleaning', 'Pandas', 'Business Intelligence'],
        'skill_bundles': ['SQL + Tableau + Python', 'Excel + Power BI + SQL', 'Python + Pandas + Data Visualization'],
        'courses': ['Google Data Analytics Professional Certificate (Coursera)', 'SQL for Data Science (Coursera)', 'Tableau Training (Udemy)', 'Power BI Masterclass (Udemy)'],
        'certifications': ['Microsoft Power BI Data Analyst', 'Tableau Desktop Specialist', 'Google Data Analytics']
    },
    'Data Engineer': {
        'priority_skills': ['Python', 'SQL', 'Spark', 'Airflow', 'AWS', 'Big Data', 'ETL', 'Kafka', 'Hadoop', 'Data Warehousing'],
        'skill_bundles': ['Python + Spark + SQL', 'AWS + Airflow + Python', 'Kafka + Spark + Big Data'],
        'courses': ['Data Engineering with Python (DataCamp)', 'AWS Certified Data Analytics (Coursera)', 'Apache Spark for Data Engineering (Udemy)', 'Data Engineering on Google Cloud (Coursera)'],
        'certifications': ['AWS Certified Data Analytics', 'Google Cloud Data Engineer', 'Databricks Certified Engineer']
    },
    'DevOps Engineer': {
        'priority_skills': ['AWS', 'Docker', 'Kubernetes', 'Terraform', 'Linux', 'CI/CD', 'Jenkins', 'Python', 'Bash', 'Git'],
        'skill_bundles': ['AWS + Docker + Kubernetes', 'Docker + Kubernetes + Terraform', 'Jenkins + Docker + CI/CD'],
        'courses': ['AWS Certified Solutions Architect (Coursera)', 'Docker Mastery (Udemy)', 'Kubernetes for Developers (Linux Academy)', 'Terraform Associate Certification Course'],
        'certifications': ['AWS Certified DevOps Engineer', 'Certified Kubernetes Administrator (CKA)', 'Terraform Associate']
    },
    'Cloud Engineer': {
        'priority_skills': ['AWS', 'Azure', 'Google Cloud', 'Docker', 'Kubernetes', 'Terraform', 'Linux', 'Networking', 'Python', 'CI/CD'],
        'skill_bundles': ['AWS + Terraform + Docker', 'AWS + Python + Linux', 'Azure + Docker + Kubernetes'],
        'courses': ['AWS Certified Solutions Architect (Coursera)', 'Google Cloud Engineer Training (Coursera)', 'Azure Administrator Certification (Microsoft)', 'Cloud Computing with AWS (edX)'],
        'certifications': ['AWS Solutions Architect', 'Google Cloud Engineer', 'Azure Administrator']
    },
    'Cybersecurity Analyst': {
        'priority_skills': ['Network Security', 'Firewalls', 'SIEM', 'Incident Response', 'Linux', 'Python', 'Risk Assessment', 'Penetration Testing', 'Cryptography', 'Compliance'],
        'skill_bundles': ['Firewalls + Network Security + SIEM', 'Incident Response + SIEM + Linux', 'Penetration Testing + Python + Linux'],
        'courses': ['Certified Information Systems Security Professional (CISSP) Prep', 'CompTIA Security+ (Cybrary)', 'Practical Ethical Hacking (TCM Security)', 'Introduction to Cybersecurity (Cisco)'],
        'certifications': ['CompTIA Security+', 'CISSP', 'CEH', 'GIAC', 'CISM']
    },
    'Mobile Developer (Android)': {
        'priority_skills': ['Kotlin', 'Android Studio', 'Java', 'REST APIs', 'Git', 'Firebase', 'SQLite', 'Material Design', 'Jetpack Compose', 'Gradle'],
        'skill_bundles': ['Kotlin + Android Studio + Firebase', 'Java + REST APIs + Git', 'Android + Material Design + SQLite'],
        'courses': ['Android Development with Kotlin (Google/Udacity)', 'Android App Development Masterclass (Udemy)', 'Firebase for Android (Coursera)', 'Kotlin for Java Developers (Coursera)'],
        'certifications': ['Google Associate Android Developer', 'Meta Android Developer Certificate']
    },
    'Mobile Developer (iOS)': {
        'priority_skills': ['Swift', 'iOS', 'Xcode', 'UIKit', 'SwiftUI', 'REST APIs', 'Git', 'Core Data', 'Firebase', 'App Store Deployment'],
        'skill_bundles': ['Swift + Xcode + UIKit', 'iOS + SwiftUI + Core Data', 'Swift + REST APIs + Firebase'],
        'courses': ['iOS Development with Swift (Apple/Udacity)', 'SwiftUI Masterclass (Udemy)', 'iOS App Development Bootcamp (Coursera)', 'Advanced iOS Development (Pluralsight)'],
        'certifications': ['Apple Certified iOS Developer', 'Meta iOS Developer Certificate']
    },
    'Mobile Developer (Cross-Platform)': {
        'priority_skills': ['Flutter', 'Dart', 'React Native', 'JavaScript', 'REST APIs', 'Git', 'Firebase', 'Mobile UI', 'State Management', 'App Deployment'],
        'skill_bundles': ['Flutter + Dart + Firebase', 'React Native + JavaScript + Redux', 'Flutter + REST APIs + Git'],
        'courses': ['Flutter & Dart - The Complete Guide (Udemy)', 'React Native - The Practical Guide (Udemy)', 'Cross-Platform Mobile Development (Coursera)', 'Firebase for Mobile Apps (Google)'],
        'certifications': ['Google Flutter Certification', 'Meta React Native Certificate']
    },
    'UI/UX Designer': {
        'priority_skills': ['Figma', 'User Research', 'Wireframing', 'Prototyping', 'Visual Design', 'Adobe Xd', 'Usability Testing', 'Design Systems', 'Information Architecture', 'Interaction Design'],
        'skill_bundles': ['Figma + Adobe Xd + Wireframing', 'User Research + Usability Testing', 'Prototyping + Visual Design + Design Systems'],
        'courses': ['Google UX Design Certificate (Coursera)', 'Figma UI/UX Design Essentials (Udemy)', 'Interaction Design Specialization (UC San Diego)', 'Design Systems Masterclass (Figma)'],
        'certifications': ['Google UX Design Certificate', 'Certified Usability Analyst', 'NN/g UX Certification']
    },
    'Product Manager': {
        'priority_skills': ['Agile', 'Scrum', 'Product Strategy', 'User Research', 'Data Analysis', 'Roadmapping', 'JIRA', 'Stakeholder Management', 'Market Research', 'MVP'],
        'skill_bundles': ['Agile + Scrum + JIRA', 'Product Strategy + Roadmapping + User Research', 'Data Analysis + Market Research + MVP'],
        'courses': ['Product Management Specialization (University of Virginia/Coursera)', 'Agile Product Management (Google/Coursera)', 'Become a Product Manager (LinkedIn Learning)', 'Product Management 101 (Udemy)'],
        'certifications': ['Certified Scrum Product Owner (CSPO)', 'Product Management Certification (PMI)']
    },
    'QA Engineer': {
        'priority_skills': ['Test Automation', 'Selenium', 'Manual Testing', 'JIRA', 'API Testing', 'Python', 'Regression Testing', 'CI/CD', 'Postman', 'Agile'],
        'skill_bundles': ['Selenium + Python + Test Automation', 'JIRA + Manual Testing + Agile', 'Postman + API Testing + CI/CD'],
        'courses': ['Selenium WebDriver with Python (Udemy)', 'Software Testing and Automation (Coursera)', 'API Testing with Postman (Udemy)', 'ISTQB Foundation Certification Prep'],
        'certifications': ['ISTQB Certified Tester', 'Certified Test Automation Engineer', 'Selenium Certification']
    },
    'Network Engineer': {
        'priority_skills': ['TCP/IP', 'Routing', 'Switching', 'Firewalls', 'Cisco', 'VPN', 'Network Security', 'BGP', 'OSPF', 'Wireshark'],
        'skill_bundles': ['Cisco + Routing + Switching', 'TCP/IP + Network Security + Firewalls', 'BGP + OSPF + Routing'],
        'courses': ['Cisco CCNA Certification (Cisco)', 'Network Security Fundamentals (Coursera)', 'TCP/IP and Networking Basics (Udemy)', 'Advanced Routing and Switching (Pluralsight)'],
        'certifications': ['CCNA', 'CCNP', 'CompTIA Network+', 'Cisco CyberOps']
    },
    'Database Administrator': {
        'priority_skills': ['SQL', 'PostgreSQL', 'MySQL', 'Database Design', 'Performance Tuning', 'Backup Recovery', 'Query Optimization', 'MongoDB', 'High Availability', 'Linux'],
        'skill_bundles': ['SQL + PostgreSQL + Database Design', 'MySQL + Performance Tuning + Linux', 'MongoDB + SQL + Backup Recovery'],
        'courses': ['SQL for Database Administrators (Coursera)', 'PostgreSQL Administration (Udemy)', 'MySQL Database Administration (Pluralsight)', 'MongoDB for DBAs (MongoDB University)'],
        'certifications': ['Oracle DBA Certification', 'Microsoft SQL Server Certification', 'MongoDB DBA']
    },
    'System Administrator': {
        'priority_skills': ['Linux', 'Windows Server', 'Networking', 'Bash', 'Cloud', 'Virtualization', 'Monitoring', 'Security', 'Backup', 'Troubleshooting'],
        'skill_bundles': ['Linux + Bash + Networking', 'Windows Server + Active Directory + DNS', 'Cloud + Virtualization + Monitoring'],
        'courses': ['Linux Administration Bootcamp (Udemy)', 'Windows Server 2022 Administration (Coursera)', 'System Administration and IT Infrastructure (Google/Coursera)', 'Virtualization with VMware (Pluralsight)'],
        'certifications': ['Red Hat Certified Administrator (RHCSA)', 'CompTIA Linux+', 'Microsoft Certified: Windows Server']
    },
    'Security Engineer': {
        'priority_skills': ['Network Security', 'Firewalls', 'Linux', 'Python', 'Penetration Testing', 'Cryptography', 'Incident Response', 'SIEM', 'Cloud Security', 'DevSecOps'],
        'skill_bundles': ['Linux + Python + Penetration Testing', 'Firewalls + Network Security + SIEM', 'Cloud Security + AWS + DevSecOps'],
        'courses': ['Certified Ethical Hacker (CEH) Prep', 'Security Engineering on AWS (Coursera)', 'Python for Security Professionals (Udemy)', 'Introduction to DevSecOps (Linux Academy)'],
        'certifications': ['CEH', 'CISSP', 'GIAC Security Essentials (GSEC)', 'AWS Security Specialty']
    },
    'Machine Learning Engineer': {
        'priority_skills': ['Python', 'Machine Learning', 'TensorFlow', 'PyTorch', 'SQL', 'Data Structures', 'Algorithms', 'Deep Learning', 'MLOps', 'Cloud Computing'],
        'skill_bundles': ['Python + TensorFlow + PyTorch', 'Machine Learning + Deep Learning + Python', 'MLOps + Docker + Cloud'],
        'courses': ['Machine Learning Engineering for Production (MLOps) (Coursera)', 'TensorFlow Developer Certificate Prep (Udemy)', 'Production Machine Learning Systems (Google/edX)', 'MLOps with AWS (Coursera)'],
        'certifications': ['TensorFlow Developer Certificate', 'AWS Certified Machine Learning', 'Databricks ML Certification']
    },
    'AI Engineer': {
        'priority_skills': ['Python', 'Machine Learning', 'Deep Learning', 'NLP', 'Computer Vision', 'TensorFlow', 'PyTorch', 'LLMs', 'Transformers', 'Cloud AI'],
        'skill_bundles': ['Python + TensorFlow + Deep Learning', 'NLP + Transformers + Python', 'Computer Vision + PyTorch + Deep Learning'],
        'courses': ['Deep Learning Specialization (DeepLearning.ai)', 'Natural Language Processing with Transformers (Hugging Face)', 'Computer Vision with PyTorch (Udacity)', 'Generative AI with LLMs (Coursera)'],
        'certifications': ['TensorFlow Developer Certificate', 'NVIDIA Deep Learning Institute Certifications']
    },
    'Site Reliability Engineer (SRE)': {
        'priority_skills': ['Linux', 'AWS', 'Docker', 'Kubernetes', 'Python', 'Go', 'Monitoring', 'Prometheus', 'Grafana', 'CI/CD'],
        'skill_bundles': ['AWS + Docker + Kubernetes', 'Prometheus + Grafana + Monitoring', 'Python + Linux + CI/CD'],
        'courses': ['Site Reliability Engineering (Google/Coursera)', 'SRE and DevOps Fundamentals (Linux Academy)', 'Advanced Kubernetes for SRE (Udemy)', 'Monitoring with Prometheus and Grafana (Pluralsight)'],
        'certifications': ['Google Cloud SRE Certification', 'Certified Kubernetes Administrator (CKA)']
    },
    'Blockchain Developer': {
        'priority_skills': ['Solidity', 'Ethereum', 'Smart Contracts', 'Web3.js', 'Python', 'JavaScript', 'Blockchain', 'Cryptography', 'Truffle', 'Hardhat'],
        'skill_bundles': ['Solidity + Ethereum + Smart Contracts', 'Web3.js + JavaScript + Blockchain', 'Python + Truffle + Hardhat'],
        'courses': ['Blockchain Developer Specialization (Coursera)', 'Ethereum and Solidity Bootcamp (Udemy)', 'Smart Contract Development (ConsenSys Academy)', 'Blockchain Fundamentals (edX)'],
        'certifications': ['Certified Blockchain Developer', 'Ethereum Developer Certification']
    },
    'Game Developer': {
        'priority_skills': ['Unity', 'C#', 'Unreal Engine', 'C++', '3D Modeling', 'Game Physics', 'Animation', 'Shader Programming', 'Multiplayer Networking', 'Game Design'],
        'skill_bundles': ['Unity + C# + Game Physics', 'Unreal Engine + C++ + Animation', '3D Modeling + Unity + C#'],
        'courses': ['Complete Unity Developer Bootcamp (Udemy)', 'Unreal Engine C++ Developer (Udemy)', 'Game Design and Development (Coursera)', 'Multiplayer Game Development (Pluralsight)'],
        'certifications': ['Unity Certified Developer', 'Unreal Engine Certification']
    },
    'Scrum Master': {
        'priority_skills': ['Scrum', 'Agile', 'JIRA', 'Facilitation', 'Conflict Resolution', 'Kanban', 'SAFe', 'Team Coaching', 'Retrospectives', 'Sprint Planning'],
        'skill_bundles': ['Scrum + JIRA + Agile', 'Kanban + SAFe + Agile', 'Scrum + Team Coaching + Retrospectives'],
        'courses': ['Certified ScrumMaster (CSM) Training (Scrum Alliance)', 'Agile with Atlassian JIRA (Coursera)', 'Scrum Master Certification (Udemy)', 'SAFe Scrum Master (Scaled Agile)'],
        'certifications': ['Certified ScrumMaster (CSM)', 'Professional Scrum Master (PSM)', 'SAFe Scrum Master']
    },
    'Technical Project Manager': {
        'priority_skills': ['Project Management', 'Agile', 'JIRA', 'Risk Management', 'Stakeholder Management', 'Budgeting', 'Reporting', 'Waterfall', 'MS Project', 'Communication'],
        'skill_bundles': ['Agile + JIRA + Project Management', 'Risk Management + Stakeholder Management + Budgeting', 'Waterfall + MS Project + Reporting'],
        'courses': ['Project Management Professional (PMP) Prep (PMI)', 'Agile Project Management (Google/Coursera)', 'Technical Project Management (edX)', 'JIRA for Project Management (Atlassian)'],
        'certifications': ['PMP (Project Management Professional)', 'Certified ScrumMaster (CSM)', 'PRINCE2']
    },
    'Big Data Engineer': {
        'priority_skills': ['Hadoop', 'Spark', 'Python', 'Scala', 'Kafka', 'Hive', 'HBase', 'Airflow', 'Big Data', 'AWS EMR'],
        'skill_bundles': ['Hadoop + Spark + Python', 'Kafka + Spark + Big Data', 'AWS EMR + Spark + Hadoop'],
        'courses': ['Big Data Specialization (UC San Diego/Coursera)', 'Apache Spark with Python (Udemy)', 'Kafka for Big Data Engineers (Udemy)', 'Hadoop Certification Prep (Cloudera)'],
        'certifications': ['Cloudera Certified Data Engineer', 'Databricks Certified Engineer', 'AWS Big Data Specialty']
    }
}
# HELPER FUNCTIONS

def show_metric_explanations():
    with st.expander("Understanding Skill Bundles"):
        st.markdown("""
        - **Lift**: Measures connection strength (higher = stronger association)
        - **Confidence**: Reliability of the rule (e.g., 80% = 8 out of 10 jobs follow this pattern)
        - **Focus on high lift values (>2)** for the most meaningful skill combinations
        """)

def create_skill_network_graph(rules_df, top_n=20):
    top_rules = rules_df.nlargest(top_n, 'lift')
    nodes = set()
    edges = []
    
    for idx, row in top_rules.iterrows():
        nodes.add(row['antecedents'])
        nodes.add(row['consequents'])
        edges.append({'source': row['antecedents'], 'target': row['consequents'], 'lift': row['lift']})
    
    node_list = list(nodes)
    n_nodes = len(node_list)
    angles = [2 * math.pi * i / n_nodes for i in range(n_nodes)]
    node_positions = {node: (math.cos(angle), math.sin(angle)) for node, angle in zip(node_list, angles)}
    
    fig = go.Figure()
    
    for edge in edges:
        if edge['source'] in node_positions and edge['target'] in node_positions:
            x0, y0 = node_positions[edge['source']]
            x1, y1 = node_positions[edge['target']]
            fig.add_trace(go.Scatter(
                x=[x0, x1], y=[y0, y1],
                mode='lines',
                line=dict(width=min(edge['lift']/2, 4), color=COLORS['primary-light']),
                hoverinfo='text',
                text=f"{edge['source']} → {edge['target']}<br>Lift: {edge['lift']:.2f}",
                showlegend=False
            ))
    
    fig.add_trace(go.Scatter(
        x=[pos[0] for pos in node_positions.values()],
        y=[pos[1] for pos in node_positions.values()],
        mode='markers+text',
        marker=dict(size=16, color=COLORS['primary'], line=dict(width=1, color='white')),
        text=list(node_positions.keys()),
        textposition='bottom center',
        textfont=dict(size=10),
        hoverinfo='none',
        showlegend=False
    ))
    
    fig.update_layout(
        title=None,
        xaxis=dict(showgrid=False, zeroline=False, visible=False),
        yaxis=dict(showgrid=False, zeroline=False, visible=False),
        height=450,
        hovermode='closest',
        plot_bgcolor='white',
        paper_bgcolor='white',
        margin=dict(l=20, r=20, t=20, b=20)
    )
    return fig

# TECHNICAL SKILL BUNDLES PAGE

def technical_bundles_page():
    st.markdown("### Technical Skill Bundles")
    st.markdown("Skills that employers frequently request together in job postings")
    
    show_metric_explanations()
    tech_df = load_technical_skill_bundles()
    
    col1, col2 = st.columns(2)
    with col1:
        min_lift = st.slider("Minimum Lift", 1.0, 5.0, 1.2, 0.1, help="Higher = stronger connection between skills")
    with col2:
        min_conf = st.slider("Minimum Confidence", 0.2, 1.0, 0.35, 0.05, help="Higher = more reliable rule")
    
    categories = ['All', 'Cloud/DevOps', 'Backend', 'Frontend', 'Database', 'Data Science', 'Mobile', 'General']
    selected_category = st.selectbox("Filter by Category", categories)
    
    filtered_rules = tech_df[(tech_df['lift'] >= min_lift) & (tech_df['confidence'] >= min_conf)]
    
    if selected_category != 'All':
        category_keywords = {
            'Cloud/DevOps': ['AWS', 'Docker', 'Kubernetes', 'Terraform', 'Jenkins', 'Linux', 'Azure', 'GCP', 'Ansible', 'Prometheus'],
            'Backend': ['Python', 'Django', 'Flask', 'Node.js', 'Express', 'Java', 'Spring', 'Go', 'Rust', 'PHP', 'Ruby'],
            'Frontend': ['React', 'Angular', 'Vue', 'JavaScript', 'TypeScript', 'HTML', 'CSS', 'Redux', 'Next.js'],
            'Database': ['SQL', 'PostgreSQL', 'MySQL', 'MongoDB', 'Redis', 'Elasticsearch', 'Cassandra'],
            'Data Science': ['TensorFlow', 'PyTorch', 'Pandas', 'NumPy', 'Machine Learning', 'Spark', 'Kafka'],
            'Mobile': ['Flutter', 'Dart', 'React Native', 'Swift', 'Kotlin', 'Android', 'iOS']
        }
        keywords = category_keywords.get(selected_category, [])
        mask = filtered_rules['antecedents'].str.contains('|'.join(keywords), case=False, na=False) | \
               filtered_rules['consequents'].str.contains('|'.join(keywords), case=False, na=False)
        filtered_rules = filtered_rules[mask]
    
    display_df = filtered_rules[['antecedents', 'consequents', 'lift', 'confidence']].head(50).copy()
    display_df.columns = ['Required Skill', 'Associated Skill', 'Lift', 'Confidence']
    
    def strength_indicator(lift):
        if lift >= 3:
            return "🟢 Very Strong"
        elif lift >= 2:
            return "🟡 Strong"
        else:
            return "🔵 Moderate"
    
    display_df['Connection Strength'] = display_df['Lift'].apply(strength_indicator)
    display_df = display_df[['Required Skill', 'Associated Skill', 'Connection Strength', 'Lift', 'Confidence']]
    
    st.dataframe(display_df, use_container_width=True, hide_index=True)
    
    st.markdown("### Skill Connection Network")
    if len(filtered_rules) > 0:
        fig = create_skill_network_graph(filtered_rules, top_n=20)
        st.plotly_chart(fig, use_container_width=True)
    
    csv = filtered_rules.to_csv(index=False)
    st.download_button("Download Technical Skill Bundles (CSV)", csv, "technical_skill_bundles.csv", "text/csv")

# DESIGN SKILL BUNDLES PAGE

def design_bundles_page():
    st.markdown("### Design & UX Skill Bundles")
    st.markdown("Design and UX skills that employers frequently request together")
    
    show_metric_explanations()
    design_df = load_design_skill_bundles()
    
    col1, col2 = st.columns(2)
    with col1:
        min_lift = st.slider("Minimum Lift", 1.0, 30.0, 2.0, 0.5, help="Design bundles often have very high lift values")
    with col2:
        min_conf = st.slider("Minimum Confidence", 0.3, 1.0, 0.7, 0.05, help="Design skills are typically bundled together")
    
    filtered_rules = design_df[(design_df['lift'] >= min_lift) & (design_df['confidence'] >= min_conf)]
    
    display_df = filtered_rules[['antecedents', 'consequents', 'lift', 'confidence']].head(30).copy()
    display_df.columns = ['Design Skill', 'Associated Skill', 'Lift', 'Confidence']
    
    def strength_indicator(lift):
        if lift >= 10:
            return "🔴 Extremely Strong"
        elif lift >= 5:
            return "🟡 Very Strong"
        else:
            return "🟢 Strong"
    
    display_df['Connection Strength'] = display_df['Lift'].apply(strength_indicator)
    display_df = display_df[['Design Skill', 'Associated Skill', 'Connection Strength', 'Lift', 'Confidence']]
    
    st.dataframe(display_df, use_container_width=True, hide_index=True)
    
    st.markdown("### Design Skill Network")
    if len(filtered_rules) > 0:
        fig = create_skill_network_graph(filtered_rules, top_n=15)
        st.plotly_chart(fig, use_container_width=True)
    
    csv = filtered_rules.to_csv(index=False)
    st.download_button("Download Design Skill Bundles (CSV)", csv, "design_skill_bundles.csv", "text/csv")


# LEARNING RECOMMENDATIONS PAGE 

def recommendations_page():
    st.markdown("### Personalized Learning Recommendations")
    st.markdown("AI-powered recommendations based on market demand in Nigeria's tech sector")
    
    gap_df = load_gap_analysis()
    available_roles = sorted(LEARNING_RECOMMENDATIONS.keys())
    
    col1, col2 = st.columns([1, 2])
    with col1:
        selected_role = st.selectbox("Select Your Target Role", available_roles)
    
    role_rec = LEARNING_RECOMMENDATIONS.get(selected_role, LEARNING_RECOMMENDATIONS['Software Developer'])
    
    demand_data = []
    for skill in role_rec['priority_skills'][:10]:
        if skill in gap_df['skill'].values:
            demand_pct = gap_df[gap_df['skill'] == skill]['demand_percentage'].values[0]
            demand_data.append({'skill': skill, 'demand': demand_pct})
        else:
            demand_data.append({'skill': skill, 'demand': 45})
    
    demand_df = pd.DataFrame(demand_data)
    fig = px.bar(demand_df, x='skill', y='demand', title=f"Market Demand for {selected_role}",
                 color='demand', color_continuous_scale='Greens', labels={'demand': 'Demand (%)'})
    fig.update_layout(height=350, plot_bgcolor='white', margin=dict(l=20, r=20, t=40, b=20))
    st.plotly_chart(fig, use_container_width=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        avg_demand = demand_df['demand'].mean()
        st.metric("Average Market Demand", f"{avg_demand:.0f}%")
    with col2:
        top_skill = demand_df.loc[demand_df['demand'].idxmax(), 'skill']
        st.metric("Most In-Demand Skill", top_skill)
    with col3:
        shortage_count = len([d for d in demand_data if d['skill'] in gap_df[gap_df['gap_score'] > 10]['skill'].values])
        st.metric("Critical Shortage Skills", shortage_count)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("#### 🎯 Priority Skills to Learn")
        for skill in role_rec['priority_skills'][:10]:
            st.markdown(f"• **{skill}**")
        
        st.markdown("#### 🔗 Skill Bundles to Master")
        for bundle in role_rec['skill_bundles']:
            st.markdown(f"• {bundle}")
    
    with col2:
        st.markdown("#### 📚 Recommended Courses")
        for course in role_rec['courses'][:5]:
            st.markdown(f"• {course}")
        
        st.markdown("#### 🏆 Recommended Certifications")
        for cert in role_rec['certifications']:
            st.markdown(f"• {cert}")
    
    with col3:
        st.markdown("#### 📈 Career Progression Timeline")
        st.markdown("""
        - **Months 0-3:** Core Fundamentals
        - **Months 4-6:** Specialization Skills
        - **Months 7-9:** Skill Bundles & Tools
        - **Months 10-12:** Certifications & Portfolio
        """)
        
        st.markdown("#### 💡 Quick Tips")
        st.markdown("""
        - Learn skills in bundles, not isolation
        - Build projects combining multiple skills
        - Get certified to validate knowledge
        - Update your portfolio regularly
        """)
    
    plan_text = f"""
    SKILL SYNC NIGERIA - PERSONALIZED LEARNING PLAN
    ================================================
    Role: {selected_role}
    Date: {datetime.now().strftime('%Y-%m-%d')}
    
    PRIORITY SKILLS TO LEARN:
    {chr(10).join(['- ' + s for s in role_rec['priority_skills']])}
    
    SKILL BUNDLES TO MASTER:
    {chr(10).join(['- ' + b for b in role_rec['skill_bundles']])}
    
    RECOMMENDED COURSES:
    {chr(10).join(['- ' + c for c in role_rec['courses']])}
    
    RECOMMENDED CERTIFICATIONS:
    {chr(10).join(['- ' + c for c in role_rec['certifications']])}
    
    12-MONTH LEARNING TIMELINE:
    Months 0-3: Core Fundamentals
    Months 4-6: Specialization Skills
    Months 7-9: Skill Bundles & Tools
    Months 10-12: Certifications & Portfolio
    """
    st.download_button("📥 Download Learning Plan", plan_text, f"{selected_role.replace(' ', '_')}_learning_plan.txt", "text/plain")

# GAP ANALYSIS PAGE

def gap_analysis_page():
    st.markdown("### Skills Gap Analysis")
    
    gap_df = load_gap_analysis()
    
    col1, col2 = st.columns(2)
    with col1:
        search = st.text_input("Search Skill", placeholder="e.g., Python, AWS...")
    with col2:
        status_filter = st.selectbox("Filter by Status", ["All", "Shortage (Gap > 10%)", "Balanced", "Surplus (Gap < -5%)"])
    
    filtered_df = gap_df.copy()
    if search:
        filtered_df = filtered_df[filtered_df['skill'].str.contains(search, case=False)]
    if status_filter == "Shortage (Gap > 10%)":
        filtered_df = filtered_df[filtered_df['gap_score'] > 10]
    elif status_filter == "Surplus (Gap < -5%)":
        filtered_df = filtered_df[filtered_df['gap_score'] < -5]
    elif status_filter == "Balanced":
        filtered_df = filtered_df[filtered_df['gap_score'].abs() <= 5]
    
    st.dataframe(filtered_df, use_container_width=True, hide_index=True)
    csv = filtered_df.to_csv(index=False)
    st.download_button("Download Gap Analysis (CSV)", csv, "skills_gap_analysis.csv", "text/csv")

# DASHBOARD PAGE 

def dashboard_page():
    st.markdown("### Nigeria Tech Skills Intelligence")
    st.markdown("Data-driven insights for bridging the technology skills gap")
    
    gap_df = load_gap_analysis()
    tech_df = load_technical_skill_bundles()
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        shortage = len(gap_df[gap_df['gap_score'] > 10])
        # Removed the delta "High Priority" label as requested
        st.metric("Critical Shortages", shortage)
    with col2:
        st.metric("Skills Analyzed", len(gap_df))
    with col3:
        st.metric("Skill Bundles", len(tech_df))
    with col4:
        st.metric("Roles Covered", len(LEARNING_RECOMMENDATIONS))
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Top Skills in Shortage")
        shortage_df = gap_df.nlargest(10, 'gap_score')
        fig = px.bar(shortage_df, x='gap_score', y='skill', orientation='h',
                     color='gap_score', color_continuous_scale='Reds',
                     labels={'gap_score': 'Gap (%)', 'skill': ''})
        fig.update_layout(height=350, plot_bgcolor='white', margin=dict(l=0, r=0, t=20, b=0))
        fig.update_traces(marker=dict(color=COLORS['danger'], line=dict(width=0)))
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("#### Top Skills in Surplus")
        surplus_df = gap_df.nsmallest(10, 'gap_score')
        fig = px.bar(surplus_df, x='gap_score', y='skill', orientation='h',
                     color='gap_score', color_continuous_scale='Greens',
                     labels={'gap_score': 'Gap (%)', 'skill': ''})
        fig.update_layout(height=350, plot_bgcolor='white', margin=dict(l=0, r=0, t=20, b=0))
        fig.update_traces(marker=dict(color=COLORS['primary-light'], line=dict(width=0)))
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("#### Demand vs Supply Distribution")
    
    if 'demand_percentage' in gap_df.columns:
        scatter_df = gap_df.copy()
        scatter_df['abs_gap'] = scatter_df['gap_score'].abs()
        scatter_df['size'] = scatter_df['abs_gap'] + 1
        
        fig = px.scatter(scatter_df, x='demand_percentage', y='supply_percentage',
                         size='size', color='gap_score', hover_name='skill', text='skill',
                         color_continuous_scale='RdYlGn', size_max=20,
                         labels={'demand_percentage': 'Demand (%)', 'supply_percentage': 'Supply (%)'})
        fig.add_shape(type="line", x0=0, y0=0, x1=100, y1=100, line=dict(color=COLORS['gray'], dash="dash", width=1))
        fig.update_layout(height=450, plot_bgcolor='white', margin=dict(l=20, r=20, t=20, b=20))
        st.plotly_chart(fig, use_container_width=True, config={'scrollZoom': True})
# DATA EXPLORER PAGE

def data_page():
    st.markdown("### Data Explorer")
    
    tab1, tab2, tab3 = st.tabs(["Skills Gap Data", "Technical Skill Bundles", "Design Skill Bundles"])
    
    with tab1:
        gap_df = load_gap_analysis()
        st.dataframe(gap_df, use_container_width=True)
        st.download_button("Download CSV", gap_df.to_csv(index=False), "skills_gap.csv", "text/csv")
    
    with tab2:
        tech_df = load_technical_skill_bundles()
        st.dataframe(tech_df, use_container_width=True)
        st.download_button("Download CSV", tech_df.to_csv(index=False), "technical_bundles.csv", "text/csv")
    
    with tab3:
        design_df = load_design_skill_bundles()
        st.dataframe(design_df, use_container_width=True)
        st.download_button("Download CSV", design_df.to_csv(index=False), "design_bundles.csv", "text/csv")
# PROFILE PAGE
def profile_page():
    st.markdown("### My Profile")
    
    username = st.session_state.username
    profile = get_user_profile(username)
    
    with open(USER_DB_FILE, 'r') as f:
        users = json.load(f)
    user_data = users.get(username, {})
    
    tab1, tab2, tab3 = st.tabs(["Information", "Security", "Activity"])
    
    with tab1:
        col1, col2 = st.columns([1, 2])
        with col1:
            st.markdown(f'<div class="profile-avatar">{profile.get("avatar", "👤")}</div>', unsafe_allow_html=True)
            avatars = ['👤', '👨‍💻', '👩‍💻', '🧑‍💻', '👨‍🎓', '👩‍🎓', '🌟', '🎯']
            selected = st.selectbox("Avatar", avatars, index=avatars.index(profile.get('avatar', '👤')) if profile.get('avatar', '👤') in avatars else 0)
            if selected != profile.get('avatar', '👤'):
                profile['avatar'] = selected
                update_user_profile(username, profile)
                st.rerun()
        
        with col2:
            st.markdown('<div class="profile-card">', unsafe_allow_html=True)
            full_name = st.text_input("Full Name", value=profile.get('full_name', user_data.get('full_name', '')))
            email = st.text_input("Email", value=profile.get('email', user_data.get('email', '')))
            bio = st.text_area("Bio", value=profile.get('bio', ''), height=80, placeholder="Tell us about your tech journey...")
            if st.button("Save Changes"):
                profile['full_name'] = full_name
                profile['email'] = email
                profile['bio'] = bio
                update_user_profile(username, profile)
                st.success("Profile updated")
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
    
    with tab2:
        st.markdown('<div class="profile-card">', unsafe_allow_html=True)
        with st.form("password_form"):
            old = st.text_input("Current Password", type="password")
            new = st.text_input("New Password", type="password")
            confirm = st.text_input("Confirm New Password", type="password")
            if st.form_submit_button("Change Password"):
                if new != confirm:
                    st.error("Passwords do not match")
                elif len(new) < 6:
                    st.error("Password must be at least 6 characters")
                else:
                    success, msg = change_password(username, old, new)
                    if success:
                        st.success(msg)
                    else:
                        st.error(msg)
        
        st.markdown("---")
        prefs = profile.get('notification_preferences', {'email_updates': True, 'market_alerts': True, 'newsletter': False})
        email_up = st.checkbox("Email Updates", value=prefs.get('email_updates', True))
        market_al = st.checkbox("Market Alerts", value=prefs.get('market_alerts', True))
        newsletter = st.checkbox("Newsletter", value=prefs.get('newsletter', False))
        if st.button("Save Preferences"):
            profile['notification_preferences'] = {'email_updates': email_up, 'market_alerts': market_al, 'newsletter': newsletter}
            update_user_profile(username, profile)
            st.success("Preferences saved")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with tab3:
        st.markdown('<div class="profile-card">', unsafe_allow_html=True)
        st.markdown("**Recent Activity**")
        activities = [
            {"date": datetime.now().strftime("%Y-%m-%d"), "action": "Logged into Skill Sync Nigeria"},
            {"date": datetime.now().strftime("%Y-%m-%d"), "action": "Viewed skills gap analysis"},
            {"date": datetime.now().strftime("%Y-%m-%d"), "action": "Explored skill bundles"}
        ]
        for act in activities:
            st.markdown(f'<div class="activity-item"><strong>{act["date"]}</strong><br>{act["action"]}</div>', unsafe_allow_html=True)
        
        st.markdown("---")
        st.markdown("**Account Statistics**")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Login Streak", "3 days")
        with col2:
            st.metric("Recommendations", "12")
        st.markdown('</div>', unsafe_allow_html=True)
    # LOGOUT BUTTON 
    st.markdown("---")
    if st.button("🚪 Logout", use_container_width=True):
        logout()
# LOGIN PAGE
def login_page():
    st.markdown(f"""
    <style>
    .login-wrapper {{
        display: flex;
        justify-content: center;
        align-items: center;
        min-height: 80vh;
        padding: 20px;
    }}
    .login-card {{
        background: white;
        border-radius: 20px;
        padding: 32px;
        max-width: 450px;
        width: 100%;
        box-shadow: {COLORS['shadow']};
        text-align: center;
    }}
    .login-logo {{
        width: 70px;
        height: 70px;
        background: {COLORS['gradient-soft']};
        border-radius: 18px;
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 0 auto 16px auto;
        font-size: 2em;
    }}
    .login-title {{
        font-size: 1.5em;
        font-weight: 600;
        margin-bottom: 8px;
        color: {COLORS['primary']};
    }}
    .login-subtitle {{
        color: {COLORS['gray']};
        margin-bottom: 24px;
        font-size: 0.85em;
    }}
    </style>
    
    <div class="login-wrapper">
        <div class="login-card">
            <div class="login-logo">🎯</div>
            <div class="login-title">Skill Sync Nigeria</div>
            <div class="login-subtitle">Tech Skills Intelligence Platform</div>
    """, unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["Sign In", "Create Account"])
    
    with tab1:
        with st.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            if st.form_submit_button("Sign In", use_container_width=True):
                if verify_user(username, password):
                    st.session_state.logged_in = True
                    st.session_state.username = username
                    st.rerun()
                else:
                    st.error("Invalid username or password")
    
    with tab2:
        with st.form("register_form"):
            full_name = st.text_input("Full Name")
            new_user = st.text_input("Username")
            email = st.text_input("Email")
            new_pass = st.text_input("Password", type="password")
            confirm_pass = st.text_input("Confirm Password", type="password")
            if st.form_submit_button("Create Account", use_container_width=True):
                if new_pass != confirm_pass:
                    st.error("Passwords do not match")
                elif len(new_pass) < 6:
                    st.error("Password must be at least 6 characters")
                elif not new_user or not email:
                    st.error("Please fill all fields")
                else:
                    success, msg = register_user(new_user, new_pass, email, full_name)
                    if success:
                        st.success(msg)
                    else:
                        st.error(msg)
    
    st.markdown("</div></div>", unsafe_allow_html=True)


#  DASHBOARD


def main_dashboard():
    show_skillsync_header()
    
    st.markdown('<div class="top-nav">', unsafe_allow_html=True)
    show_top_navigation()
    st.markdown('</div>', unsafe_allow_html=True)
    
    page = st.session_state.page
    
    if page == "Dashboard":
        dashboard_page()
    elif page == "Gap Analysis":
        gap_analysis_page()
    elif page == "Technical Bundles":
        technical_bundles_page()
    elif page == "Design Bundles":
        design_bundles_page()
    elif page == "Recommendations":
        recommendations_page()
    elif page == "Data":
        data_page()
    elif page == "Profile":
        profile_page()
    
    st.markdown(f"""
    <div class="footer">
        <p>Skill Sync Nigeria © 2024 | Tech Skills Intelligence | Bridging the Demand-Supply Divide</p>
    </div>
    """, unsafe_allow_html=True)
# APP


def main():
    if st.session_state.logged_in:
        main_dashboard()
    else:
        login_page()

if __name__ == "__main__":
    main()
