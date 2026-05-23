"""
Regenerate Technical Skill Bundles - All Categories
Run this to create a complete technical_skill_bundles.csv file
"""

import pandas as pd
import ast
from mlxtend.frequent_patterns import apriori, association_rules
from mlxtend.preprocessing import TransactionEncoder

# ============================================================
# COMPREHENSIVE TECHNICAL SKILLS - ALL CATEGORIES
# ============================================================

TECHNICAL_SKILLS = {
    # Programming Languages
    'Python', 'Java', 'JavaScript', 'TypeScript', 'C++', 'C#', 'Go', 'Ruby',
    'PHP', 'Swift', 'Kotlin', 'Rust', 'Scala', 'Dart', 'R', 'MATLAB',
    
    # Frontend
    'React', 'Angular', 'Vue.js', 'Next.js', 'Redux', 'Webpack', 'jQuery',
    'Bootstrap', 'Tailwind CSS', 'HTML/CSS', 'TypeScript',
    
    # Backend
    'Node.js', 'Django', 'Flask', 'Spring Boot', 'Express.js', 'Laravel',
    'ASP.NET', 'FastAPI', 'GraphQL', 'REST APIs', 'Microservices',
    
    # Databases
    'SQL', 'PostgreSQL', 'MySQL', 'MongoDB', 'Redis', 'Elasticsearch',
    'Cassandra', 'Oracle', 'Firebase', 'DynamoDB', 'SQLite',
    
    # Cloud & DevOps
    'AWS', 'Azure', 'Google Cloud', 'Docker', 'Kubernetes', 'Terraform',
    'Jenkins', 'CI/CD', 'Linux', 'Bash', 'Serverless', 'Lambda',
    
    # Data Science
    'Machine Learning', 'Deep Learning', 'Data Science', 'Pandas', 'NumPy',
    'Scikit-learn', 'TensorFlow', 'PyTorch', 'Statistics', 'Tableau', 'Power BI',
    
    # Security (keep but don't dominate)
    'Cybersecurity', 'Network Security', 'Firewalls', 'Penetration Testing',
    'SIEM', 'Incident Response', 'Cryptography',
    
    # Mobile
    'Android', 'iOS', 'React Native', 'Flutter', 'Xamarin',
    
    # Testing
    'Unit Testing', 'Test Automation', 'Selenium', 'Jest', 'PyTest',
    
    # Tools
    'Git', 'JIRA', 'Confluence'
}

def load_and_process_demand_data(filepath='demand_processed.csv'):
    """Load demand data and extract technical skills"""
    print("Loading demand data...")
    df = pd.read_csv(filepath)
    print(f"Loaded {len(df)} job postings")
    
    # Find skills column
    skills_col = None
    for col in ['normalized_skills', 'required_skills', 'skills']:
        if col in df.columns:
            skills_col = col
            break
    
    if skills_col is None:
        raise ValueError("No skills column found")
    
    # Extract transactions
    transactions = []
    category_counts = {cat: 0 for cat in [
        'Programming', 'Frontend', 'Backend', 'Databases', 'Cloud/DevOps', 
        'Data Science', 'Security', 'Mobile', 'Testing', 'Tools'
    ]}
    
    for idx, row in df.iterrows():
        skills = row[skills_col]
        
        if isinstance(skills, str):
            try:
                skills = ast.literal_eval(skills)
            except:
                skills = [s.strip() for s in skills.strip('[]').replace("'", "").split(',') if s.strip()]
        
        if not isinstance(skills, list):
            skills = []
        
        # Filter to technical skills only
        technical_skills = [s for s in skills if s in TECHNICAL_SKILLS]
        
        if len(technical_skills) >= 2:  # Need at least 2 skills for bundling
            transactions.append(technical_skills)
            
            # Count categories for reporting
            for skill in technical_skills:
                if skill in ['Python', 'Java', 'JavaScript', 'C++', 'Go', 'Ruby', 'PHP', 'Rust']:
                    category_counts['Programming'] += 1
                elif skill in ['React', 'Angular', 'Vue.js', 'HTML/CSS', 'Tailwind CSS']:
                    category_counts['Frontend'] += 1
                elif skill in ['Node.js', 'Django', 'Flask', 'Spring Boot', 'Express.js']:
                    category_counts['Backend'] += 1
                elif skill in ['SQL', 'PostgreSQL', 'MySQL', 'MongoDB', 'Redis']:
                    category_counts['Databases'] += 1
                elif skill in ['AWS', 'Docker', 'Kubernetes', 'Terraform', 'Jenkins', 'CI/CD']:
                    category_counts['Cloud/DevOps'] += 1
                elif skill in ['Machine Learning', 'Pandas', 'TensorFlow', 'Data Science']:
                    category_counts['Data Science'] += 1
                elif skill in ['Cybersecurity', 'Firewalls', 'Network Security']:
                    category_counts['Security'] += 1
                elif skill in ['Android', 'iOS', 'Flutter', 'React Native']:
                    category_counts['Mobile'] += 1
                elif skill in ['Unit Testing', 'Selenium', 'Test Automation']:
                    category_counts['Testing'] += 1
                elif skill in ['Git', 'JIRA']:
                    category_counts['Tools'] += 1
    
    print(f"\n📊 Transaction Summary:")
    print(f"   Total transactions: {len(transactions)}")
    print(f"\n📊 Skill Category Distribution:")
    for cat, count in sorted(category_counts.items(), key=lambda x: x[1], reverse=True):
        if count > 0:
            print(f"   {cat}: {count} skill mentions")
    
    return transactions

def run_apriori_on_technical_skills(transactions, min_support=0.015, min_confidence=0.4, min_lift=1.2):
    """Run Apriori on technical skills"""
    print(f"\n🔧 Running Apriori with:")
    print(f"   Min support: {min_support} ({min_support*100}% of jobs)")
    print(f"   Min confidence: {min_confidence}")
    print(f"   Min lift: {min_lift}")
    
    te = TransactionEncoder()
    te_ary = te.fit(transactions).transform(transactions)
    df_encoded = pd.DataFrame(te_ary, columns=te.columns_)
    
    print(f"   Skills in analysis: {len(te.columns_)}")
    
    frequent_itemsets = apriori(df_encoded, min_support=min_support, use_colnames=True, max_len=3)
    print(f"   Frequent itemsets found: {len(frequent_itemsets)}")
    
    if len(frequent_itemsets) == 0:
        print("   No frequent itemsets. Try lowering min_support.")
        return None
    
    rules = association_rules(frequent_itemsets, metric="lift", min_threshold=min_lift)
    rules = rules[rules['confidence'] >= min_confidence]
    rules = rules.sort_values('lift', ascending=False)
    
    print(f"   Association rules generated: {len(rules)}")
    
    # Convert frozenset to strings
    rules['antecedents'] = rules['antecedents'].apply(lambda x: ', '.join(list(x)))
    rules['consequents'] = rules['consequents'].apply(lambda x: ', '.join(list(x)))
    
    return rules

def main():
    print("=" * 70)
    print("REGENERATING TECHNICAL SKILL BUNDLES - ALL CATEGORIES")
    print("=" * 70)
    
    # Load data
    transactions = load_and_process_demand_data('demand_processed.csv')
    
    if len(transactions) < 100:
        print(f"\n⚠️ Only {len(transactions)} transactions. Consider collecting more data.")
        return
    
    # Run Apriori with lower thresholds to capture more bundles
    rules = run_apriori_on_technical_skills(
        transactions, 
        min_support=0.01,      # Lowered to capture more rules
        min_confidence=0.35,   # Lowered to include more bundles
        min_lift=1.1           # Lowered to include positive associations
    )
    
    if rules is None or len(rules) == 0:
        print("\n⚠️ No rules generated. Try lowering thresholds further.")
        return
    
    # Display results by category
    print("\n" + "=" * 70)
    print("SKILL BUNDLES BY CATEGORY")
    print("=" * 70)
    
    categories = {
        'Cloud/DevOps': ['AWS', 'Docker', 'Kubernetes', 'Terraform', 'Jenkins', 'CI/CD', 'Linux', 'Azure'],
        'Backend': ['Python', 'Django', 'Flask', 'Node.js', 'Express', 'Java', 'Spring', 'SQL', 'PostgreSQL'],
        'Frontend': ['React', 'Angular', 'Vue', 'JavaScript', 'TypeScript', 'HTML', 'CSS', 'Redux'],
        'Data Science': ['Python', 'Pandas', 'NumPy', 'Machine Learning', 'TensorFlow', 'Tableau', 'SQL'],
        'Databases': ['SQL', 'PostgreSQL', 'MySQL', 'MongoDB', 'Redis', 'Database'],
        'Security': ['Firewalls', 'Network Security', 'Cybersecurity', 'SIEM', 'Penetration'],
        'Programming Languages': ['Python', 'Java', 'JavaScript', 'Go', 'Rust', 'C++'],
        'Mobile': ['Android', 'iOS', 'Flutter', 'React Native', 'Kotlin', 'Swift'],
        'Testing': ['Unit Testing', 'Selenium', 'Test Automation', 'Jest', 'PyTest']
    }
    
    for category, keywords in categories.items():
        category_rules = rules[
            rules['antecedents'].str.contains('|'.join(keywords), case=False, na=False) |
            rules['consequents'].str.contains('|'.join(keywords), case=False, na=False)
        ]
        
        if len(category_rules) > 0:
            print(f"\n📁 {category}: {len(category_rules)} bundles")
            for idx, row in category_rules.head(5).iterrows():
                print(f"   • {row['antecedents']} → {row['consequents']} (Lift: {row['lift']:.2f}, Conf: {row['confidence']:.2f})")
    
    # Save all rules
    rules.to_csv('technical_skill_bundles_complete.csv', index=False)
    print(f"\n✅ Saved {len(rules)} rules to technical_skill_bundles_complete.csv")
    
    # Show top 20 overall
    print("\n" + "=" * 70)
    print("TOP 20 TECHNICAL SKILL BUNDLES (All Categories)")
    print("=" * 70)
    print(f"{'#':<3} {'If you have...':<35} {'You also need...':<35} {'Lift':<8}")
    print("-" * 85)
    
    for i, row in rules.head(20).iterrows():
        ant = row['antecedents'][:32] + ".." if len(row['antecedents']) > 32 else row['antecedents']
        con = row['consequents'][:32] + ".." if len(row['consequents']) > 32 else row['consequents']
        print(f"{i+1:<3} {ant:<35} {con:<35} {row['lift']:<8.2f}")

if __name__ == "__main__":
    main()