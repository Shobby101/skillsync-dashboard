"""
2000 Job Postings Generator for Nigerian Tech Skills Gap Project
Demand Dataset with Extracted Skills
"""

import pandas as pd
import random
import os
from datetime import datetime

# ============================================================
# SAFE FILE SAVING FUNCTION
# ============================================================

def safe_save_dataframe(df, filename):
    """Safely save DataFrame with permission error handling"""
    try:
        if os.path.exists(filename):
            try:
                with open(filename, 'a') as f:
                    pass
            except PermissionError:
                print(f"  ⚠️ Cannot overwrite {filename} - file may be open")
                alt_filename = filename.replace('.csv', f'_{datetime.now().strftime("%H%M%S")}.csv')
                df.to_csv(alt_filename, index=False)
                print(f"  → Saved as: {alt_filename}")
                return alt_filename
        df.to_csv(filename, index=False)
        print(f"  ✓ Saved: {filename}")
        return filename
    except Exception as e:
        print(f"  ✗ Error saving {filename}: {e}")
        alt_name = f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{filename}"
        df.to_csv(alt_name, index=False)
        print(f"  → Saved as: {alt_name}")
        return alt_name


# ============================================================
# 2000 JOB POSTINGS GENERATOR
# ============================================================

class DemandDataGenerator:
    """Generates 2000 tech job postings for demand dataset"""
    
    def __init__(self):
        self.jobs = []
    
    def generate_2000_jobs(self):
        """Generate 2000 job postings with realistic Nigerian tech market data"""
        
        print("\n" + "=" * 70)
        print("GENERATING 2000 TECH JOB POSTINGS FOR DEMAND DATASET")
        print("=" * 70)
        
        # ============================================================
        # 1. JOB TITLES (60 unique titles)
        # ============================================================
        job_titles = {
            'Software Developer': ['Python Developer', 'Java Developer', 'JavaScript Developer', 'C# Developer', 
                                   'Ruby Developer', 'Go Developer', 'PHP Developer', 'Rust Developer',
                                   'Software Engineer', 'Software Developer', 'Application Developer'],
            'Frontend Developer': ['React Developer', 'Angular Developer', 'Vue.js Developer', 'Frontend Engineer',
                                   'UI Developer', 'Web Developer', 'Frontend UI Developer', 'Next.js Developer'],
            'Backend Developer': ['Node.js Developer', 'Django Developer', 'Flask Developer', 'Spring Boot Developer',
                                  'Laravel Developer', 'ASP.NET Developer', 'Backend Engineer', 'API Developer'],
            'Full Stack Developer': ['Full Stack Engineer', 'Full Stack Developer', 'MEAN Stack Developer',
                                     'MERN Stack Developer', 'Full Stack Web Developer'],
            'Data Scientist': ['Data Scientist', 'Machine Learning Engineer', 'AI Engineer', 'Deep Learning Engineer',
                               'NLP Engineer', 'Computer Vision Engineer'],
            'Data Analyst': ['Data Analyst', 'Business Intelligence Analyst', 'Analytics Engineer', 
                             'Marketing Data Analyst', 'Product Data Analyst'],
            'Data Engineer': ['Data Engineer', 'Big Data Engineer', 'ETL Developer', 'Data Pipeline Engineer'],
            'DevOps Engineer': ['DevOps Engineer', 'Site Reliability Engineer', 'Platform Engineer', 
                                'Build Engineer', 'Infrastructure Engineer'],
            'Cloud Engineer': ['Cloud Engineer', 'AWS Engineer', 'Azure Engineer', 'Google Cloud Engineer',
                               'Cloud Architect', 'Cloud Solutions Architect'],
            'Cybersecurity': ['Cybersecurity Analyst', 'Security Engineer', 'Information Security Analyst',
                              'Penetration Tester', 'Security Operations Analyst', 'GRC Analyst'],
            'Product Manager': ['Product Manager', 'Technical Product Manager', 'Product Owner', 
                                'Associate Product Manager', 'Senior Product Manager'],
            'UI/UX Designer': ['UI Designer', 'UX Designer', 'Product Designer', 'UI/UX Designer',
                               'Interaction Designer', 'Visual Designer'],
            'Mobile Developer': ['Android Developer', 'iOS Developer', 'Flutter Developer', 'React Native Developer',
                                 'Mobile Engineer', 'Cross-Platform Developer'],
            'QA Engineer': ['QA Engineer', 'Test Automation Engineer', 'Software Tester', 'Quality Assurance Analyst',
                            'SDET'],
            'Database Admin': ['Database Administrator', 'DBA', 'Database Engineer', 'SQL Developer'],
            'Network Engineer': ['Network Engineer', 'Network Administrator', 'Network Architect', 'Network Security Engineer'],
            'System Admin': ['System Administrator', 'Systems Engineer', 'IT Administrator', 'Infrastructure Engineer'],
            'Technical Writer': ['Technical Writer', 'Documentation Specialist', 'Content Developer'],
            'Scrum Master': ['Scrum Master', 'Agile Coach', 'Agile Project Manager'],
            'Project Manager': ['Technical Project Manager', 'IT Project Manager', 'Delivery Manager']
        }
        
        # ============================================================
        # 2. COMPANIES IN NIGERIA (50+ real companies)
        # ============================================================
        companies = [
            # Nigerian Tech Companies
            "Flutterwave", "Paystack", "Andela", "Interswitch", "Paga", "Kuda Bank",
            "Chipper Cash", "Bamboo", "Cowrywise", "TalentQL", "Decagon", "AltSchool Africa",
            "Semicolon", "Moni", "Kippa", "Termii", "TeamApt", "Carbon", "Rensource",
            "Kobo360", "MTN Nigeria", "Airtel Nigeria", "MainOne", "IHS Towers",
            "Sterling Bank", "GTBank", "Access Bank", "UBA", "First Bank",
            # International with Nigerian presence
            "Google Nigeria", "Microsoft Nigeria", "Amazon Web Services", "IBM Nigeria",
            "Oracle Nigeria", "Cisco Nigeria", "Deloitte Nigeria", "PwC Nigeria",
            "KPMG Nigeria", "EY Nigeria", "Andela", "Cellulant", "Paga", "Flutterwave",
            # Tech Hubs & Startups
            "CCHub", "Ventures Platform", "Future Africa", "Microtraction", "Launch Africa",
            "Techstars Lagos", "Ingressive Capital", "ARM Labs", "Nest Innovation", "Co-Creation Hub"
        ]
        
        # ============================================================
        # 3. LOCATIONS IN NIGERIA
        # ============================================================
        locations = [
            'Lagos, Nigeria', 'Abuja, Nigeria', 'Port Harcourt, Nigeria', 
            'Ibadan, Nigeria', 'Kano, Nigeria', 'Enugu, Nigeria',
            'Remote (Nigeria)', 'Hybrid - Lagos', 'Hybrid - Abuja'
        ]
        location_weights = [0.45, 0.12, 0.08, 0.08, 0.04, 0.03, 0.12, 0.05, 0.03]
        
        # ============================================================
        # 4. SKILLS FOR EACH JOB CATEGORY
        # ============================================================
        job_skills_map = {
            'Software Developer': ['Python', 'Java', 'JavaScript', 'Git', 'SQL', 'Data Structures', 'Algorithms', 
                                   'Object-Oriented Programming', 'REST APIs', 'Linux', 'Debugging', 'Unit Testing'],
            'Frontend Developer': ['JavaScript', 'React', 'HTML5', 'CSS3', 'TypeScript', 'Git', 'Redux', 
                                   'Responsive Design', 'Tailwind CSS', 'Webpack', 'REST APIs', 'Figma'],
            'Backend Developer': ['Python', 'Node.js', 'SQL', 'REST APIs', 'Git', 'Django', 'PostgreSQL', 
                                  'Docker', 'Linux', 'MongoDB', 'Redis', 'API Design'],
            'Full Stack Developer': ['JavaScript', 'Python', 'React', 'Node.js', 'SQL', 'Git', 'HTML/CSS', 
                                     'MongoDB', 'Docker', 'REST APIs', 'TypeScript', 'Express.js'],
            'Data Scientist': ['Python', 'SQL', 'Machine Learning', 'Pandas', 'NumPy', 'Statistics', 
                               'Data Visualization', 'Scikit-learn', 'TensorFlow', 'Deep Learning', 'Tableau'],
            'Data Analyst': ['SQL', 'Excel', 'Python', 'Tableau', 'Power BI', 'Data Visualization', 
                             'Statistics', 'Data Cleaning', 'Business Intelligence', 'Looker'],
            'Data Engineer': ['Python', 'SQL', 'AWS', 'Spark', 'Airflow', 'ETL', 'Big Data', 
                              'Data Warehousing', 'Kafka', 'Hadoop', 'Scala'],
            'DevOps Engineer': ['AWS', 'Docker', 'Kubernetes', 'Jenkins', 'Terraform', 'Linux', 'CI/CD', 
                                'Python', 'Bash', 'Git', 'Prometheus', 'Grafana', 'Ansible'],
            'Cloud Engineer': ['AWS', 'Azure', 'Docker', 'Kubernetes', 'Terraform', 'Linux', 'Python', 
                               'Networking', 'CI/CD', 'Serverless', 'CloudFormation'],
            'Cybersecurity': ['Network Security', 'SIEM', 'Firewalls', 'Incident Response', 'Linux', 
                              'Python', 'Risk Assessment', 'Penetration Testing', 'Cryptography', 'Compliance'],
            'Product Manager': ['Agile', 'Scrum', 'Product Strategy', 'User Research', 'Data Analysis', 
                                'JIRA', 'Roadmapping', 'Stakeholder Management', 'Market Research', 'MVP'],
            'UI/UX Designer': ['Figma', 'User Research', 'Wireframing', 'Prototyping', 'Visual Design', 
                               'Adobe XD', 'Usability Testing', 'Design Systems', 'Information Architecture'],
            'Mobile Developer': ['Flutter', 'Dart', 'Kotlin', 'Swift', 'React Native', 'Firebase', 
                                 'REST APIs', 'Git', 'Mobile UI', 'App Store Deployment', 'Android', 'iOS'],
            'QA Engineer': ['Test Automation', 'Selenium', 'Manual Testing', 'JIRA', 'API Testing', 
                            'Python', 'Regression Testing', 'Test Planning', 'CI/CD', 'Postman'],
            'Database Admin': ['SQL', 'PostgreSQL', 'MySQL', 'Database Design', 'Performance Tuning', 
                               'Backup Recovery', 'Query Optimization', 'MongoDB', 'High Availability'],
            'Network Engineer': ['TCP/IP', 'Routing', 'Switching', 'Firewalls', 'Cisco', 'VPN', 
                                 'Network Security', 'BGP', 'OSPF', 'Wireshark', 'Load Balancing'],
            'System Admin': ['Linux', 'Windows Server', 'Networking', 'Bash', 'Cloud', 'Virtualization', 
                             'Monitoring', 'Security', 'Backup', 'Troubleshooting'],
            'Technical Writer': ['Technical Writing', 'Documentation', 'Markdown', 'Git', 'API Documentation', 
                                 'MadCap Flare', 'Confluence', 'Communication', 'Research'],
            'Scrum Master': ['Scrum', 'Agile', 'JIRA', 'Confluence', 'Facilitation', 'Conflict Resolution',
                             'Kanban', 'SAFe', 'Team Coaching', 'Retrospectives'],
            'Project Manager': ['Project Management', 'Agile', 'Waterfall', 'JIRA', 'Risk Management', 
                                'Budgeting', 'Stakeholder Management', 'MS Project', 'Communication']
        }
        
        # ============================================================
        # 5. GENERATE 2000 JOBS
        # ============================================================
        
        # Flatten job titles with their categories
        all_job_entries = []
        for category, titles in job_titles.items():
            for title in titles:
                all_job_entries.append({
                    'category': category,
                    'title': title
                })
        
        # Weight distribution by category (realistic for Nigerian market)
        category_weights = {
            'Software Developer': 0.18,
            'Frontend Developer': 0.10,
            'Backend Developer': 0.12,
            'Full Stack Developer': 0.12,
            'Data Scientist': 0.05,
            'Data Analyst': 0.07,
            'Data Engineer': 0.04,
            'DevOps Engineer': 0.05,
            'Cloud Engineer': 0.04,
            'Cybersecurity': 0.03,
            'Product Manager': 0.05,
            'UI/UX Designer': 0.04,
            'Mobile Developer': 0.04,
            'QA Engineer': 0.02,
            'Database Admin': 0.01,
            'Network Engineer': 0.01,
            'System Admin': 0.01,
            'Technical Writer': 0.01,
            'Scrum Master': 0.01,
            'Project Manager': 0.00
        }
        
        # Create list of categories with weights
        weighted_categories = []
        for cat, weight in category_weights.items():
            weighted_categories.extend([cat] * int(weight * 2000))
        
        print("\n📊 Generating 2000 job postings...")
        print("-" * 50)
        
        for i in range(2000):
            # Select category based on weights
            if weighted_categories:
                category = random.choice(weighted_categories)
            else:
                category = random.choice(list(job_titles.keys()))
            
            # Select a specific job title from that category
            job_title = random.choice(job_titles.get(category, ['Software Developer']))
            
            # Select company
            company = random.choice(companies)
            
            # Select location
            location = random.choices(locations, weights=location_weights, k=1)[0]
            
            # Get skills for this category
            skills = job_skills_map.get(category, job_skills_map['Software Developer'])
            
            # Select 6-12 random skills for this job
            num_skills = random.randint(6, 12)
            selected_skills = random.sample(skills, min(num_skills, len(skills)))
            
            # Add soft skills to every job
            soft_skills = ['Communication', 'Teamwork', 'Problem Solving']
            for ss in random.sample(soft_skills, 2):
                if ss not in selected_skills:
                    selected_skills.append(ss)
            
            # Generate salary range (in Naira)
            salary_ranges = [
                '₦3,000,000 - ₦5,000,000 per year',
                '₦5,000,000 - ₦8,000,000 per year',
                '₦8,000,000 - ₦12,000,000 per year',
                '₦12,000,000 - ₦18,000,000 per year',
                'Competitive salary based on experience'
            ]
            
            # Generate years of experience required
            exp_required = random.choice(['0-2 years', '3-5 years', '5+ years', '1-3 years', '2-4 years'])
            
            # Generate job description
            description = generate_job_description(job_title, company, selected_skills, exp_required, salary_ranges)
            
            # Create job posting
            self.jobs.append({
                'job_id': f'JOB_{i+1:04d}',
                'job_title': job_title,
                'category': category,
                'company': company,
                'location': location,
                'experience_required': exp_required,
                'salary_range': random.choice(salary_ranges),
                'description': description,
                'required_skills': selected_skills,
                'skill_count': len(selected_skills),
                'source': 'Generated Dataset',
                'date_collected': datetime.now().strftime('%Y-%m-%d')
            })
            
            # Progress indicator
            if (i + 1) % 500 == 0:
                print(f"  Generated {i+1}/2000 job postings...")
        
        print(f"\n  ✓ Total job postings generated: {len(self.jobs)}")
        return True


def generate_job_description(job_title, company, skills, exp_required, salary_range):
    """Generate a realistic job description"""
    
    skill_text = ', '.join(skills[:5])
    if len(skills) > 5:
        skill_text += f' and {len(skills) - 5} other technical skills'
    
    templates = [
        f"""
        {company} is seeking an experienced {job_title} to join our growing technology team in Lagos, Nigeria.
        
        Requirements:
        • Strong proficiency in {skill_text}
        • {exp_required} of relevant experience
        • Bachelor's degree in Computer Science, Engineering, or related field
        • Strong problem-solving and analytical skills
        • Excellent communication and collaboration abilities
        
        Responsibilities:
        • Design, develop, and maintain high-quality software solutions
        • Collaborate with cross-functional teams to deliver projects on time
        • Participate in code reviews and technical discussions
        • Mentor junior developers and contribute to team growth
        • Stay current with emerging technologies and best practices
        
        Benefits:
        • {random.choice(salary_range.split(' - ')[0] if ' - ' in salary_range else salary_range)}
        • Health insurance and wellness benefits
        • Flexible work arrangements
        • Professional development budget
        • Annual team retreats and events
        """,
        
        f"""
        Job Title: {job_title}
        Location: Lagos, Nigeria (Hybrid)
        Company: {company}
        
        About the Role:
        We are looking for a talented {job_title} to help us build innovative products for the African market.
        
        Required Skills:
        • {skill_text}
        
        Experience Required: {exp_required}
        
        What You'll Do:
        • Build scalable and reliable software solutions
        • Work with product managers and designers to define requirements
        • Write clean, maintainable, and well-documented code
        • Troubleshoot and debug production issues
        
        What We Offer:
        • {salary_range}
        • Health insurance
        • Learning and development opportunities
        • Modern office with great amenities
        """
    ]
    
    return random.choice(templates).strip()


# ============================================================
# SKILL EXTRACTION FUNCTION (for comparison with supply)
# ============================================================

def extract_skills_for_demand_analysis(df):
    """Extract and format skills for demand analysis"""
    
    # Create expanded format (one skill per row)
    expanded_rows = []
    for idx, row in df.iterrows():
        for skill in row['required_skills']:
            expanded_rows.append({
                'job_id': row['job_id'],
                'job_title': row['job_title'],
                'category': row['category'],
                'company': row['company'],
                'location': row['location'],
                'experience_required': row['experience_required'],
                'required_skill': skill
            })
    
    expanded_df = pd.DataFrame(expanded_rows)
    return expanded_df


# ============================================================
# MAIN EXECUTION
# ============================================================

def main():
    """Main function to generate 2000 job postings"""
    
    print("=" * 70)
    print("DEMAND DATASET GENERATOR - 2000 TECH JOB POSTINGS")
    print("For Nigerian Tech Skills Gap Project")
    print("=" * 70)
    
    # Create generator
    generator = DemandDataGenerator()
    
    # Generate 2000 jobs
    generator.generate_2000_jobs()
    
    # Convert to DataFrame
    demand_df = pd.DataFrame(generator.jobs)
    
    # Create expanded format (one skill per row)
    demand_expanded = extract_skills_for_demand_analysis(demand_df)
    
    # Save files
    safe_save_dataframe(demand_df, 'demand_dataset_2000_jobs.csv')
    safe_save_dataframe(demand_expanded, 'demand_dataset_2000_jobs_expanded.csv')
    
    # ============================================================
    # SUMMARY REPORT
    # ============================================================
    print("\n" + "=" * 70)
    print("DEMAND DATASET SUMMARY - 2000 JOB POSTINGS")
    print("=" * 70)
    
    print(f"\n📊 TOTAL JOBS: {len(demand_df)}")
    print(f"\n📈 DISTRIBUTION BY CATEGORY:")
    category_counts = demand_df['category'].value_counts()
    for cat, count in category_counts.items():
        print(f"   {cat}: {count} jobs ({count/len(demand_df)*100:.1f}%)")
    
    print(f"\n💼 TOP COMPANIES HIRING:")
    top_companies = demand_df['company'].value_counts().head(10)
    for company, count in top_companies.items():
        print(f"   {company}: {count} jobs")
    
    print(f"\n📍 LOCATION DISTRIBUTION:")
    location_counts = demand_df['location'].value_counts()
    for loc, count in location_counts.items():
        print(f"   {loc}: {count} jobs ({count/len(demand_df)*100:.1f}%)")
    
    print(f"\n🛠️ SKILL STATISTICS:")
    print(f"   Total unique skills in demand dataset: {demand_expanded['required_skill'].nunique()}")
    print(f"   Average skills per job: {demand_df['skill_count'].mean():.1f}")
    
    print(f"\n🎯 TOP 20 MOST IN-DEMAND SKILLS:")
    top_skills = demand_expanded['required_skill'].value_counts().head(20)
    for skill, count in top_skills.items():
        percentage = (count / len(demand_df)) * 100
        print(f"   {skill}: {count} jobs ({percentage:.1f}%)")
    
    print(f"\n📁 FILES CREATED:")
    print(f"   1. demand_dataset_2000_jobs.csv (full dataset)")
    print(f"   2. demand_dataset_2000_jobs_expanded.csv (one skill per row)")
    
    print("\n" + "=" * 70)
    print("✅ DEMAND DATASET GENERATION COMPLETE!")
    print("   You can now compare with supply dataset for gap analysis.")
    print("=" * 70)
    
    return demand_df, demand_expanded


# ============================================================
# RUN THE GENERATOR
# ============================================================

if __name__ == "__main__":
    # Change to script directory if needed
    script_dir = os.path.dirname(os.path.abspath(__file__))
    if script_dir:
        os.chdir(script_dir)
        print(f"Working directory: {os.getcwd()}")
    
    # Generate the 2000 job postings
    demand_df, demand_expanded = main()
    
    # Preview first few rows
    print("\n\n📋 PREVIEW - FIRST 5 JOB POSTINGS:")
    print(demand_df[['job_id', 'job_title', 'category', 'company', 'location', 'skill_count']].head())