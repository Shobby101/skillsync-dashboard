"""
Data Processing and Normalization for Skills Gap Analysis
Handles both Demand (jobs) and Supply (resumes) datasets
NO QUANTITATIVE GAP ANALYSIS - Only Processing & Normalization
"""

import pandas as pd
import numpy as np
import re
import os
from datetime import datetime

# ============================================================
# PART 1: SKILL NORMALIZATION DICTIONARY
# ============================================================

class SkillNormalizer:
    """
    Normalizes skill names to standard format for accurate comparison
    between demand and supply datasets
    """
    
    # Mapping of variations to standard skill names
    SKILL_NORMALIZATION_MAP = {
        # Python
        'python': 'Python', 'python3': 'Python', 'py': 'Python',
        'python programming': 'Python', 'python developer': 'Python',
        
        # JavaScript
        'javascript': 'JavaScript', 'js': 'JavaScript', 'javascipt': 'JavaScript',
        'javascripts': 'JavaScript', 'es6': 'JavaScript', 'ecmascript': 'JavaScript',
        
        # Java
        'java': 'Java', 'java8': 'Java', 'java 11': 'Java', 'core java': 'Java',
        'advanced java': 'Java', 'j2ee': 'Java', 'spring': 'Java',
        
        # React
        'react': 'React', 'react.js': 'React', 'reactjs': 'React', 'react js': 'React',
        'react native': 'React Native', 'reactnative': 'React Native',
        
        # Node.js
        'node': 'Node.js', 'nodejs': 'Node.js', 'node.js': 'Node.js', 'express': 'Node.js',
        'express.js': 'Node.js', 'nestjs': 'Node.js',
        
        # SQL
        'sql': 'SQL', 'mysql': 'SQL', 'postgresql': 'SQL', 'postgres': 'SQL',
        'sql server': 'SQL', 'mariadb': 'SQL', 'oracle sql': 'SQL',
        
        # AWS
        'aws': 'AWS', 'amazon web services': 'AWS', 'ec2': 'AWS', 's3': 'AWS',
        'lambda': 'AWS', 'cloudfront': 'AWS', 'route53': 'AWS',
        
        # Docker
        'docker': 'Docker', 'dockerfile': 'Docker', 'docker compose': 'Docker',
        'container': 'Docker', 'containerization': 'Docker',
        
        # Git
        'git': 'Git', 'github': 'Git', 'gitlab': 'Git', 'bitbucket': 'Git',
        'version control': 'Git',
        
        # HTML/CSS
        'html': 'HTML/CSS', 'html5': 'HTML/CSS', 'css': 'HTML/CSS', 'css3': 'HTML/CSS',
        'sass': 'HTML/CSS', 'scss': 'HTML/CSS', 'tailwind': 'HTML/CSS',
        
        # Machine Learning
        'machine learning': 'Machine Learning', 'ml': 'Machine Learning',
        'ai': 'Machine Learning', 'artificial intelligence': 'Machine Learning',
        
        # Data Science
        'data science': 'Data Science', 'data analytics': 'Data Science',
        'data analysis': 'Data Science', 'analytics': 'Data Science',
        
        # Soft Skills
        'communication': 'Communication', 'communications': 'Communication',
        'teamwork': 'Teamwork', 'team player': 'Teamwork', 'collaboration': 'Teamwork',
        'problem solving': 'Problem Solving', 'analytical': 'Problem Solving',
        'leadership': 'Leadership', 'leading': 'Leadership',
        'time management': 'Time Management', 'organized': 'Time Management',
        
        # Additional Skills
        'c++': 'C++', 'cpp': 'C++', 'c plus plus': 'C++',
        'c#': 'C#', 'csharp': 'C#', 'dotnet': 'C#',
        'typescript': 'TypeScript', 'ts': 'TypeScript',
        'angular': 'Angular', 'angularjs': 'Angular',
        'vue': 'Vue.js', 'vuejs': 'Vue.js',
        'django': 'Django', 'flask': 'Flask', 'fastapi': 'FastAPI',
        'mongodb': 'MongoDB', 'mongo': 'MongoDB',
        'postgresql': 'PostgreSQL', 'postgres': 'PostgreSQL',
        'redis': 'Redis', 'elasticsearch': 'Elasticsearch',
        'kubernetes': 'Kubernetes', 'k8s': 'Kubernetes',
        'terraform': 'Terraform', 'jenkins': 'Jenkins',
        'azure': 'Azure', 'gcp': 'Google Cloud', 'google cloud': 'Google Cloud',
        'pandas': 'Pandas', 'numpy': 'NumPy', 'tensorflow': 'TensorFlow',
        'pytorch': 'PyTorch', 'scikit-learn': 'Scikit-learn',
        'tableau': 'Tableau', 'power bi': 'Power BI', 'powerbi': 'Power BI'
    }
    
    # Stop words to remove from skill names
    STOP_WORDS = {'skills', 'proficient', 'experience', 'knowledge', 'familiarity',
                  'ability', 'expertise', 'understanding', 'working', 'using', 'with'}
    
    @classmethod
    def normalize_skill(cls, skill):
        """
        Convert a skill to its standard form
        
        Args:
            skill: Raw skill string
            
        Returns:
            Normalized skill name
        """
        if not skill or not isinstance(skill, str):
            return None
        
        # Convert to lowercase for matching
        skill_lower = skill.lower().strip()
        
        # Remove common stop words
        for stop_word in cls.STOP_WORDS:
            skill_lower = skill_lower.replace(stop_word, '')
        
        # Remove extra spaces and punctuation
        skill_lower = re.sub(r'[^\w\s]', '', skill_lower)
        skill_lower = ' '.join(skill_lower.split())
        
        # Check if skill exists in mapping
        if skill_lower in cls.SKILL_NORMALIZATION_MAP:
            return cls.SKILL_NORMALIZATION_MAP[skill_lower]
        
        # Check for partial matches (skill is contained in mapping key)
        for key, value in cls.SKILL_NORMALIZATION_MAP.items():
            if key in skill_lower or skill_lower in key:
                return value
        
        # If no match, return original with proper capitalization
        return skill.strip().title()
    
    @classmethod
    def normalize_skill_list(cls, skills_list):
        """
        Normalize a list of skills
        
        Args:
            skills_list: List of raw skill strings
            
        Returns:
            List of normalized skill names (unique)
        """
        if not skills_list:
            return []
        
        normalized = []
        for skill in skills_list:
            norm_skill = cls.normalize_skill(skill)
            if norm_skill and norm_skill not in normalized:
                normalized.append(norm_skill)
        
        return normalized


# ============================================================
# PART 2: DEMAND DATA PROCESSOR (Job Postings)
# ============================================================

class DemandDataProcessor:
    """
    Processes job posting data to extract and normalize skills
    """
    
    def __init__(self, filepath):
        """
        Args:
            filepath: Path to CSV file containing job postings
        """
        self.filepath = filepath
        self.raw_df = None
        self.processed_df = None
        self.expanded_df = None
    
    def load_data(self):
        """Load the raw demand dataset"""
        print(f"  Loading demand data from: {self.filepath}")
        self.raw_df = pd.read_csv(self.filepath)
        print(f"  Loaded {len(self.raw_df)} job postings")
        return self.raw_df
    
    def clean_text_field(self, text):
        """
        Clean text fields (job titles, descriptions)
        """
        if pd.isna(text):
            return ""
        text = str(text)
        text = text.lower()
        text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
        text = ' '.join(text.split())
        return text
    
    def extract_skills_from_description(self, description):
        """
        Extract skill keywords from job description text
        """
        if pd.isna(description):
            return []
        
        description = self.clean_text_field(description)
        found_skills = []
        
        # Check for each known skill pattern
        for skill_variant, normalized in SkillNormalizer.SKILL_NORMALIZATION_MAP.items():
            if skill_variant in description:
                if normalized not in found_skills:
                    found_skills.append(normalized)
        
        return found_skills
    
    def parse_skills_column(self, skills_data):
        """
        Parse skills from string representation if needed
        """
        if pd.isna(skills_data):
            return []
        if isinstance(skills_data, str):
            # Clean and split
            skills_data = skills_data.replace('[', '').replace(']', '').replace("'", "")
            return [s.strip() for s in skills_data.split(',') if s.strip()]
        elif isinstance(skills_data, list):
            return skills_data
        return []
    
    def normalize_job_title(self, title):
        """
        Normalize job title to standard category
        """
        title = self.clean_text_field(title)
        
        # Role detection logic
        if 'python' in title:
            return 'Python Developer'
        elif 'java' in title and 'script' not in title:
            return 'Java Developer'
        elif 'javascript' in title or 'js' in title:
            return 'JavaScript Developer'
        elif 'react' in title:
            return 'React Developer'
        elif 'frontend' in title or 'front-end' in title:
            return 'Frontend Developer'
        elif 'backend' in title or 'back-end' in title:
            return 'Backend Developer'
        elif 'fullstack' in title or 'full-stack' in title or 'full stack' in title:
            return 'Full Stack Developer'
        elif 'data scientist' in title or 'machine learning' in title or 'ai' in title:
            return 'Data Scientist'
        elif 'data analyst' in title or 'business intelligence' in title:
            return 'Data Analyst'
        elif 'data engineer' in title:
            return 'Data Engineer'
        elif 'devops' in title or 'sre' in title:
            return 'DevOps Engineer'
        elif 'cloud' in title:
            return 'Cloud Engineer'
        elif 'security' in title or 'cyber' in title:
            return 'Cybersecurity Analyst'
        elif 'product manager' in title or 'product owner' in title:
            return 'Product Manager'
        elif 'ui' in title or 'ux' in title or 'designer' in title:
            return 'UI/UX Designer'
        elif 'mobile' in title or 'android' in title or 'ios' in title or 'flutter' in title:
            return 'Mobile Developer'
        elif 'qa' in title or 'quality' in title or 'test' in title:
            return 'QA Engineer'
        elif 'database' in title or 'dba' in title:
            return 'Database Administrator'
        elif 'network' in title:
            return 'Network Engineer'
        else:
            return 'Software Developer'
    
    def process(self):
        """
        Main processing pipeline for demand data
        """
        print("\n" + "=" * 60)
        print("PROCESSING DEMAND DATASET (Job Postings)")
        print("=" * 60)
        
        # Load data if not already loaded
        if self.raw_df is None:
            self.load_data()
        
        # Create a copy
        df = self.raw_df.copy()
        
        # Step 1: Handle missing values
        print("\n📊 Step 1: Handling missing values...")
        print(f"   Initial shape: {df.shape}")
        
        if 'description' in df.columns:
            df['description'] = df['description'].fillna('')
        
        if 'job_title' in df.columns:
            df['job_title'] = df['job_title'].fillna('Unknown')
        
        if 'company' in df.columns:
            df['company'] = df['company'].fillna('Unknown')
        
        print(f"   After cleaning: {df.shape}")
        
        # Step 2: Normalize job titles
        print("\n📊 Step 2: Normalizing job titles...")
        df['normalized_title'] = df['job_title'].apply(self.normalize_job_title)
        
        # Step 3: Extract and normalize skills
        print("\n📊 Step 3: Extracting and normalizing skills...")
        
        # Check if required_skills column exists
        if 'required_skills' in df.columns:
            # Parse skills from string representation
            df['raw_skills'] = df['required_skills'].apply(self.parse_skills_column)
            df['normalized_skills'] = df['raw_skills'].apply(SkillNormalizer.normalize_skill_list)
            print("   Skills extracted from 'required_skills' column")
            
        elif 'description' in df.columns:
            # Extract skills from description
            df['extracted_skills'] = df['description'].apply(self.extract_skills_from_description)
            df['normalized_skills'] = df['extracted_skills'].apply(SkillNormalizer.normalize_skill_list)
            print("   Skills extracted from 'description' column")
        else:
            df['normalized_skills'] = [[] for _ in range(len(df))]
            print("   No skill column found. Created empty skill lists.")
        
        # Step 4: Calculate skill count
        df['skill_count'] = df['normalized_skills'].apply(len)
        
        # Step 5: Create expanded format (one skill per row)
        print("\n📊 Step 4: Creating expanded format...")
        
        expanded_rows = []
        for idx, row in df.iterrows():
            for skill in row['normalized_skills']:
                expanded_rows.append({
                    'job_id': idx,
                    'job_title': row.get('job_title', 'Unknown'),
                    'normalized_title': row['normalized_title'],
                    'company': row.get('company', 'Unknown'),
                    'location': row.get('location', 'Unknown'),
                    'required_skill': skill,
                    'source': row.get('source', 'Unknown')
                })
        
        self.expanded_df = pd.DataFrame(expanded_rows)
        self.processed_df = df
        
        print(f"\n✅ Demand processing complete!")
        print(f"   Processed jobs: {len(df)}")
        print(f"   Expanded entries: {len(self.expanded_df)}")
        print(f"   Average skills per job: {df['skill_count'].mean():.1f}")
        print(f"   Unique skills found: {self.expanded_df['required_skill'].nunique() if not self.expanded_df.empty else 0}")
        
        return self.processed_df, self.expanded_df
    
    def save_processed_data(self, output_prefix='demand_processed'):
        """
        Save processed data to CSV files
        """
        if self.processed_df is not None:
            self.processed_df.to_csv(f'{output_prefix}.csv', index=False)
            print(f"  ✓ Saved: {output_prefix}.csv")
        
        if self.expanded_df is not None and not self.expanded_df.empty:
            self.expanded_df.to_csv(f'{output_prefix}_expanded.csv', index=False)
            print(f"  ✓ Saved: {output_prefix}_expanded.csv")


# ============================================================
# PART 3: SUPPLY DATA PROCESSOR (Resume Profiles)
# ============================================================

class SupplyDataProcessor:
    """
    Processes resume profile data to extract and normalize skills
    """
    
    def __init__(self, filepath):
        """
        Args:
            filepath: Path to CSV file containing resume profiles
        """
        self.filepath = filepath
        self.raw_df = None
        self.processed_df = None
        self.expanded_df = None
    
    def load_data(self):
        """Load the raw supply dataset"""
        print(f"  Loading supply data from: {self.filepath}")
        self.raw_df = pd.read_csv(self.filepath)
        print(f"  Loaded {len(self.raw_df)} resume profiles")
        return self.raw_df
    
    def parse_skills_column(self, skills_data):
        """
        Parse skills from string representation
        """
        if pd.isna(skills_data):
            return []
        if isinstance(skills_data, str):
            # Clean and split
            skills_data = skills_data.replace('[', '').replace(']', '').replace("'", "")
            return [s.strip() for s in skills_data.split(',') if s.strip()]
        elif isinstance(skills_data, list):
            return skills_data
        return []
    
    def normalize_experience(self, exp):
        """
        Normalize experience level to standard format
        """
        if pd.isna(exp):
            return 'Not Specified'
        
        exp_str = str(exp).lower()
        
        if 'entry' in exp_str or '0-2' in exp_str or 'junior' in exp_str:
            return 'Entry Level (0-2 years)'
        elif 'mid' in exp_str or '3-5' in exp_str or 'intermediate' in exp_str:
            return 'Mid Level (3-5 years)'
        elif 'senior' in exp_str or '5-8' in exp_str or 'lead' in exp_str:
            return 'Senior Level (5-8 years)'
        elif 'principal' in exp_str or 'architect' in exp_str or '8+' in exp_str or '10+' in exp_str:
            return 'Lead Level (8+ years)'
        else:
            return 'Not Specified'
    
    def process(self):
        """
        Main processing pipeline for supply data
        """
        print("\n" + "=" * 60)
        print("PROCESSING SUPPLY DATASET (Resume Profiles)")
        print("=" * 60)
        
        # Load data if not already loaded
        if self.raw_df is None:
            self.load_data()
        
        # Create a copy
        df = self.raw_df.copy()
        
        # Step 1: Handle missing values
        print("\n📊 Step 1: Handling missing values...")
        print(f"   Initial shape: {df.shape}")
        
        if 'role_category' in df.columns:
            df['role_category'] = df['role_category'].fillna('Other')
        else:
            df['role_category'] = 'Not Specified'
        
        print(f"   After cleaning: {df.shape}")
        
        # Step 2: Find which column contains skills
        print("\n📊 Step 2: Parsing and normalizing skills...")
        
        skill_column = None
        for col in ['skills', 'required_skills', 'skill_list', 'normalized_skills']:
            if col in df.columns:
                skill_column = col
                break
        
        if skill_column:
            df['raw_skills'] = df[skill_column].apply(self.parse_skills_column)
            print(f"   Skills parsed from column: '{skill_column}'")
        else:
            df['raw_skills'] = [[] for _ in range(len(df))]
            print("   No skills column found. Created empty skill lists.")
        
        # Step 3: Normalize skills
        df['normalized_skills'] = df['raw_skills'].apply(SkillNormalizer.normalize_skill_list)
        
        # Step 4: Calculate skill count
        df['skill_count'] = df['normalized_skills'].apply(len)
        
        # Step 5: Normalize experience levels
        print("\n📊 Step 3: Normalizing experience levels...")
        
        if 'experience_level' in df.columns:
            df['normalized_experience'] = df['experience_level'].apply(self.normalize_experience)
        elif 'experience_years' in df.columns:
            df['normalized_experience'] = df['experience_years'].apply(self.normalize_experience)
        else:
            df['normalized_experience'] = 'Not Specified'
        
        # Step 6: Create expanded format (one skill per row)
        print("\n📊 Step 4: Creating expanded format...")
        
        expanded_rows = []
        for idx, row in df.iterrows():
            for skill in row['normalized_skills']:
                expanded_rows.append({
                    'profile_id': row.get('profile_id', f'PROF_{idx:04d}'),
                    'role_category': row.get('role_category', 'Unknown'),
                    'normalized_experience': row['normalized_experience'],
                    'skill': skill,
                    'skill_count': len(row['normalized_skills']),
                    'source': row.get('source', 'Unknown')
                })
        
        self.expanded_df = pd.DataFrame(expanded_rows)
        self.processed_df = df
        
        print(f"\n✅ Supply processing complete!")
        print(f"   Processed profiles: {len(df)}")
        print(f"   Expanded entries: {len(self.expanded_df)}")
        print(f"   Average skills per profile: {df['skill_count'].mean():.1f}")
        print(f"   Unique skills found: {self.expanded_df['skill'].nunique() if not self.expanded_df.empty else 0}")
        
        return self.processed_df, self.expanded_df
    
    def save_processed_data(self, output_prefix='supply_processed'):
        """
        Save processed data to CSV files
        """
        if self.processed_df is not None:
            self.processed_df.to_csv(f'{output_prefix}.csv', index=False)
            print(f"  ✓ Saved: {output_prefix}.csv")
        
        if self.expanded_df is not None and not self.expanded_df.empty:
            self.expanded_df.to_csv(f'{output_prefix}_expanded.csv', index=False)
            print(f"  ✓ Saved: {output_prefix}_expanded.csv")


# ============================================================
# PART 4: MAIN EXECUTION
# ============================================================

def run_processing_pipeline(demand_file, supply_file):
    """
    Run the complete data processing pipeline (NO GAP ANALYSIS)
    
    Args:
        demand_file: Path to demand dataset CSV
        supply_file: Path to supply dataset CSV
    """
    print("\n" + "=" * 70)
    print("DATA PROCESSING AND NORMALIZATION PIPELINE")
    print("(No Quantitative Gap Analysis)")
    print("=" * 70)
    
    # Process Demand Data
    print("\n🔧 Processing Demand Dataset")
    demand_processor = DemandDataProcessor(demand_file)
    demand_processed, demand_expanded = demand_processor.process()
    demand_processor.save_processed_data('demand_processed')
    
    # Process Supply Data
    print("\n🔧 Processing Supply Dataset")
    supply_processor = SupplyDataProcessor(supply_file)
    supply_processed, supply_expanded = supply_processor.process()
    supply_processor.save_processed_data('supply_processed')
    
    # Summary
    print("\n" + "=" * 70)
    print("PROCESSING COMPLETE - SUMMARY")
    print("=" * 70)
    
    print(f"\n📊 DEMAND DATASET (Job Postings):")
    print(f"   Original jobs: {len(demand_processor.raw_df) if demand_processor.raw_df is not None else 0}")
    print(f"   Processed jobs: {len(demand_processed)}")
    print(f"   Expanded skill entries: {len(demand_expanded)}")
    print(f"   Average skills per job: {demand_processed['skill_count'].mean():.1f}")
    print(f"   Unique skills: {demand_expanded['required_skill'].nunique() if not demand_expanded.empty else 0}")
    
    print(f"\n👥 SUPPLY DATASET (Resume Profiles):")
    print(f"   Original profiles: {len(supply_processor.raw_df) if supply_processor.raw_df is not None else 0}")
    print(f"   Processed profiles: {len(supply_processed)}")
    print(f"   Expanded skill entries: {len(supply_expanded)}")
    print(f"   Average skills per profile: {supply_processed['skill_count'].mean():.1f}")
    print(f"   Unique skills: {supply_expanded['skill'].nunique() if not supply_expanded.empty else 0}")
    
    print(f"\n📁 FILES CREATED:")
    print(f"   - demand_processed.csv")
    print(f"   - demand_processed_expanded.csv")
    print(f"   - supply_processed.csv")
    print(f"   - supply_processed_expanded.csv")
    
    print("\n" + "=" * 70)
    print("✅ PROCESSING AND NORMALIZATION COMPLETE!")
    print("   Data is now ready for gap analysis.")
    print("=" * 70)
    
    return demand_processed, demand_expanded, supply_processed, supply_expanded


# ============================================================
# RUN THE PIPELINE
# ============================================================

if __name__ == "__main__":
    # Set working directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    if script_dir:
        os.chdir(script_dir)
        print(f"Working directory: {os.getcwd()}")
    
    # File paths - UPDATE THESE TO YOUR ACTUAL FILE NAMES
    DEMAND_FILE = 'demand_dataset_2000_jobs.csv'
    SUPPLY_FILE = 'supply_dataset_tech_resumes.csv'
    
    # Check if files exist
    if not os.path.exists(DEMAND_FILE):
        print(f"⚠️ Warning: {DEMAND_FILE} not found!")
        print("   Searching for alternative demand files...")
        
        # Try alternative filenames
        alternatives = ['demand_dataset_with_skills.csv', 'demand_processed.csv', 'demand_dataset.csv']
        for alt in alternatives:
            if os.path.exists(alt):
                DEMAND_FILE = alt
                print(f"   Using: {DEMAND_FILE}")
                break
        else:
            print("   No demand dataset found. Please run demand generator first.")
            exit(1)
    
    if not os.path.exists(SUPPLY_FILE):
        print(f"⚠️ Warning: {SUPPLY_FILE} not found!")
        print("   Searching for alternative supply files...")
        
        alternatives = ['supply_processed.csv', 'supply_dataset.csv', 'supply_data.csv']
        for alt in alternatives:
            if os.path.exists(alt):
                SUPPLY_FILE = alt
                print(f"   Using: {SUPPLY_FILE}")
                break
        else:
            print("   No supply dataset found. Please run supply generator first.")
            exit(1)
    
    # Run the processing pipeline
    demand_data, demand_expanded, supply_data, supply_expanded = run_processing_pipeline(DEMAND_FILE, SUPPLY_FILE)