import pandas as pd

df = pd.read_csv('skill_bundles_apriori.csv')

# Design and soft skill keywords to exclude
design_keywords = [
    'Figma', 'Adobe Xd', 'Adobe XD', 'Sketch', 'InVision',
    'Wireframing', 'Prototyping', 'Prototype', 'Usability Testing',
    'User Research', 'Information Architecture', 'Visual Design',
    'UI', 'UX', 'Design Systems', 'Responsive Design',
    'Teamwork', 'Communication', 'Leadership', 'Problem Solving',
    'Agile', 'Scrum', 'JIRA', 'Confluence'
]

def contains_design(text):
    if pd.isna(text):
        return False
    text_lower = str(text).lower()
    for keyword in design_keywords:
        if keyword.lower() in text_lower:
            return True
    return False

# Keep only rows with NO design skills
technical_df = df[
    ~df['antecedents'].apply(contains_design) & 
    ~df['consequents'].apply(contains_design)
]

technical_df = technical_df.sort_values('lift', ascending=False)
technical_df.to_csv('skill_bundles_technical_exclude_design.csv', index=False)

print(f"Technical bundles (design excluded): {len(technical_df)}")
print(technical_df[['antecedents', 'consequents', 'lift', 'support']].head(20))