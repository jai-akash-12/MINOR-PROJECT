"""
REAL-TIME DASHBOARD WITH LIVE DATA INTEGRATION
Updates automatically when attacks happen

Run this instead of the regular dashboard for live demos
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import time
import json
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parent.parent))

from utilities.config import LOGS_DIR

# Page config
st.set_page_config(
    page_title="AI Cyber Deception SOC - LIVE",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
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
    .live-indicator {
        display: inline-block;
        width: 12px;
        height: 12px;
        background-color: #ff0000;
        border-radius: 50%;
        animation: blink 1s infinite;
    }
    @keyframes blink {
        0%, 50% { opacity: 1; }
        51%, 100% { opacity: 0.3; }
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
    }
</style>
""", unsafe_allow_html=True)


def read_live_attacks(max_records=50):
    """Read attacks from live log file"""
    attack_log = LOGS_DIR / "attack_events.jsonl"
    
    attacks = []
    if attack_log.exists():
        try:
            with open(attack_log, 'r') as f:
                lines = f.readlines()
                for line in lines[-max_records:]:
                    try:
                        attack = json.loads(line)
                        attacks.append(attack)
                    except:
                        pass
        except:
            pass
    
    return attacks


def read_live_deceptions(max_records=50):
    """Read deception events from live log"""
    deception_log = LOGS_DIR / "deception_events.jsonl"
    
    deceptions = []
    if deception_log.exists():
        try:
            with open(deception_log, 'r') as f:
                lines = f.readlines()
                for line in lines[-max_records:]:
                    try:
                        deception = json.loads(line)
                        deceptions.append(deception)
                    except:
                        pass
        except:
            pass
    
    return deceptions


def calculate_live_metrics(attacks):
    """Calculate real-time metrics from attacks"""
    if not attacks:
        return {
            'total_attacks': 0,
            'active_threats': 0,
            'deception_rate': 0,
            'avg_threat_score': 0
        }
    
    recent_attacks = [a for a in attacks if (datetime.now() - datetime.fromisoformat(a['timestamp'])).seconds < 300]
    
    return {
        'total_attacks': len(attacks),
        'active_threats': len(recent_attacks),
        'deception_rate': sum(1 for a in attacks if a.get('deception_triggered', False)) / len(attacks) * 100,
        'avg_threat_score': sum(a.get('threat_score', 0) for a in attacks) / len(attacks)
    }


def create_live_network_graph(attacks):
    """Create network graph with real attacker IPs"""
    fig = go.Figure()
    
    # Your system (center)
    fig.add_trace(go.Scatter(
        x=[0], y=[0],
        mode='markers+text',
        name='Your System',
        text=['Your System'],
        textposition="top center",
        marker=dict(size=40, color='blue', symbol='square'),
        hovertext='Protected System'
    ))
    
    # Real attackers from logs
    if attacks:
        recent_attacks = attacks[-10:]  # Last 10 attacks
        unique_ips = list(set([a['source_ip'] for a in recent_attacks]))
        
        for i, ip in enumerate(unique_ips[:5]):  # Max 5 to avoid clutter
            angle = (i * 2 * np.pi / 5)
            x = 2 * np.cos(angle)
            y = 2 * np.sin(angle)
            
            # Count attacks from this IP
            attack_count = sum(1 for a in recent_attacks if a['source_ip'] == ip)
            
            fig.add_trace(go.Scatter(
                x=[x], y=[y],
                mode='markers+text',
                name=f'Attacker {i+1}',
                text=[f'{ip}'],
                textposition="top center",
                marker=dict(size=30, color='red'),
                hovertext=f'{ip}<br>Attacks: {attack_count}'
            ))
            
            # Draw connection line
            fig.add_trace(go.Scatter(
                x=[0, x], y=[0, y],
                mode='lines',
                line=dict(color='red', width=2, dash='dash'),
                showlegend=False,
                hoverinfo='none'
            ))
    
    fig.update_layout(
        title="Live Network Topology - Active Threats",
        showlegend=False,
        hovermode='closest',
        height=400,
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[-3, 3]),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[-3, 3]),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    
    return fig


def create_live_timeline(attacks):
    """Create timeline from real attacks"""
    if not attacks:
        return go.Figure()
    
    # Get last 20 attacks
    recent = attacks[-20:]
    
    df = pd.DataFrame([{
        'time': datetime.fromisoformat(a['timestamp']),
        'threat_score': a.get('threat_score', 0.5),
        'type': a['type']
    } for a in recent])
    
    fig = px.line(df, x='time', y='threat_score',
                  title='Real-Time Threat Score Timeline',
                  labels={'threat_score': 'Threat Score', 'time': 'Time'},
                  color='type')
    
    fig.add_hline(y=0.7, line_dash="dash", line_color="red",
                  annotation_text="Critical Threshold")
    
    fig.update_layout(height=300)
    
    return fig


def create_attack_type_distribution(attacks):
    """Create pie chart from real attack types"""
    if not attacks:
        return go.Figure()
    
    type_counts = {}
    for attack in attacks:
        attack_type = attack['type']
        type_counts[attack_type] = type_counts.get(attack_type, 0) + 1
    
    fig = px.pie(
        values=list(type_counts.values()),
        names=list(type_counts.keys()),
        title='Attack Type Distribution (Live Data)',
        color_discrete_sequence=px.colors.sequential.RdBu
    )
    
    fig.update_layout(height=300)
    
    return fig


def main():
    """Main dashboard with live data"""
    
    # Auto-refresh every 2 seconds
    if 'last_update' not in st.session_state:
        st.session_state.last_update = time.time()
    
    # Sidebar
    with st.sidebar:
        st.markdown('<h1 class="main-header">🛡️ SOC Control</h1>', unsafe_allow_html=True)
        st.markdown('<div style="text-align: center;"><span class="live-indicator"></span> <b>LIVE MODE</b></div>', unsafe_allow_html=True)
        st.markdown("---")
        
        page = st.radio(
            "Navigation",
            ["🔴 Live Monitor", "🎭 Attack Feed", "📊 Statistics"],
            label_visibility="collapsed"
        )
        
        st.markdown("---")
        st.markdown("### Auto-Refresh")
        auto_refresh = st.checkbox("Enable (2s)", value=True)
        
        if auto_refresh:
            st.write(f"Last update: {datetime.now().strftime('%H:%M:%S')}")
        
        st.markdown("---")
        
        # Live metrics
        attacks = read_live_attacks()
        metrics = calculate_live_metrics(attacks)
        
        st.markdown("### System Status")
        st.success("✅ Live Monitoring Active")
        st.metric("Total Attacks", metrics['total_attacks'])
        st.metric("Active Threats", metrics['active_threats'])
        st.metric("Deception Rate", f"{metrics['deception_rate']:.1f}%")
    
    # Main content
    if page == "🔴 Live Monitor":
        render_live_monitor()
    elif page == "🎭 Attack Feed":
        render_attack_feed()
    elif page == "📊 Statistics":
        render_statistics()
    
    # Auto-refresh
    if auto_refresh:
        time.sleep(2)
        st.rerun()


def render_live_monitor():
    """Live monitoring page"""
    st.markdown('<h1 class="main-header">🔴 Real-Time Threat Monitor <span class="live-indicator"></span></h1>', unsafe_allow_html=True)
    
    # Read live data
    attacks = read_live_attacks()
    metrics = calculate_live_metrics(attacks)
    
    # Top metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        delta = "+1" if metrics['active_threats'] > 0 else "0"
        st.metric("Active Threats", metrics['active_threats'], delta, delta_color="inverse")
    
    with col2:
        st.metric("Total Attacks", metrics['total_attacks'])
    
    with col3:
        st.metric("Deception Rate", f"{metrics['deception_rate']:.1f}%")
    
    with col4:
        st.metric("Avg Threat Score", f"{metrics['avg_threat_score']:.2f}")
    
    st.markdown("---")
    
    # Network topology and timeline
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.plotly_chart(create_live_network_graph(attacks), use_container_width=True)
    
    with col2:
        st.plotly_chart(create_live_timeline(attacks), use_container_width=True)
        st.plotly_chart(create_attack_type_distribution(attacks), use_container_width=True)


def render_attack_feed():
    """Real-time attack feed"""
    st.markdown('<h1 class="main-header">🎭 Live Attack Feed <span class="live-indicator"></span></h1>', unsafe_allow_html=True)
    
    attacks = read_live_attacks(100)
    
    if not attacks:
        st.info("No attacks detected yet. Waiting for activity...")
        st.markdown("**Try running an attack:**")
        st.code("nmap -p 1-1000 localhost")
        return
    
    # Show recent attacks
    st.markdown(f"### Last {len(attacks)} Attacks")
    
    # Create DataFrame
    attack_data = []
    for attack in reversed(attacks[-50:]):  # Most recent first
        attack_data.append({
            'Time': datetime.fromisoformat(attack['timestamp']).strftime('%H:%M:%S'),
            'Type': attack['type'],
            'Source IP': attack['source_ip'],
            'Target': attack['target'],
            'Threat Score': f"{attack['threat_score']:.2f}",
            'Severity': attack['severity'],
            'Deception': '✅' if attack.get('deception_triggered') else '❌'
        })
    
    df = pd.DataFrame(attack_data)
    
    # Color-code by severity
    def highlight_severity(row):
        if row['Severity'] == 'CRITICAL':
            return ['background-color: #ff4444'] * len(row)
        elif row['Severity'] == 'HIGH':
            return ['background-color: #ff8800'] * len(row)
        elif row['Severity'] == 'MEDIUM':
            return ['background-color: #ffaa00'] * len(row)
        else:
            return ['background-color: #00aa00'] * len(row)
    
    st.dataframe(df, use_container_width=True, hide_index=True)
    
    # Latest attack details
    if attacks:
        st.markdown("### Latest Attack Details")
        latest = attacks[-1]
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.json({
                'Timestamp': latest['timestamp'],
                'Type': latest['type'],
                'Source IP': latest['source_ip'],
                'Target': latest['target']
            })
        
        with col2:
            st.json({
                'Severity': latest['severity'],
                'Threat Score': latest['threat_score'],
                'Deception Triggered': latest.get('deception_triggered', False),
                'Details': latest.get('details', {})
            })


def render_statistics():
    """Statistics page"""
    st.markdown('<h1 class="main-header">📊 Live Statistics</h1>', unsafe_allow_html=True)
    
    attacks = read_live_attacks()
    deceptions = read_live_deceptions()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Attack Statistics")
        
        if attacks:
            # Attack types breakdown
            type_counts = {}
            for attack in attacks:
                type_counts[attack['type']] = type_counts.get(attack['type'], 0) + 1
            
            st.bar_chart(type_counts)
            
            # Severity breakdown
            severity_counts = {}
            for attack in attacks:
                severity_counts[attack['severity']] = severity_counts.get(attack['severity'], 0) + 1
            
            st.write("**By Severity:**")
            st.json(severity_counts)
        else:
            st.info("No attack data yet")
    
    with col2:
        st.markdown("### Deception Statistics")
        
        if deceptions:
            st.metric("Total Deception Events", len(deceptions))
            
            # Recent deceptions
            recent = deceptions[-10:]
            deception_data = [{
                'Time': datetime.fromisoformat(d['timestamp']).strftime('%H:%M:%S'),
                'Type': d.get('mutation_type', 'Unknown')
            } for d in recent]
            
            df = pd.DataFrame(deception_data)
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.info("No deception events yet")
    
    # Timeline of activity
    st.markdown("### Activity Timeline (Last Hour)")
    
    if attacks:
        now = datetime.now()
        hour_ago = now - timedelta(hours=1)
        
        recent_attacks = [a for a in attacks if datetime.fromisoformat(a['timestamp']) > hour_ago]
        
        if recent_attacks:
            times = [datetime.fromisoformat(a['timestamp']) for a in recent_attacks]
            types = [a['type'] for a in recent_attacks]
            
            df = pd.DataFrame({
                'Time': times,
                'Type': types,
                'Count': 1
            })
            
            # Group by minute
            df['Minute'] = df['Time'].dt.floor('T')
            grouped = df.groupby(['Minute', 'Type']).size().reset_index(name='Count')
            
            fig = px.bar(grouped, x='Minute', y='Count', color='Type',
                        title='Attacks per Minute')
            st.plotly_chart(fig, use_container_width=True)


if __name__ == "__main__":
    main()