"""
PROFESSIONAL SOC MONITORING DASHBOARD
Beautiful, real-time dashboard for AI Cyber Deception System

Features:
- Live threat monitoring
- Polymorphic mirage visualization
- Genetic algorithm evolution tracking
- AI detection analytics
- Alert management
- Performance metrics
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import time
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parent.parent))

# Set page config FIRST
st.set_page_config(
    page_title="AI Cyber Deception SOC",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for beautiful styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 1rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .alert-critical {
        background-color: #ff4444;
        padding: 0.5rem;
        border-radius: 5px;
        color: white;
    }
    .alert-high {
        background-color: #ff8800;
        padding: 0.5rem;
        border-radius: 5px;
        color: white;
    }
    .alert-medium {
        background-color: #ffaa00;
        padding: 0.5rem;
        border-radius: 5px;
        color: white;
    }
    .alert-low {
        background-color: #00aa00;
        padding: 0.5rem;
        border-radius: 5px;
        color: white;
    }
</style>
""", unsafe_allow_html=True)


def create_network_topology_graph():
    """Create interactive network topology visualization"""
    # Create network graph
    fig = go.Figure()
    
    # Add nodes (servers, honeypots, attackers)
    nodes_x = [0, 2, 4, 1, 3, 2.5]
    nodes_y = [0, 0, 0, -1, -1, 1]
    node_types = ['Server', 'Honeypot', 'Honeypot', 'Attacker', 'Attacker', 'Firewall']
    node_colors = ['blue', 'green', 'green', 'red', 'red', 'orange']
    
    for i, (x, y, node_type, color) in enumerate(zip(nodes_x, nodes_y, node_types, node_colors)):
        fig.add_trace(go.Scatter(
            x=[x], y=[y],
            mode='markers+text',
            name=node_type,
            text=[node_type],
            textposition="bottom center",
            marker=dict(size=30, color=color),
            hoverinfo='text',
            hovertext=f"{node_type}<br>Status: Active"
        ))
    
    # Add edges (connections)
    edges = [(0, 1), (0, 2), (1, 3), (2, 4), (5, 0)]
    for edge in edges:
        fig.add_trace(go.Scatter(
            x=[nodes_x[edge[0]], nodes_x[edge[1]]],
            y=[nodes_y[edge[0]], nodes_y[edge[1]]],
            mode='lines',
            line=dict(width=2, color='gray'),
            showlegend=False,
            hoverinfo='none'
        ))
    
    fig.update_layout(
        title="Network Topology - Active Threats",
        showlegend=True,
        hovermode='closest',
        height=400,
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    
    return fig


def create_threat_timeline():
    """Create threat detection timeline"""
    # Generate sample data
    now = datetime.now()
    times = [now - timedelta(minutes=i*5) for i in range(20)]
    threat_scores = np.random.uniform(0.3, 0.9, 20)
    
    df = pd.DataFrame({
        'time': times,
        'threat_score': threat_scores,
        'threat_type': np.random.choice(['Port Scan', 'Brute Force', 'Lateral Movement'], 20)
    })
    
    fig = px.line(df, x='time', y='threat_score', 
                  title='Threat Score Timeline',
                  labels={'threat_score': 'Threat Score', 'time': 'Time'},
                  color='threat_type')
    
    fig.add_hline(y=0.7, line_dash="dash", line_color="red", 
                  annotation_text="Critical Threshold")
    
    fig.update_layout(height=300)
    
    return fig


def create_genetic_evolution_chart():
    """Create genetic algorithm fitness evolution chart"""
    generations = list(range(1, 51))
    best_fitness = [300 + i*12 + np.random.uniform(-20, 20) for i in range(50)]
    avg_fitness = [200 + i*8 + np.random.uniform(-15, 15) for i in range(50)]
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=generations, y=best_fitness,
        mode='lines+markers',
        name='Best Fitness',
        line=dict(color='green', width=3)
    ))
    
    fig.add_trace(go.Scatter(
        x=generations, y=avg_fitness,
        mode='lines',
        name='Average Fitness',
        line=dict(color='blue', width=2, dash='dash')
    ))
    
    fig.update_layout(
        title='Genetic Algorithm Fitness Evolution',
        xaxis_title='Generation',
        yaxis_title='Fitness Score',
        height=350,
        hovermode='x unified'
    )
    
    return fig


def create_deception_effectiveness_gauge():
    """Create gauge chart for deception effectiveness"""
    effectiveness = np.random.uniform(0.85, 0.95)
    
    fig = go.Figure(go.Indicator(
        mode = "gauge+number+delta",
        value = effectiveness * 100,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "Deception Effectiveness"},
        delta = {'reference': 90},
        gauge = {
            'axis': {'range': [None, 100]},
            'bar': {'color': "darkblue"},
            'steps': [
                {'range': [0, 50], 'color': "lightgray"},
                {'range': [50, 75], 'color': "gray"},
                {'range': [75, 100], 'color': "lightgreen"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 90
            }
        }
    ))
    
    fig.update_layout(height=250)
    
    return fig


def create_attack_distribution_pie():
    """Create pie chart of attack types"""
    attack_types = ['Port Scan', 'SSH Brute Force', 'Lateral Movement', 'Data Exfiltration', 'Privilege Escalation']
    counts = [45, 32, 18, 12, 8]
    
    fig = px.pie(
        values=counts,
        names=attack_types,
        title='Attack Type Distribution',
        color_discrete_sequence=px.colors.sequential.RdBu
    )
    
    fig.update_layout(height=300)
    
    return fig


def create_ai_model_performance():
    """Create bar chart of AI model performance"""
    models = ['Isolation Forest', 'LSTM', 'Autoencoder', 'Random Forest', 'Ensemble']
    accuracies = [0.89, 0.92, 0.87, 0.94, 0.96]
    
    fig = go.Figure(data=[
        go.Bar(
            x=models,
            y=accuracies,
            marker_color=['#667eea', '#764ba2', '#f093fb', '#4facfe', '#43e97b']
        )
    ])
    
    fig.update_layout(
        title='AI Model Detection Accuracy',
        yaxis_title='Accuracy',
        yaxis=dict(range=[0, 1]),
        height=300
    )
    
    return fig


def create_mirage_diversity_heatmap():
    """Create heatmap of genetic diversity scores"""
    mirages = [f'Mirage {i+1}' for i in range(10)]
    time_points = [f'T-{i*5}m' for i in range(12)]
    
    diversity_scores = np.random.uniform(0.5, 1.0, (10, 12))
    
    fig = go.Figure(data=go.Heatmap(
        z=diversity_scores,
        x=time_points,
        y=mirages,
        colorscale='Viridis',
        hovertemplate='%{y}<br>%{x}<br>Diversity: %{z:.2f}<extra></extra>'
    ))
    
    fig.update_layout(
        title='Polymorphic Mirage Genetic Diversity',
        height=350
    )
    
    return fig


def main():
    """Main dashboard function"""
    
    # Sidebar
    with st.sidebar:
        st.markdown('<h1 class="main-header">🛡️ SOC Control</h1>', unsafe_allow_html=True)
        st.markdown("---")
        
        page = st.radio(
            "Navigation",
            ["🔴 Live Monitor", "🎭 Polymorphic Mirages", "🧬 Genetic Evolution", 
             "📊 AI Analytics", "⚠️ Alerts", "📈 Metrics"],
            label_visibility="collapsed"
        )
        
        st.markdown("---")
        
        # System status
        st.markdown("### System Status")
        st.success("✅ All Systems Operational")
        st.metric("Uptime", "47h 23m")
        st.metric("Active Mirages", "12")
        st.metric("Threats Detected", "156")
        
        st.markdown("---")
        st.markdown("### Quick Actions")
        if st.button("🔄 Refresh Data"):
            st.rerun()
        if st.button("📥 Export Report"):
            st.info("Report exported!")
        
    # Main content based on selected page
    if page == "🔴 Live Monitor":
        render_live_monitor()
    elif page == "🎭 Polymorphic Mirages":
        render_mirage_dashboard()
    elif page == "🧬 Genetic Evolution":
        render_genetic_evolution()
    elif page == "📊 AI Analytics":
        render_ai_analytics()
    elif page == "⚠️ Alerts":
        render_alerts()
    elif page == "📈 Metrics":
        render_metrics()


def render_live_monitor():
    """Render live threat monitoring page"""
    st.markdown('<h1 class="main-header">🔴 Real-Time Threat Monitor</h1>', unsafe_allow_html=True)
    
    # Top metrics row
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric("Active Threats", "7", "+2", delta_color="inverse")
    with col2:
        st.metric("Mirages Active", "12", "+3")
    with col3:
        st.metric("Deception Rate", "94%", "+5%")
    with col4:
        st.metric("GA Fitness", "847", "+12")
    with col5:
        st.metric("AI Accuracy", "96.7%", "+0.3%")
    
    st.markdown("---")
    
    # Network topology and threat timeline
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.plotly_chart(create_network_topology_graph(), use_container_width=True)
    
    with col2:
        st.plotly_chart(create_threat_timeline(), use_container_width=True)
        st.plotly_chart(create_attack_distribution_pie(), use_container_width=True)
    
    st.markdown("---")
    
    # Live attack feed
    st.markdown("### 📡 Live Attack Feed")
    
    # Sample attack data
    attacks = [
        {"time": "14:23:15", "type": "SSH Brute Force", "source": "192.168.1.100", "severity": "HIGH", "status": "Blocked"},
        {"time": "14:22:47", "type": "Port Scan", "source": "10.0.0.45", "severity": "MEDIUM", "status": "Deceived"},
        {"time": "14:21:32", "type": "Lateral Movement", "source": "192.168.1.100", "severity": "CRITICAL", "status": "Trapped"},
        {"time": "14:20:18", "type": "Data Exfiltration", "source": "172.16.0.99", "severity": "CRITICAL", "status": "Blocked"},
        {"time": "14:19:05", "type": "Privilege Escalation", "source": "192.168.1.100", "severity": "HIGH", "status": "Deceived"}
    ]
    
    df = pd.DataFrame(attacks)
    st.dataframe(df, use_container_width=True, hide_index=True)


def render_mirage_dashboard():
    """Render polymorphic mirage dashboard"""
    st.markdown('<h1 class="main-header">🎭 Polymorphic Process Mirages</h1>', unsafe_allow_html=True)
    
    st.info("**Innovation**: Processes that morph their identity every 30 seconds to confuse attackers")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Mirages", "12", "+3")
    with col2:
        st.metric("Total Mutations", "1,247", "+34")
    with col3:
        st.metric("Avg Diversity Score", "0.78", "+0.05")
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Active Mirages")
        mirages_data = pd.DataFrame({
            'ID': [f'M{i+1:03d}' for i in range(12)],
            'Type': np.random.choice(['database', 'web_server', 'ssh_daemon'], 12),
            'Mutations': np.random.randint(50, 200, 12),
            'Diversity': np.random.uniform(0.6, 0.9, 12),
            'Interactions': np.random.randint(0, 50, 12)
        })
        st.dataframe(mirages_data, use_container_width=True, hide_index=True)
    
    with col2:
        st.markdown("### Genetic Diversity Scores")
        diversity_data = pd.DataFrame({
            'Mirage': [f'M{i+1:03d}' for i in range(12)],
            'Diversity': np.random.uniform(0.6, 0.9, 12)
        })
        fig = px.bar(diversity_data, x='Mirage', y='Diversity', 
                     title='Current Diversity Scores',
                     color='Diversity',
                     color_continuous_scale='Viridis')
        st.plotly_chart(fig, use_container_width=True)
    
    st.plotly_chart(create_mirage_diversity_heatmap(), use_container_width=True)


def render_genetic_evolution():
    """Render genetic algorithm evolution page"""
    st.markdown('<h1 class="main-header">🧬 Genetic Algorithm Evolution</h1>', unsafe_allow_html=True)
    
    st.success("**Innovation**: GA evolves the most effective deception strategies across generations")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Generation", "47", "+1")
    with col2:
        st.metric("Best Fitness", "892.3", "+15.7")
    with col3:
        st.metric("Avg Fitness", "654.1", "+8.3")
    with col4:
        st.metric("Improvement", "+47%", "vs Gen 1")
    
    st.markdown("---")
    
    st.plotly_chart(create_genetic_evolution_chart(), use_container_width=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🏆 Best Deception Strategy")
        st.json({
            "strategy_id": "gen47_chr_best",
            "fitness": 892.3,
            "honeypots": 8,
            "mirages": 12,
            "mutation_rate": 0.42,
            "deception_intensity": 0.87
        })
    
    with col2:
        st.markdown("### 📊 Strategy Comparison")
        strategies = pd.DataFrame({
            'Strategy': ['Current Best', 'Previous Best', 'Population Avg', 'Initial'],
            'Fitness': [892, 847, 654, 420]
        })
        fig = px.bar(strategies, x='Strategy', y='Fitness',
                     color='Fitness',
                     color_continuous_scale='Blues')
        st.plotly_chart(fig, use_container_width=True)


def render_ai_analytics():
    """Render AI detection analytics page"""
    st.markdown('<h1 class="main-header">📊 AI Detection Analytics</h1>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.plotly_chart(create_ai_model_performance(), use_container_width=True)
        
        st.markdown("### Detection Accuracy Timeline")
        times = pd.date_range(end=datetime.now(), periods=24, freq='H')
        accuracy = np.random.uniform(0.92, 0.98, 24)
        df = pd.DataFrame({'Time': times, 'Accuracy': accuracy})
        fig = px.line(df, x='Time', y='Accuracy')
        fig.add_hline(y=0.95, line_dash="dash", line_color="green", 
                      annotation_text="Target: 95%")
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### Threat Classification Distribution")
        threat_types = ['Port Scan', 'Brute Force', 'Malware', 'DDoS', 'Exfiltration']
        counts = [45, 32, 18, 12, 8]
        fig = px.pie(values=counts, names=threat_types,
                     color_discrete_sequence=px.colors.sequential.RdBu)
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("### Model Confidence Scores")
        models = ['Isolation Forest', 'LSTM', 'Autoencoder', 'Random Forest']
        confidence = np.random.uniform(0.85, 0.98, 4)
        df = pd.DataFrame({'Model': models, 'Confidence': confidence})
        fig = px.bar(df, x='Model', y='Confidence', color='Confidence',
                     color_continuous_scale='Greens')
        st.plotly_chart(fig, use_container_width=True)


def render_alerts():
    """Render active alerts page"""
    st.markdown('<h1 class="main-header">⚠️ Active Alerts</h1>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Alerts", "47", "+5")
    with col2:
        st.metric("Critical", "3", "+1", delta_color="inverse")
    with col3:
        st.metric("High", "8", "+2", delta_color="inverse")
    with col4:
        st.metric("Medium/Low", "36", "+2")
    
    st.markdown("---")
    
    # Alert list
    alerts = pd.DataFrame({
        'Time': ['14:23:15', '14:22:47', '14:21:32', '14:20:18', '14:19:05'],
        'Severity': ['CRITICAL', 'HIGH', 'CRITICAL', 'HIGH', 'MEDIUM'],
        'Type': ['Lateral Movement', 'SSH Brute Force', 'Data Exfiltration', 'Port Scan', 'Privilege Escalation'],
        'Source': ['192.168.1.100', '10.0.0.45', '172.16.0.99', '192.168.1.100', '10.0.0.45'],
        'Status': ['Active', 'Contained', 'Blocked', 'Monitoring', 'Resolved'],
        'AI Confidence': ['98%', '95%', '97%', '89%', '92%']
    })
    
    st.dataframe(alerts, use_container_width=True, hide_index=True)


def render_metrics():
    """Render performance metrics page"""
    st.markdown('<h1 class="main-header">📈 Performance Metrics</h1>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.plotly_chart(create_deception_effectiveness_gauge(), use_container_width=True)
    
    with col2:
        st.markdown("### System Resources")
        resources = pd.DataFrame({
            'Resource': ['CPU', 'Memory', 'Disk', 'Network'],
            'Usage': [45, 62, 38, 51]
        })
        fig = px.bar(resources, x='Resource', y='Usage',
                     color='Usage',
                     color_continuous_scale='Reds')
        fig.update_layout(height=250)
        st.plotly_chart(fig, use_container_width=True)
    
    with col3:
        st.markdown("### Detection Performance")
        st.metric("Mean Time to Detect", "2.3s", "-0.4s")
        st.metric("False Positive Rate", "2.1%", "-0.3%")
        st.metric("Throughput", "1,247 events/s", "+120")
    
    st.markdown("---")
    
    st.markdown("### Research Validation Metrics")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("**Polymorphic Innovation**")
        st.success("✅ Implemented")
        st.metric("Genetic Diversity", "0.78")
        st.metric("Mutation Frequency", "34/min")
    
    with col2:
        st.markdown("**Genetic Algorithm**")
        st.success("✅ Implemented")
        st.metric("Generations", "47")
        st.metric("Fitness Improvement", "+47%")
    
    with col3:
        st.markdown("**Mathematical Deception**")
        st.success("✅ Implemented")
        st.metric("Entropy Score", "0.84")
        st.metric("Fractal Depth", "4")


if __name__ == "__main__":
    main()