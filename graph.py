"""
Skill Bundles Network Graph Visualization
Creates an interactive network graph of technical skill bundles
"""

import pandas as pd
import networkx as nx
import plotly.graph_objects as go
import matplotlib.pyplot as plt  # ← ADD THIS MISSING IMPORT
from plotly.subplots import make_subplots
import numpy as np

# ============================================================
# STEP 1: LOAD AND FILTER TECHNICAL SKILL BUNDLES
# ============================================================

def load_and_filter_technical_bundles(csv_file='skill_bundles_apriori.csv'):
    """Load and filter only technical skill bundles"""
    
    df = pd.read_csv(csv_file)
    
    # Technical skill keywords
    technical_keywords = [
        'Python', 'Java', 'JavaScript', 'TypeScript', 'C++', 'C#', 'Go', 'Ruby', 
        'PHP', 'Swift', 'Kotlin', 'R', 'Scala', 'Rust', 'React', 'Angular', 'Vue',
        'Django', 'Flask', 'Node.js', 'Spring', 'Laravel', 'ASP.NET', 'Express',
        'SQL', 'PostgreSQL', 'MySQL', 'MongoDB', 'Redis', 'Elasticsearch',
        'AWS', 'Azure', 'Google Cloud', 'Docker', 'Kubernetes', 'Terraform', 
        'Jenkins', 'CI/CD', 'Linux', 'Bash', 'Ansible', 'Prometheus', 'Grafana',
        'Machine Learning', 'Data Science', 'Pandas', 'NumPy', 'TensorFlow', 
        'PyTorch', 'Scikit-learn', 'Tableau', 'Power BI', 'REST APIs', 'GraphQL',
        'Microservices', 'Git', 'GitHub', 'GitLab', 'Cybersecurity', 'Firewalls',
        'Android', 'iOS', 'Flutter', 'React Native'
    ]
    
    def contains_technical(text):
        if pd.isna(text):
            return False
        text_lower = str(text).lower()
        for keyword in technical_keywords:
            if keyword.lower() in text_lower:
                return True
        return False
    
    # Filter
    technical_df = df[
        df['antecedents'].apply(contains_technical) | 
        df['consequents'].apply(contains_technical)
    ]
    
    # Keep only high-quality rules (lift > 1.5, support > 0.01)
    technical_df = technical_df[technical_df['lift'] > 1.5]
    technical_df = technical_df[technical_df['support'] > 0.01]
    
    # Sort by lift
    technical_df = technical_df.sort_values('lift', ascending=False)
    
    print(f"Loaded {len(technical_df)} technical skill bundles")
    print(f"Lift range: {technical_df['lift'].min():.2f} - {technical_df['lift'].max():.2f}")
    
    return technical_df


# ============================================================
# STEP 2: BUILD NETWORK GRAPH
# ============================================================

def build_skill_network(technical_df, max_rules=50):
    """
    Build a NetworkX graph from the skill bundle rules
    
    Args:
        technical_df: DataFrame with antecedents, consequents, lift, support
        max_rules: Maximum number of rules to include (for readability)
    """
    
    # Take top rules by lift
    top_rules = technical_df.head(max_rules)
    
    # Create graph
    G = nx.Graph()
    
    # Add edges with weights (lift)
    for idx, row in top_rules.iterrows():
        antecedents = str(row['antecedents']).split(', ')
        consequents = str(row['consequents']).split(', ')
        
        # Add edge between each antecedent and each consequent
        for ante in antecedents:
            for cons in consequents:
                if ante != cons:
                    # Use lift as weight
                    weight = row['lift']
                    support = row['support']
                    
                    if G.has_edge(ante, cons):
                        # If edge exists, take max lift
                        current_weight = G[ante][cons]['weight']
                        if weight > current_weight:
                            G[ante][cons]['weight'] = weight
                            G[ante][cons]['support'] = support
                    else:
                        G.add_edge(ante, cons, weight=weight, support=support)
    
    print(f"\nNetwork has {G.number_of_nodes()} skills and {G.number_of_edges()} connections")
    
    return G, top_rules


# ============================================================
# STEP 3: CREATE INTERACTIVE PLOTLY VISUALIZATION
# ============================================================

def create_network_visualization(G, top_rules):
    """
    Create an interactive Plotly network graph
    """
    
    # Get node positions using spring layout
    pos = nx.spring_layout(G, k=2, iterations=50, seed=42)
    
    # Create node traces
    node_x = []
    node_y = []
    node_text = []
    node_size = []
    node_color = []
    
    # Calculate node importance (degree centrality)
    degree_centrality = nx.degree_centrality(G)
    
    for node in G.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)
        
        # Node label
        node_text.append(node)
        
        # Node size based on degree (more connections = larger)
        size = 20 + (degree_centrality[node] * 50)
        node_size.append(size)
        
        # Node color based on skill category (inferred)
        node_color.append(get_skill_category(node))
    
    # Create edge traces
    edge_x = []
    edge_y = []
    edge_weights = []
    edge_text = []
    
    for edge in G.edges(data=True):
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        
        edge_x.append(x0)
        edge_x.append(x1)
        edge_x.append(None)
        
        edge_y.append(y0)
        edge_y.append(y1)
        edge_y.append(None)
        
        weight = edge[2].get('weight', 1)
        edge_weights.append(weight)
        edge_text.append(f"{edge[0]} ↔ {edge[1]}<br>Lift: {weight:.2f}")
    
    # Create edge trace (color based on lift strength)
    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=1.5, color='lightgray'),
        hoverinfo='text',
        text=edge_text,
        mode='lines'
    )
    
    # Create node trace
    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers+text',
        text=node_text,
        textposition="top center",
        hoverinfo='text',
        marker=dict(
            size=node_size,
            color=node_color,
            line=dict(width=2, color='white')
        ),
        textfont=dict(size=10)
    )
    
    # Create layout
    layout = go.Layout(
        title=dict(
            text="<b>Technical Skill Bundles Network</b><br><sub>Skills that appear together in job postings | Node size = connections | Edge strength = Lift</sub>",
            font=dict(size=16)
        ),
        showlegend=False,
        hovermode='closest',
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        width=1000,
        height=800,
        plot_bgcolor='white',
        annotations=[
            dict(
                text="Stronger connections (higher Lift) appear as thicker, darker edges",
                showarrow=False,
                xref="paper", yref="paper",
                x=0, y=-0.05
            )
        ]
    )
    
    fig = go.Figure(data=[edge_trace, node_trace], layout=layout)
    
    return fig


def get_skill_category(skill):
    """Assign color based on skill category"""
    
    # Programming Languages
    prog_langs = {'Python', 'Java', 'JavaScript', 'TypeScript', 'C++', 'C#', 'Go', 'Ruby', 'PHP', 'Swift', 'Kotlin', 'R', 'Scala', 'Rust'}
    if skill in prog_langs:
        return '#3498db'  # Blue
    
    # Web Frameworks
    web_frameworks = {'React', 'Angular', 'Vue', 'Django', 'Flask', 'Node.js', 'Spring', 'Laravel', 'ASP.NET', 'Express'}
    if skill in web_frameworks:
        return '#2ecc71'  # Green
    
    # Databases
    databases = {'SQL', 'PostgreSQL', 'MySQL', 'MongoDB', 'Redis', 'Elasticsearch'}
    if skill in databases:
        return '#e74c3c'  # Red
    
    # Cloud & DevOps
    cloud_devops = {'AWS', 'Azure', 'Google Cloud', 'Docker', 'Kubernetes', 'Terraform', 'Jenkins', 'CI/CD', 'Linux', 'Bash', 'Git'}
    if skill in cloud_devops:
        return '#f39c12'  # Orange
    
    # Data Science
    data_science = {'Machine Learning', 'Data Science', 'Pandas', 'NumPy', 'TensorFlow', 'PyTorch', 'Scikit-learn', 'Tableau', 'Power BI'}
    if skill in data_science:
        return '#9b59b6'  # Purple
    
    # Default
    return '#95a5a6'  # Gray


# ============================================================
# STEP 4: CREATE BAR CHART OF TOP SKILL BUNDLES
# ============================================================

def create_top_bundles_bar_chart(technical_df, n=15):
    """
    Create a horizontal bar chart of top skill bundles by lift
    """
    
    top_bundles = technical_df.head(n).copy()
    
    # Create readable labels
    labels = []
    for idx, row in top_bundles.iterrows():
        ante = str(row['antecedents'])[:20]
        cons = str(row['consequents'])[:20]
        if len(str(row['antecedents'])) > 20:
            ante += "..."
        if len(str(row['consequents'])) > 20:
            cons += "..."
        labels.append(f"{ante} → {cons}")
    
    # Create colors based on lift strength (using plotly colors, not matplotlib)
    fig = go.Figure(data=[
        go.Bar(
            x=top_bundles['lift'],
            y=labels,
            orientation='h',
            marker=dict(
                color=top_bundles['lift'],
                colorscale='Viridis',
                showscale=True,
                colorbar=dict(title="Lift")
            ),
            text=top_bundles['lift'].round(2),
            textposition='outside',
            hovertemplate='<b>%{y}</b><br>Lift: %{x:.2f}<br>Support: %{customdata:.3f}<extra></extra>',
            customdata=top_bundles['support']
        )
    ])
    
    fig.update_layout(
        title="<b>Top Technical Skill Bundles</b><br><sub>Higher Lift = Stronger association between skills</sub>",
        xaxis_title="Lift (Strength of Association)",
        yaxis_title="Skill Bundle (If X → Then Y)",
        height=600,
        width=900,
        font=dict(size=12)
    )
    
    return fig


# ============================================================
# STEP 5: CREATE FORCE-DIRECTED NETWORK (Alternative)
# ============================================================

def create_force_directed_network(G, top_rules):
    """
    Alternative network visualization with edge thickness based on lift
    """
    
    # Get positions
    pos = nx.spring_layout(G, k=1.5, iterations=50, seed=42)
    
    # Prepare edge data
    edge_x = []
    edge_y = []
    edge_widths = []
    
    # Calculate max lift for normalization
    max_lift = max([edge[2].get('weight', 1) for edge in G.edges(data=True)]) if G.edges() else 1
    
    for edge in G.edges(data=True):
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])
        
        # Width based on lift (normalized)
        lift = edge[2].get('weight', 1)
        width = 1 + (lift / max_lift) * 3
        edge_widths.append(width)
    
    # Create edge traces with varying width
    edge_traces = []
    
    # Group edges by width for separate traces
    unique_widths = set(edge_widths)
    for width in unique_widths:
        x_vals = []
        y_vals = []
        
        for edge in G.edges(data=True):
            lift = edge[2].get('weight', 1)
            edge_width = 1 + (lift / max_lift) * 3
            if abs(edge_width - width) < 0.1:  # Close enough
                x0, y0 = pos[edge[0]]
                x1, y1 = pos[edge[1]]
                x_vals.extend([x0, x1, None])
                y_vals.extend([y0, y1, None])
        
        if x_vals:
            edge_traces.append(
                go.Scatter(
                    x=x_vals, y=y_vals,
                    line=dict(width=width, color='rgba(150,150,150,0.5)'),
                    hoverinfo='none',
                    mode='lines'
                )
            )
    
    # Node trace
    node_x = [pos[node][0] for node in G.nodes()]
    node_y = [pos[node][1] for node in G.nodes()]
    node_text = list(G.nodes())
    
    degrees = dict(G.degree())
    node_sizes = [20 + degrees[node] * 5 for node in G.nodes()]
    
    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers+text',
        text=node_text,
        textposition="top center",
        marker=dict(
            size=node_sizes,
            color=[get_skill_category(node) for node in G.nodes()],
            line=dict(width=2, color='white')
        ),
        textfont=dict(size=11)
    )
    
    fig = go.Figure(data=edge_traces + [node_trace])
    fig.update_layout(
        title="<b>Skill Bundles Network (Force-Directed)</b>",
        showlegend=False,
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        width=1000,
        height=800,
        plot_bgcolor='white'
    )
    
    return fig


# ============================================================
# STEP 6: CREATE SKILL CLUSTER DETECTION
# ============================================================

def detect_skill_clusters(G):
    """
    Detect communities/clusters of skills using Louvain algorithm
    """
    try:
        import community.community_louvain as community_louvain
    except ImportError:
        print("Installing python-louvain for community detection...")
        import subprocess
        subprocess.check_call(['pip', 'install', 'python-louvain'])
        import community.community_louvain as community_louvain
    
    # Convert to undirected for community detection
    G_undirected = G.to_undirected()
    
    # Detect communities
    partition = community_louvain.best_partition(G_undirected)
    
    # Group nodes by community
    communities = {}
    for node, community_id in partition.items():
        if community_id not in communities:
            communities[community_id] = []
        communities[community_id].append(node)
    
    print("\n" + "=" * 60)
    print("DETECTED SKILL CLUSTERS (Communities)")
    print("=" * 60)
    
    for comm_id, skills in communities.items():
        print(f"\n📁 Cluster {comm_id + 1}: {', '.join(skills[:10])}")
        if len(skills) > 10:
            print(f"   ... and {len(skills) - 10} more skills")
    
    return communities


# ============================================================
# STEP 7: MAIN EXECUTION
# ============================================================

def main():
    """Run the complete skill bundles visualization pipeline"""
    
    print("=" * 70)
    print("TECHNICAL SKILL BUNDLES VISUALIZATION")
    print("=" * 70)
    
    # Load data
    print("\n📊 Loading skill bundles data...")
    technical_df = load_and_filter_technical_bundles('skill_bundles_apriori.csv')
    
    if len(technical_df) == 0:
        print("No technical bundles found. Check file path or filters.")
        return None, None, None
    
    # Build network
    print("\n🔗 Building skill network...")
    G, top_rules = build_skill_network(technical_df, max_rules=60)
    
    # Detect clusters
    print("\n🔍 Detecting skill communities...")
    communities = detect_skill_clusters(G)
    
    # Create visualizations
    print("\n📈 Creating visualizations...")
    
    # Visualization 1: Network graph
    fig1 = create_network_visualization(G, top_rules)
    fig1.write_html("skill_bundles_network.html")
    print("  ✓ Saved: skill_bundles_network.html")
    
    # Visualization 2: Bar chart
    fig2 = create_top_bundles_bar_chart(technical_df, n=15)
    fig2.write_html("top_skill_bundles_bar.html")
    print("  ✓ Saved: top_skill_bundles_bar.html")
    
    # Visualization 3: Force-directed network
    try:
        fig3 = create_force_directed_network(G, top_rules)
        fig3.write_html("skill_bundles_force_directed.html")
        print("  ✓ Saved: skill_bundles_force_directed.html")
    except Exception as e:
        print(f"  ⚠️ Could not create force-directed graph: {e}")
    
    # Save cluster results
    with open('skill_clusters.txt', 'w') as f:
        f.write("SKILL CLUSTERS FROM APRIORI BUNDLES\n")
        f.write("=" * 50 + "\n\n")
        for comm_id, skills in communities.items():
            f.write(f"Cluster {comm_id + 1}:\n")
            f.write(f"  Skills: {', '.join(skills)}\n\n")
    print("  ✓ Saved: skill_clusters.txt")
    
    # Print summary
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"  Total technical bundles: {len(technical_df)}")
    print(f"  Unique skills in network: {G.number_of_nodes()}")
    print(f"  Connections between skills: {G.number_of_edges()}")
    print(f"  Skill communities detected: {len(communities)}")
    
    print("\n" + "=" * 70)
    print("✅ VISUALIZATION COMPLETE!")
    print("   Open the .html files in your browser to explore the interactive graphs.")
    print("=" * 70)
    
    return technical_df, G, communities


# ============================================================
# RUN THE ANALYSIS
# ============================================================

if __name__ == "__main__":
    import plotly.io as pio
    pio.renderers.default = 'browser'
    
    # Optional: Install missing packages
    try:
        import networkx
    except ImportError:
        print("Installing networkx...")
        import subprocess
        subprocess.check_call(['pip', 'install', 'networkx'])
        import networkx
    
    technical_df, G, communities = main()
    
    if technical_df is not None:
        print("\n📊 First 5 technical skill bundles:")
        print(technical_df[['antecedents', 'consequents', 'lift', 'support']].head())
    else:
        print("\n⚠️ No data available. Please ensure skill_bundles_apriori.csv exists.")
    
    print("\n✅ Technical analysis completed.")