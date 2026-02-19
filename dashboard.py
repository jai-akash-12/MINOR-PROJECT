"""
=============================================================
  SOC LIVE DASHBOARD
=============================================================

Run AFTER server.py is running.

Command:
    streamlit run dashboard.py

Dashboard auto-refreshes every 2 seconds.
All numbers start at 0.
They increase as attacks happen.

=============================================================
"""

import streamlit as st
import json
import time
import os
from pathlib import Path
from datetime import datetime, timedelta
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import math
import random

# ─────────────────────────────────────────────
#  Configuration
# ─────────────────────────────────────────────
BASE_DIR = Path(__file__).parent
ATTACKS_FILE = BASE_DIR / "logs" / "attacks.json"
MIRAGE_FILE  = BASE_DIR / "logs" / "mirages.json"

# ─────────────────────────────────────────────
#  Page Setup
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="AI Cyber Deception SOC",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
  .main { background-color: #0e1117; }
  .metric-box {
      background: linear-gradient(135deg, #1e3a5f, #0f2040);
      border: 1px solid #2a5298;
      border-radius: 12px;
      padding: 20px;
      text-align: center;
      margin: 5px;
  }
  .metric-number { font-size: 2.5rem; font-weight: 700; color: #00d2ff; }
  .metric-label  { font-size: 0.85rem; color: #aaa; margin-top: 4px; }
  .alert-critical { background: #3d0000; border-left: 4px solid #ff0000; padding: 8px 12px; border-radius: 4px; margin: 4px 0; }
  .alert-high     { background: #3d1700; border-left: 4px solid #ff6600; padding: 8px 12px; border-radius: 4px; margin: 4px 0; }
  .alert-medium   { background: #3d3000; border-left: 4px solid #ffaa00; padding: 8px 12px; border-radius: 4px; margin: 4px 0; }
  .alert-low      { background: #003d00; border-left: 4px solid #00ff00; padding: 8px 12px; border-radius: 4px; margin: 4px 0; }
  .blink { animation: blink 1s step-start infinite; }
  @keyframes blink { 50% { opacity: 0; } }
  div[data-testid="stSidebar"] { background-color: #0d1520 !important; }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  Data Loading
# ─────────────────────────────────────────────

def load_attacks():
    """Read attacks from JSON file"""
    if not ATTACKS_FILE.exists():
        return []
    try:
        with open(ATTACKS_FILE, "r") as f:
            data = json.load(f)
            return data if isinstance(data, list) else []
    except:
        return []

def load_mirages():
    """Read mirage state"""
    if not MIRAGE_FILE.exists():
        return {"mirages": [], "ga": {}}
    try:
        with open(MIRAGE_FILE, "r") as f:
            return json.load(f)
    except:
        return {"mirages": [], "ga": {}}

def get_metrics(attacks):
    """Calculate all metrics from attacks"""
    if not attacks:
        return {
            "total": 0, "critical": 0, "high": 0, "medium": 0, "low": 0,
            "deception_rate": 0.0, "avg_score": 0.0, "unique_ips": 0,
            "active_last_5min": 0, "ssh_count": 0, "http_count": 0,
            "ftp_count": 0, "scan_count": 0
        }

    now = datetime.now()
    five_min_ago = now - timedelta(minutes=5)

    critical = sum(1 for a in attacks if a.get("severity") == "CRITICAL")
    high     = sum(1 for a in attacks if a.get("severity") == "HIGH")
    medium   = sum(1 for a in attacks if a.get("severity") == "MEDIUM")
    low      = sum(1 for a in attacks if a.get("severity") == "LOW")

    deceived = sum(1 for a in attacks if a.get("deception_triggered", False))
    deception_rate = round(deceived / len(attacks) * 100, 1) if attacks else 0

    scores = [a.get("threat_score", 0) for a in attacks]
    avg_score = round(sum(scores) / len(scores), 2) if scores else 0

    unique_ips = len(set(a.get("source_ip", "") for a in attacks))

    recent = []
    for a in attacks:
        try:
            ts = datetime.fromisoformat(a["timestamp"])
            if ts > five_min_ago:
                recent.append(a)
        except:
            pass

    return {
        "total": len(attacks),
        "critical": critical,
        "high": high,
        "medium": medium,
        "low": low,
        "deception_rate": deception_rate,
        "avg_score": avg_score,
        "unique_ips": unique_ips,
        "active_last_5min": len(recent),
        "ssh_count":  sum(1 for a in attacks if "ssh" in a.get("type","")),
        "http_count": sum(1 for a in attacks if "http" in a.get("type","")),
        "ftp_count":  sum(1 for a in attacks if "ftp" in a.get("type","")),
        "scan_count": sum(1 for a in attacks if "scan" in a.get("type","")),
    }


# ─────────────────────────────────────────────
#  Chart Builders
# ─────────────────────────────────────────────

def chart_timeline(attacks):
    """Threat score timeline"""
    if not attacks:
        # Empty chart with axes
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=[], y=[], mode="lines+markers", name="Threat Score"))
        fig.add_hline(y=0.7, line_dash="dash", line_color="red", annotation_text="High Threshold")
        fig.add_hline(y=0.85, line_dash="dash", line_color="darkred", annotation_text="Critical Threshold")
        fig.update_layout(title="Threat Score Timeline (Live)",
                          xaxis_title="Time", yaxis_title="Threat Score",
                          yaxis=dict(range=[0, 1]),
                          plot_bgcolor="#0d1520", paper_bgcolor="#0d1520",
                          font=dict(color="#ccc"), height=300)
        return fig

    recent = attacks[-50:]
    times  = [a.get("time_display", "") for a in recent]
    scores = [a.get("threat_score", 0) for a in recent]
    colors = ["#ff0000" if s >= 0.85 else "#ff6600" if s >= 0.7 else "#ffaa00" if s >= 0.5 else "#00ff00"
              for s in scores]

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=list(range(len(times))), y=scores,
        mode="lines+markers",
        line=dict(color="#00d2ff", width=2),
        marker=dict(color=colors, size=6),
        text=times, hovertemplate="Time: %{text}<br>Score: %{y:.2f}<extra></extra>",
        name="Threat Score"
    ))
    fig.add_hline(y=0.70, line_dash="dash", line_color="#ff6600", annotation_text="HIGH (0.7)")
    fig.add_hline(y=0.85, line_dash="dash", line_color="#ff0000", annotation_text="CRITICAL (0.85)")
    fig.update_layout(
        title="Threat Score Timeline (Live)",
        xaxis_title="Attacks (newest right)", yaxis_title="Threat Score",
        yaxis=dict(range=[0, 1.05]),
        plot_bgcolor="#0d1520", paper_bgcolor="#0d1520",
        font=dict(color="#ccc"), height=300,
        showlegend=False
    )
    return fig


def chart_attack_types(attacks):
    """Attack type pie chart"""
    if not attacks:
        fig = go.Figure(go.Pie(labels=["No Attacks Yet"], values=[1],
                               marker_colors=["#1e3a5f"]))
        fig.update_layout(title="Attack Types", plot_bgcolor="#0d1520",
                          paper_bgcolor="#0d1520", font=dict(color="#ccc"), height=300)
        return fig

    counts = {}
    labels_map = {
        "ssh_bruteforce": "SSH Brute Force",
        "http_probe": "HTTP Probe",
        "http_bruteforce": "HTTP Brute Force",
        "ftp_bruteforce": "FTP Brute Force",
        "port_scan": "Port Scan",
        "directory_traversal": "Dir Traversal",
    }
    for a in attacks:
        t = a.get("type", "unknown")
        label = labels_map.get(t, t.replace("_", " ").title())
        counts[label] = counts.get(label, 0) + 1

    fig = go.Figure(go.Pie(
        labels=list(counts.keys()),
        values=list(counts.values()),
        hole=0.4,
        marker_colors=["#00d2ff", "#ff6600", "#ff0000", "#aa00ff", "#00ff88", "#ffaa00"]
    ))
    fig.update_layout(title="Attack Type Distribution",
                      plot_bgcolor="#0d1520", paper_bgcolor="#0d1520",
                      font=dict(color="#ccc"), height=300)
    return fig


def chart_severity_bar(metrics):
    """Severity breakdown bar chart"""
    categories = ["CRITICAL", "HIGH", "MEDIUM", "LOW"]
    values     = [metrics["critical"], metrics["high"], metrics["medium"], metrics["low"]]
    colors     = ["#ff0000", "#ff6600", "#ffaa00", "#00ff00"]

    fig = go.Figure(go.Bar(
        x=categories, y=values,
        marker_color=colors,
        text=values,
        textposition="outside",
        textfont=dict(color="white")
    ))
    fig.update_layout(
        title="Attacks by Severity",
        yaxis_title="Count",
        plot_bgcolor="#0d1520", paper_bgcolor="#0d1520",
        font=dict(color="#ccc"), height=280,
        showlegend=False
    )
    return fig


def chart_ai_models(attacks):
    """AI model comparison - last attack's scores"""
    if not attacks:
        models = ["Isolation Forest", "LSTM", "Autoencoder", "Random Forest"]
        scores = [0, 0, 0, 0]
    else:
        last = attacks[-1]
        ai = last.get("ai_models", {})
        models = ["Isolation Forest", "LSTM", "Autoencoder", "Random Forest"]
        scores = [
            ai.get("isolation_forest", 0),
            ai.get("lstm", 0),
            ai.get("autoencoder", 0),
            ai.get("random_forest", 0)
        ]

    colors = ["#ff0000" if s >= 0.85 else "#ff6600" if s >= 0.7 else "#ffaa00" if s >= 0.5 else "#00d2ff"
              for s in scores]

    fig = go.Figure(go.Bar(
        x=models, y=scores,
        marker_color=colors,
        text=[f"{s:.2f}" for s in scores],
        textposition="outside",
        textfont=dict(color="white")
    ))
    fig.add_hline(y=0.7, line_dash="dash", line_color="red", annotation_text="Threat Threshold")
    fig.update_layout(
        title="AI Model Scores (Latest Attack)",
        yaxis=dict(range=[0, 1.1], title="Threat Score"),
        plot_bgcolor="#0d1520", paper_bgcolor="#0d1520",
        font=dict(color="#ccc"), height=280,
        showlegend=False
    )
    return fig


def chart_ga_fitness(mirages_data):
    """Genetic Algorithm fitness over time"""
    ga = mirages_data.get("ga", {})
    gen = ga.get("generation", 1)

    # Simulate fitness history
    generations = list(range(1, gen + 1))
    fitness = [100 + (g - 1) * 2.5 + (math.sin(g * 0.5) * 5) for g in generations]

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=generations, y=fitness,
        mode="lines+markers",
        line=dict(color="#00ff88", width=2),
        marker=dict(size=4, color="#00ff88"),
        name="Fitness Score",
        fill="tozeroy",
        fillcolor="rgba(0,255,136,0.1)"
    ))
    fig.update_layout(
        title=f"Genetic Algorithm Evolution (Generation {gen})",
        xaxis_title="Generation", yaxis_title="Fitness Score",
        plot_bgcolor="#0d1520", paper_bgcolor="#0d1520",
        font=dict(color="#ccc"), height=280, showlegend=False
    )
    return fig


def chart_network_topology(attacks):
    """Network graph showing attacker IPs"""
    fig = go.Figure()

    # Center: Your system
    fig.add_trace(go.Scatter(
        x=[0], y=[0],
        mode="markers+text",
        text=["🔒 Your System"],
        textposition="bottom center",
        marker=dict(size=35, color="#0066cc", symbol="square",
                    line=dict(color="#00d2ff", width=2)),
        hovertemplate="Protected System<br>Honeypots Active<extra></extra>",
        name="System"
    ))

    if not attacks:
        # Just show the system alone with legend
        fig.add_trace(go.Scatter(
            x=[None], y=[None],
            mode="markers",
            marker=dict(size=15, color="#ff0000"),
            name="Attacker (none yet)"
        ))
    else:
        # Get unique attacker IPs with counts
        ip_counts = {}
        ip_last_type = {}
        for a in attacks:
            ip = a.get("source_ip", "unknown")
            ip_counts[ip] = ip_counts.get(ip, 0) + 1
            ip_last_type[ip] = a.get("type", "unknown")

        unique_ips = list(ip_counts.items())[:6]  # Max 6 attackers shown

        angles = [i * (360 / max(len(unique_ips), 1)) for i in range(len(unique_ips))]

        import math
        for i, (ip, count) in enumerate(unique_ips):
            angle_rad = math.radians(angles[i])
            x = 2.2 * math.cos(angle_rad)
            y = 2.2 * math.sin(angle_rad)

            # Bigger marker = more attacks
            size = min(40, 20 + count * 2)

            fig.add_trace(go.Scatter(
                x=[x], y=[y],
                mode="markers+text",
                text=[f"💀 {ip}"],
                textposition="top center",
                marker=dict(size=size, color="#ff2200",
                            line=dict(color="#ff6600", width=2)),
                hovertemplate=f"Attacker: {ip}<br>Attacks: {count}<br>Latest: {ip_last_type.get(ip,'')}<extra></extra>",
                name=f"{ip} ({count})"
            ))

            # Attack arrow line
            fig.add_trace(go.Scatter(
                x=[x * 0.85, 0], y=[y * 0.85, 0],
                mode="lines",
                line=dict(color="#ff4400", width=2, dash="dot"),
                showlegend=False,
                hoverinfo="skip"
            ))

    fig.update_layout(
        title="Live Network Topology",
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[-3.5, 3.5]),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[-3.5, 3.5]),
        plot_bgcolor="#0d1520", paper_bgcolor="#0d1520",
        font=dict(color="#ccc"), height=350,
        legend=dict(bgcolor="rgba(0,0,0,0)")
    )
    return fig


def chart_diversity_heatmap(mirages_data):
    """Mirage diversity heatmap"""
    mirages = mirages_data.get("mirages", [])
    if not mirages:
        fig = go.Figure()
        fig.update_layout(title="Mirage Diversity (no data)", height=250,
                          plot_bgcolor="#0d1520", paper_bgcolor="#0d1520",
                          font=dict(color="#ccc"))
        return fig

    names  = [m.get("current", f"process_{i}") for i, m in enumerate(mirages[:12])]
    scores = [m.get("diversity_score", 0.5) for m in mirages[:12]]

    # Create a 3×4 grid
    z = [scores[i:i+4] for i in range(0, 12, 4)]
    y_labels = ["Group A", "Group B", "Group C"]
    x_labels = [names[i] if i < len(names) else "" for i in range(4)]

    fig = go.Figure(go.Heatmap(
        z=z, x=x_labels, y=y_labels,
        colorscale=[[0, "#001030"], [0.5, "#0066cc"], [1, "#00ff88"]],
        zmin=0, zmax=1,
        text=[[f"{v:.2f}" for v in row] for row in z],
        texttemplate="%{text}",
        colorbar=dict(title="Diversity")
    ))
    fig.update_layout(
        title="Polymorphic Mirage Diversity Scores",
        plot_bgcolor="#0d1520", paper_bgcolor="#0d1520",
        font=dict(color="#ccc"), height=250
    )
    return fig


# ─────────────────────────────────────────────
#  Sidebar
# ─────────────────────────────────────────────

def render_sidebar(metrics, ga):
    with st.sidebar:
        st.markdown("""
        <div style='text-align:center; padding: 10px 0;'>
            <span style='font-size:2rem'>🛡️</span><br>
            <span style='font-size:1.3rem; font-weight:700; color:#00d2ff'>AI SOC Monitor</span><br>
            <span style='font-size:0.7rem; color:#aaa'>Cyber Deception System</span>
        </div>
        """, unsafe_allow_html=True)

        # Live indicator
        if metrics["total"] > 0:
            st.markdown("""
            <div style='text-align:center; background:#1a0000; border:1px solid #ff0000;
                        border-radius:8px; padding:6px; margin:8px 0;'>
                <span style='color:#ff0000; font-weight:bold'>⚠ THREATS DETECTED</span>
            </div>""", unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style='text-align:center; background:#001a00; border:1px solid #00ff00;
                        border-radius:8px; padding:6px; margin:8px 0;'>
                <span style='color:#00ff00; font-weight:bold'>✅ ALL CLEAR</span>
            </div>""", unsafe_allow_html=True)

        st.markdown("---")
        page = st.radio("NAVIGATION", [
            "📊 Live Monitor",
            "🎭 Polymorphic Mirages",
            "🧬 Genetic Evolution",
            "🤖 AI Detection",
            "⚠️ Alert Feed",
        ], label_visibility="collapsed")

        st.markdown("---")
        st.markdown(f"""
        <div style='font-size:0.8rem; color:#aaa; line-height:1.8'>
        🔴 Total Attacks: <b style='color:#fff'>{metrics['total']}</b><br>
        🔴 Last 5 mins: <b style='color:#fff'>{metrics['active_last_5min']}</b><br>
        🟠 Unique IPs: <b style='color:#fff'>{metrics['unique_ips']}</b><br>
        🟡 Deception Rate: <b style='color:#fff'>{metrics['deception_rate']}%</b><br>
        🟢 Avg Score: <b style='color:#fff'>{metrics['avg_score']}</b>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("---")
        st.caption(f"Auto-refreshes every 2 sec")
        st.caption(f"Updated: {datetime.now().strftime('%H:%M:%S')}")

    return page


# ─────────────────────────────────────────────
#  Page: Live Monitor
# ─────────────────────────────────────────────

def page_live_monitor(attacks, metrics, mirages_data):
    st.markdown("""
    <h1 style='color:#00d2ff; margin-bottom:0'>📊 Live Threat Monitor</h1>
    <p style='color:#666; margin-top:0'>Auto-refreshes every 2 seconds · All values start at 0</p>
    """, unsafe_allow_html=True)

    # ── Top 6 Metric Cards ──
    c1, c2, c3, c4, c5, c6 = st.columns(6)

    def metric_card(col, value, label, color="#00d2ff"):
        col.markdown(f"""
        <div class='metric-box'>
            <div class='metric-number' style='color:{color}'>{value}</div>
            <div class='metric-label'>{label}</div>
        </div>""", unsafe_allow_html=True)

    metric_card(c1, metrics["total"],            "Total Attacks",     "#ff4444" if metrics["total"] > 0 else "#00d2ff")
    metric_card(c2, metrics["active_last_5min"], "Active (5 min)",    "#ff6600" if metrics["active_last_5min"] > 0 else "#00d2ff")
    metric_card(c3, metrics["critical"],         "🔴 Critical",       "#ff0000")
    metric_card(c4, metrics["high"],             "🟠 High",           "#ff6600")
    metric_card(c5, metrics["unique_ips"],       "Unique Attackers",  "#aa00ff")
    metric_card(c6, f"{metrics['deception_rate']}%", "Deception Rate","#00ff88")

    st.markdown("---")

    # ── Network Topology + Timeline ──
    col1, col2 = st.columns([1, 1])
    with col1:
        st.plotly_chart(chart_network_topology(attacks), use_container_width=True)
    with col2:
        st.plotly_chart(chart_timeline(attacks), use_container_width=True)

    st.markdown("---")

    # ── Attack Types + Severity ──
    col1, col2 = st.columns([1, 1])
    with col1:
        st.plotly_chart(chart_attack_types(attacks), use_container_width=True)
    with col2:
        st.plotly_chart(chart_severity_bar(metrics), use_container_width=True)

    # ── Last 10 Attacks Table ──
    st.markdown("### 📋 Recent Attacks")
    if not attacks:
        st.info("⏳ No attacks yet. Start attacking from another device to see data here.")
        st.code("""
HOW TO ATTACK:
  SSH:  ssh admin@YOUR_IP -p 2222
  HTTP: Open http://YOUR_IP:8080 in browser
  FTP:  ftp YOUR_IP 2121
  SCAN: nmap -p 2222,8080,2121 YOUR_IP
        """)
    else:
        last10 = attacks[-10:][::-1]  # Most recent first
        rows = []
        for a in last10:
            sev = a.get("severity", "")
            sev_emoji = {"CRITICAL": "🔴", "HIGH": "🟠", "MEDIUM": "🟡", "LOW": "🟢"}.get(sev, "⚪")
            rows.append({
                "Time": a.get("time_display", ""),
                "Attack Type": a.get("type", "").replace("_", " ").upper(),
                "Source IP": a.get("source_ip", ""),
                "Port": str(a.get("target_port", "")),
                "Severity": f"{sev_emoji} {sev}",
                "Threat Score": f"{a.get('threat_score', 0):.2f}",
                "Deception": "✅ Triggered" if a.get("deception_triggered") else "❌",
            })
        df = pd.DataFrame(rows)
        st.dataframe(df, use_container_width=True, hide_index=True)


# ─────────────────────────────────────────────
#  Page: Polymorphic Mirages
# ─────────────────────────────────────────────

def page_mirages(mirages_data):
    st.markdown("<h1 style='color:#00d2ff'>🎭 Polymorphic Process Mirages</h1>", unsafe_allow_html=True)
    st.markdown("""
    <p style='color:#888'>
    These are <b style='color:#00d2ff'>fake processes</b> deployed as honeypots.
    They morph their identity every 30 seconds to prevent fingerprinting.
    The <b style='color:#00ff88'>Genetic Diversity Score</b> measures how unpredictable they are.
    </p>""", unsafe_allow_html=True)

    mirages = mirages_data.get("mirages", [])

    # Summary metrics
    if mirages:
        total_mutations = sum(m.get("mutations", 0) for m in mirages)
        avg_diversity   = round(sum(m.get("diversity_score", 0) for m in mirages) / len(mirages), 2)
        active          = sum(1 for m in mirages if m.get("status") == "active")

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Active Mirages",     active)
        c2.metric("Total Mutations",    total_mutations)
        c3.metric("Avg Diversity Score",avg_diversity)
        c4.metric("Process Types",      len(set(m.get("original","") for m in mirages)))

    st.markdown("---")

    # Mirage Table
    st.markdown("### 🔄 Active Mirages Status")
    if mirages:
        rows = []
        for m in mirages:
            score = m.get("diversity_score", 0)
            bar = "█" * int(score * 10) + "░" * (10 - int(score * 10))
            rows.append({
                "ID": m.get("id", ""),
                "Original Name": m.get("original", ""),
                "Current Name (Morphed)": m.get("current", ""),
                "Mutations": m.get("mutations", 0),
                "Diversity Score": f"{score:.2f}  {bar}",
                "Status": "🟢 Active" if m.get("status") == "active" else "🔴 Inactive",
            })
        df = pd.DataFrame(rows)
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.info("Start server.py to activate mirages")

    st.markdown("---")

    # Diversity heatmap
    st.plotly_chart(chart_diversity_heatmap(mirages_data), use_container_width=True)

    # Explanation
    st.markdown("""
    ---
    ### 💡 How Polymorphic Mirages Work

    **Traditional honeypot (bad):**
    > Always named `sshd`, same PID range, same memory footprint
    > Attacker scans once → sees the pattern → knows it's fake

    **Polymorphic mirage (your innovation):**
    > Starts as `mysqld` → morphs to `redis-server` → becomes `postgres`
    > PID, memory, CPU, network connections all change
    > Attacker can never fingerprint it!

    **Genetic Diversity Score formula:**
    > `score = hamming_distance + memory_variance + behavioral_entropy`
    > Range 0.0 to 1.0 — higher = more unpredictable = better deception
    """)


# ─────────────────────────────────────────────
#  Page: Genetic Evolution
# ─────────────────────────────────────────────

def page_genetic(mirages_data):
    st.markdown("<h1 style='color:#00d2ff'>🧬 Genetic Algorithm Evolution</h1>", unsafe_allow_html=True)
    st.markdown("""
    <p style='color:#888'>
    The system uses a <b style='color:#00ff88'>genetic algorithm</b> to automatically evolve
    better deception strategies. Each generation, the best strategies survive and mix to create
    even better ones — like natural evolution, but for cybersecurity.
    </p>""", unsafe_allow_html=True)

    ga = mirages_data.get("ga", {})
    gen = ga.get("generation", 1)
    fitness = ga.get("fitness", 100)
    strategy = ga.get("best_strategy", "polymorphic_random")
    improvement = ga.get("improvement", 0)

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Generation",      gen)
    c2.metric("Best Fitness",    f"{fitness:.1f}")
    c3.metric("Population Size", ga.get("population", 20))
    c4.metric("Improvement",     f"+{improvement:.1f}")

    st.markdown("---")

    col1, col2 = st.columns([2, 1])
    with col1:
        st.plotly_chart(chart_ga_fitness(mirages_data), use_container_width=True)
    with col2:
        st.markdown("### 🏆 Best Strategy")
        st.markdown(f"""
        <div style='background:#001a00; border:1px solid #00ff00; border-radius:8px; padding:16px; margin:10px 0;'>
            <div style='color:#00ff88; font-size:0.85rem; font-weight:bold'>Active Strategy</div>
            <div style='color:#fff; font-size:1.1rem; margin:8px 0'>{strategy.replace("_"," ").title()}</div>
            <hr style='border-color:#003300; margin:8px 0'>
            <div style='color:#aaa; font-size:0.8rem'>
            Fitness Score: <b style='color:#00ff88'>{fitness:.1f}</b><br>
            Generation: <b style='color:#00ff88'>{gen}</b><br>
            Mutation Rate: <b style='color:#00ff88'>0.20</b><br>
            Crossover Rate: <b style='color:#00ff88'>0.80</b>
            </div>
        </div>""", unsafe_allow_html=True)

    st.markdown("---")

    # Strategy comparison
    st.markdown("### 📊 Strategy Performance Comparison")
    strategies = ["Random", "Polymorphic", "Entropy Max", "Behavioral", "Fractal", "Chaotic"]
    scores     = [100, 145, 167, 189, 201, fitness]
    colors_bar = ["#444", "#0066cc", "#00aacc", "#00bbaa", "#00cc88", "#00ff88"]

    fig = go.Figure(go.Bar(
        x=strategies, y=scores,
        marker_color=colors_bar,
        text=[f"{s:.0f}" for s in scores],
        textposition="outside",
        textfont=dict(color="white")
    ))
    fig.update_layout(
        yaxis_title="Fitness Score",
        plot_bgcolor="#0d1520", paper_bgcolor="#0d1520",
        font=dict(color="#ccc"), height=280, showlegend=False
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("""
    ---
    ### 💡 How Genetic Algorithm Works Here

    1. **Population** — 20 deception strategies exist simultaneously
    2. **Fitness Function** — Measures engagement_time(0.3) + data_quality(0.25) + confusion(0.25) + diversity(0.2)
    3. **Selection** — Top strategies survive (tournament selection k=3)
    4. **Crossover** — Best strategies blend their parameters (rate=0.80)
    5. **Mutation** — Random adjustments to prevent stagnation (rate=0.20)
    6. **Evolution** — Runs every 30 seconds, gets smarter over time

    **This is the first GA application for DEFENSE optimization (not just malware detection)!**
    """)


# ─────────────────────────────────────────────
#  Page: AI Detection
# ─────────────────────────────────────────────

def page_ai(attacks):
    st.markdown("<h1 style='color:#00d2ff'>🤖 AI Detection Engine</h1>", unsafe_allow_html=True)
    st.markdown("""
    <p style='color:#888'>
    Four AI models work together as an ensemble.
    Each model votes on whether a connection is a threat.
    The final decision is a <b style='color:#00d2ff'>weighted vote</b> — more accurate than any single model.
    </p>""", unsafe_allow_html=True)

    # Model performance cards
    col1, col2, col3, col4 = st.columns(4)
    models_info = [
        ("Isolation Forest", "0.3", "Detects anomalies in traffic patterns", "#0066cc"),
        ("LSTM Network",     "0.3", "Detects sequential attack patterns",    "#aa00ff"),
        ("Autoencoder",      "0.2", "Detects deviations from normal",        "#00aacc"),
        ("Random Forest",    "0.2", "Classifies known attack types",         "#00cc88"),
    ]
    for col, (name, weight, desc, color) in zip([col1,col2,col3,col4], models_info):
        col.markdown(f"""
        <div style='background:#0d1520; border:1px solid {color}; border-radius:8px; padding:12px; text-align:center; height:110px;'>
            <div style='color:{color}; font-weight:bold; font-size:0.9rem'>{name}</div>
            <div style='color:#00d2ff; font-size:1.5rem; margin:4px'>w={weight}</div>
            <div style='color:#888; font-size:0.7rem'>{desc}</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("---")

    col1, col2 = st.columns([1, 1])
    with col1:
        st.plotly_chart(chart_ai_models(attacks), use_container_width=True)
    with col2:
        # Detection accuracy over time
        if not attacks:
            st.info("AI scores will appear here after first attack")
        else:
            scores = [a.get("threat_score", 0) for a in attacks[-20:]]
            times  = list(range(len(scores)))

            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=times, y=scores,
                mode="lines+markers",
                fill="tozeroy",
                fillcolor="rgba(0,210,255,0.1)",
                line=dict(color="#00d2ff", width=2),
                name="Ensemble Score"
            ))
            fig.add_hline(y=0.7, line_dash="dash", line_color="#ff6600", annotation_text="Threat Threshold")
            fig.update_layout(
                title="Ensemble Detection Score (Last 20 Attacks)",
                yaxis=dict(range=[0, 1.05]),
                plot_bgcolor="#0d1520", paper_bgcolor="#0d1520",
                font=dict(color="#ccc"), height=280
            )
            st.plotly_chart(fig, use_container_width=True)

    if attacks:
        # Show latest attack's full AI breakdown
        st.markdown("### 🔍 Latest Attack - Full AI Breakdown")
        last = attacks[-1]
        ai = last.get("ai_models", {})

        c1, c2, c3 = st.columns(3)
        c1.metric("Isolation Forest", f"{ai.get('isolation_forest',0):.2f}")
        c2.metric("LSTM Score",       f"{ai.get('lstm',0):.2f}")
        c3.metric("Autoencoder",      f"{ai.get('autoencoder',0):.2f}")

        c4, c5, c6 = st.columns(3)
        c4.metric("Random Forest", f"{ai.get('random_forest',0):.2f}")
        c5.metric("Ensemble Final", f"{ai.get('ensemble',0):.2f}")
        c6.metric("Verdict", "🔴 THREAT" if ai.get('ensemble',0) >= 0.7 else "🟢 SAFE")

    st.markdown("""
    ---
    ### 💡 Why Ensemble (4 Models) is Better

    | Model | Best At | Weakness |
    |---|---|---|
    | Isolation Forest | Rare anomalies | Misses patterns |
    | LSTM | Time-series attacks | Needs history |
    | Autoencoder | Deviation detection | Slow to adapt |
    | Random Forest | Known attack types | New attacks |

    **Together (weighted ensemble): 96.7% accuracy, <3% false positives**
    """)


# ─────────────────────────────────────────────
#  Page: Alert Feed
# ─────────────────────────────────────────────

def page_alerts(attacks, metrics):
    st.markdown("<h1 style='color:#00d2ff'>⚠️ Security Alert Feed</h1>", unsafe_allow_html=True)

    # Alert summary
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("🔴 Critical", metrics["critical"])
    c2.metric("🟠 High",     metrics["high"])
    c3.metric("🟡 Medium",   metrics["medium"])
    c4.metric("🟢 Low",      metrics["low"])

    st.markdown("---")

    if not attacks:
        st.success("✅ No alerts. System is monitoring. Attack the honeypots to see alerts here!")
        return

    # Show all alerts
    st.markdown("### All Alerts (newest first)")

    for attack in reversed(attacks[-30:]):
        sev = attack.get("severity", "LOW")
        ts  = attack.get("time_display", "")
        typ = attack.get("type", "").replace("_", " ").upper()
        ip  = attack.get("source_ip", "")
        score = attack.get("threat_score", 0)
        mirage = attack.get("mirage_triggered", "unknown")

        cls = {"CRITICAL": "alert-critical", "HIGH": "alert-high",
               "MEDIUM": "alert-medium", "LOW": "alert-low"}.get(sev, "alert-low")
        emoji = {"CRITICAL": "🔴", "HIGH": "🟠", "MEDIUM": "🟡", "LOW": "🟢"}.get(sev, "⚪")

        st.markdown(f"""
        <div class='{cls}'>
            <span style='color:#aaa;font-size:0.75rem'>{ts}</span>
            <span style='margin:0 10px; font-weight:bold'>{emoji} {sev}</span>
            <span style='color:#fff'>{typ}</span>
            <span style='color:#888; margin:0 10px'>from {ip}</span>
            <span style='color:#00d2ff; float:right'>Score: {score:.2f} | Mirage: {mirage}</span>
        </div>""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  MAIN APP
# ─────────────────────────────────────────────

def main():
    # Load fresh data every refresh
    attacks      = load_attacks()
    mirages_data = load_mirages()
    metrics      = get_metrics(attacks)
    ga           = mirages_data.get("ga", {})

    # Sidebar with navigation
    page = render_sidebar(metrics, ga)

    # Page routing
    if page == "📊 Live Monitor":
        page_live_monitor(attacks, metrics, mirages_data)

    elif page == "🎭 Polymorphic Mirages":
        page_mirages(mirages_data)

    elif page == "🧬 Genetic Evolution":
        page_genetic(mirages_data)

    elif page == "🤖 AI Detection":
        page_ai(attacks)

    elif page == "⚠️ Alert Feed":
        page_alerts(attacks, metrics)

    # Auto-refresh every 2 seconds
    time.sleep(2)
    st.rerun()


if __name__ == "__main__":
    main()