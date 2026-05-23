"""
Skills Gap Analysis - Works with demand_processed.csv and supply_processed.csv
"""

import pandas as pd
import os
import ast

class SkillsGapAnalyzer:
    def __init__(self, demand_file, supply_file):
        self.demand_file = demand_file
        self.supply_file = supply_file
        self.demand_df = None
        self.supply_df = None
        self.gap_results = None
    
    def load_and_expand_data(self):
        """Load non-expanded CSVs and expand to one skill per row"""
        print("\n📂 Loading data from:")
        print(f"   Demand: {self.demand_file}")
        print(f"   Supply: {self.supply_file}")
        
        # Load demand data
        self.demand_df = pd.read_csv(self.demand_file)
        print(f"   Demand rows: {len(self.demand_df)}")
        
        # Load supply data
        self.supply_df = pd.read_csv(self.supply_file)
        print(f"   Supply rows: {len(self.supply_df)}")
        
        # Expand demand skills (one skill per row)
        demand_expanded = []
        for idx, row in self.demand_df.iterrows():
            skills = row.get('normalized_skills', row.get('required_skills', row.get('skills', '[]')))
            if isinstance(skills, str):
                try:
                    skills = ast.literal_eval(skills)
                except:
                    skills = [s.strip() for s in skills.strip('[]').split(',') if s.strip()]
            if not isinstance(skills, list):
                skills = []
            for skill in skills:
                demand_expanded.append({
                    'job_id': idx,
                    'job_title': row.get('job_title', row.get('normalized_title', 'Unknown')),
                    'required_skill': skill
                })
        self.demand_expanded = pd.DataFrame(demand_expanded)
        
        # Expand supply skills
        supply_expanded = []
        for idx, row in self.supply_df.iterrows():
            skills = row.get('normalized_skills', row.get('skills', row.get('required_skills', '[]')))
            if isinstance(skills, str):
                try:
                    skills = ast.literal_eval(skills)
                except:
                    skills = [s.strip() for s in skills.strip('[]').split(',') if s.strip()]
            if not isinstance(skills, list):
                skills = []
            for skill in skills:
                supply_expanded.append({
                    'profile_id': row.get('profile_id', idx),
                    'role_category': row.get('role_category', row.get('normalized_title', 'Unknown')),
                    'skill': skill
                })
        self.supply_expanded = pd.DataFrame(supply_expanded)
        
        print(f"\n✅ Expanded demand: {len(self.demand_expanded)} skill entries")
        print(f"✅ Expanded supply: {len(self.supply_expanded)} skill entries")
        
        return self.demand_expanded, self.supply_expanded
    
    def calculate_gap_scores(self):
        print("\n" + "=" * 70)
        print("CALCULATING SKILLS GAP SCORES")
        print("=" * 70)
        
        total_jobs = self.demand_expanded['job_id'].nunique()
        total_profiles = self.supply_expanded['profile_id'].nunique()
        
        print(f"\n📈 Total job postings: {total_jobs}")
        print(f"📈 Total candidate profiles: {total_profiles}")
        
        demand_freq = self.demand_expanded['required_skill'].value_counts()
        demand_pct = (demand_freq / total_jobs) * 100
        
        supply_freq = self.supply_expanded['skill'].value_counts()
        supply_pct = (supply_freq / total_profiles) * 100
        
        all_skills = set(demand_freq.index) | set(supply_freq.index)
        print(f"\n📊 Total unique skills: {len(all_skills)}")
        
        gap_data = []
        for skill in all_skills:
            demand_score = demand_pct.get(skill, 0)
            supply_score = supply_pct.get(skill, 0)
            gap_score = demand_score - supply_score
            
            if gap_score > 10:
                status = "Critical Shortage"
            elif gap_score > 5:
                status = "Moderate Shortage"
            elif gap_score > 0:
                status = "Mild Shortage"
            elif gap_score == 0:
                status = "Balanced"
            elif gap_score > -5:
                status = "Mild Surplus"
            elif gap_score > -10:
                status = "Moderate Surplus"
            else:
                status = "Critical Surplus"
            
            gap_data.append({
                'skill': skill,
                'demand_percentage': round(demand_score, 2),
                'supply_percentage': round(supply_score, 2),
                'gap_score': round(gap_score, 2),
                'status': status
            })
        
        self.gap_results = pd.DataFrame(gap_data)
        self.gap_results = self.gap_results.sort_values('gap_score', ascending=False)
        
        print(f"\n✅ Gap calculation complete!")
        print(f"   Skills in shortage: {len(self.gap_results[self.gap_results['gap_score'] > 0])}")
        print(f"   Skills in surplus: {len(self.gap_results[self.gap_results['gap_score'] < 0])}")
        
        return self.gap_results
    
    def get_top_shortages(self, n=20):
        if self.gap_results is None:
            self.calculate_gap_scores()
        return self.gap_results.head(n)
    
    def get_top_surpluses(self, n=20):
        if self.gap_results is None:
            self.calculate_gap_scores()
        return self.gap_results.tail(n).sort_values('gap_score')
    
    def generate_summary_report(self):
        if self.gap_results is None:
            self.calculate_gap_scores()
        
        print("\n" + "=" * 70)
        print("SKILLS GAP ANALYSIS - SUMMARY REPORT")
        print("=" * 70)
        
        total = len(self.gap_results)
        shortage = len(self.gap_results[self.gap_results['gap_score'] > 0])
        surplus = len(self.gap_results[self.gap_results['gap_score'] < 0])
        balanced = len(self.gap_results[self.gap_results['gap_score'] == 0])
        
        print(f"\n📊 Total skills analyzed: {total}")
        print(f"   Skills in shortage (Demand > Supply): {shortage}")
        print(f"   Skills in surplus (Supply > Demand): {surplus}")
        print(f"   Balanced skills: {balanced}")
        
        avg_gap = self.gap_results['gap_score'].mean()
        print(f"\n📊 Average gap score: {avg_gap:.2f}%")
        print(f"   Largest shortage: {self.gap_results.iloc[0]['skill']} ({self.gap_results.iloc[0]['gap_score']:.1f}%)")
        print(f"   Largest surplus: {self.gap_results.iloc[-1]['skill']} ({self.gap_results.iloc[-1]['gap_score']:.1f}%)")
        
        return {'total': total, 'shortage': shortage, 'surplus': surplus, 'avg_gap': avg_gap}
    
    def save_gap_results(self, filename='skills_gap_analysis.csv'):
        if self.gap_results is not None:
            self.gap_results.to_csv(filename, index=False)
            print(f"\n  ✓ Saved: {filename}")
    
    def save_top_shortages(self, filename='top_shortages.csv', n=20):
        self.get_top_shortages(n).to_csv(filename, index=False)
        print(f"  ✓ Saved: {filename}")
    
    def save_top_surpluses(self, filename='top_surpluses.csv', n=20):
        self.get_top_surpluses(n).to_csv(filename, index=False)
        print(f"  ✓ Saved: {filename}")


class GapVisualizer:
    @staticmethod
    def print_top_shortages(gap_results, n=15):
        print("\n" + "=" * 80)
        print(f"TOP {n} SKILLS IN SHORTAGE (High Demand, Low Supply)")
        print("=" * 80)
        print(f"{'Skill':<25} {'Demand %':<12} {'Supply %':<12} {'Gap %':<10} {'Status':<20}")
        print("-" * 80)
        
        for idx, row in gap_results.head(n).iterrows():
            print(f"{row['skill']:<25} {row['demand_percentage']:<12.1f} {row['supply_percentage']:<12.1f} "
                  f"{row['gap_score']:<10.1f} {row['status']:<20}")
    
    @staticmethod
    def print_top_surpluses(gap_results, n=15):
        print("\n" + "=" * 80)
        print(f"TOP {n} SKILLS IN SURPLUS (Low Demand, High Supply)")
        print("=" * 80)
        print(f"{'Skill':<25} {'Demand %':<12} {'Supply %':<12} {'Gap %':<10} {'Status':<20}")
        print("-" * 80)
        
        surpluses = gap_results.tail(n).sort_values('gap_score')
        for idx, row in surpluses.iterrows():
            print(f"{row['skill']:<25} {row['demand_percentage']:<12.1f} {row['supply_percentage']:<12.1f} "
                  f"{row['gap_score']:<10.1f} {row['status']:<20}")
    
    @staticmethod
    def print_recommendations(gap_results, n=10):
        print("\n" + "=" * 80)
        print(f"TOP {n} CRITICAL RECOMMENDATIONS")
        print("=" * 80)
        
        critical = gap_results[gap_results['gap_score'] > 10].head(n)
        
        for idx, row in critical.iterrows():
            print(f"\n🎯 {row['skill']}")
            print(f"   Gap: {row['gap_score']:.1f}% (Demand: {row['demand_percentage']:.1f}%, Supply: {row['supply_percentage']:.1f}%)")
            if row['gap_score'] > 15:
                print(f"   → URGENT: Increase training and hiring for this skill")
            elif row['gap_score'] > 10:
                print(f"   → PRIORITY: Focus on upskilling programs")
            else:
                print(f"   → Monitor: Slight shortage")


def run_gap_analysis(demand_file, supply_file):
    print("\n" + "=" * 70)
    print("QUANTITATIVE SKILLS GAP ANALYSIS")
    print("Demand (Job Requirements) vs Supply (Candidate Skills)")
    print("=" * 70)
    
    analyzer = SkillsGapAnalyzer(demand_file, supply_file)
    analyzer.load_and_expand_data()
    gap_results = analyzer.calculate_gap_scores()
    analyzer.generate_summary_report()
    
    GapVisualizer.print_top_shortages(gap_results, n=15)
    GapVisualizer.print_top_surpluses(gap_results, n=10)
    GapVisualizer.print_recommendations(gap_results, n=10)
    
    analyzer.save_gap_results('skills_gap_analysis.csv')
    analyzer.save_top_shortages('top_shortages.csv', n=30)
    analyzer.save_top_surpluses('top_surpluses.csv', n=30)
    
    print("\n" + "=" * 70)
    print("✅ GAP ANALYSIS COMPLETE!")
    print("   Files created:")
    print("   - skills_gap_analysis.csv")
    print("   - top_shortages.csv")
    print("   - top_surpluses.csv")
    print("=" * 70)
    
    return gap_results


if __name__ == "__main__":
    # Set working directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    if script_dir:
        os.chdir(script_dir)
        print(f"Working directory: {os.getcwd()}")
    
    # Use the existing processed files (non-expanded)
    DEMAND_FILE = 'demand_processed.csv'
    SUPPLY_FILE = 'supply_processed.csv'
    
    # Check if files exist
    if not os.path.exists(DEMAND_FILE):
        print(f"❌ Error: {DEMAND_FILE} not found!")
        print("   Please run cleaning.py first to generate demand_processed.csv")
        exit(1)
    
    if not os.path.exists(SUPPLY_FILE):
        print(f"❌ Error: {SUPPLY_FILE} not found!")
        print("   Please run cleaning.py first to generate supply_processed.csv")
        exit(1)
    
    # Run analysis
    results = run_gap_analysis(DEMAND_FILE, SUPPLY_FILE)