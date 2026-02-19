#!/usr/bin/env python3
"""
LIVE DEMO LAUNCHER
Starts everything needed for your guide presentation

This script will:
1. Start the system components
2. Launch the live dashboard
3. Provide instructions for attacking

Run this before your guide arrives!
"""

import subprocess
import time
import sys
from pathlib import Path

def print_banner():
    print("\n" + "="*80)
    print("🎬 LIVE DEMO LAUNCHER")
    print("="*80)
    print()

def print_section(title):
    print("\n" + "─"*80)
    print(f"  {title}")
    print("─"*80)

def get_ip_address():
    """Get system IP address"""
    import socket
    try:
        # Connect to external host to determine local IP
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "localhost"

def main():
    print_banner()
    
    # Get IP
    ip_address = get_ip_address()
    
    print_section("STEP 1: Starting System Components")
    print("\n✅ Initializing...")
    print("   - Polymorphic Process Mirages")
    print("   - Genetic Algorithm")
    print("   - Honeypot Services")
    print("   - AI Detection Models")
    
    # Import and start components
    sys.path.append(str(Path(__file__).parent))
    
    try:
        from deception_layer.polymorphic_process import PolymorphicProcessMirage
        from deception_layer.genetic_deception import GeneticDeceptionEvolver
        from deception_layer.honeypot_manager import HoneypotManager
        from core_engine.ensemble_engine import EnsembleAIDetector
        
        print("\n🎭 Creating Polymorphic Mirages...")
        mirage_system = PolymorphicProcessMirage()
        for i in range(5):
            mirage_system.create_mirage()
        print(f"   ✅ {len(mirage_system.active_mirages)} mirages active")
        
        print("\n🧬 Initializing Genetic Algorithm...")
        ga = GeneticDeceptionEvolver()
        print(f"   ✅ Population of {len(ga.population)} strategies ready")
        
        print("\n🍯 Deploying Honeypots...")
        honeypot_mgr = HoneypotManager()
        honeypot_mgr.deploy_honeypots()
        stats = honeypot_mgr.get_honeypot_stats()
        print(f"   ✅ {stats['active_honeypots']} honeypots deployed:")
        for service, info in stats['by_service'].items():
            print(f"      • {service.upper()} on port {info['port']}")
        
        print("\n🤖 Initializing AI Models...")
        ai = EnsembleAIDetector()
        ai.initialize_models()
        print("   ✅ Multi-model ensemble ready")
        
    except Exception as e:
        print(f"\n⚠️  Component initialization error: {e}")
        print("   This is OK - dashboard will still work!")
    
    print_section("STEP 2: Starting Live Dashboard")
    print(f"\n🚀 Launching dashboard on http://{ip_address}:8501")
    print("   Dashboard will auto-refresh every 2 seconds")
    print("   Press Ctrl+C to stop")
    
    time.sleep(2)
    
    print_section("STEP 3: Attack Instructions")
    print(f"""
Your system is ready! To demonstrate to your guide:

📱 FROM ANOTHER DEVICE (or same terminal):

1. PORT SCAN:
   nmap -p 1-1000 {ip_address}

2. SSH BRUTE FORCE:
   ssh admin@{ip_address} -p 2222
   (Try passwords: admin, password, admin123)

3. HTTP ACCESS:
   Open browser: http://{ip_address}:8080

4. CONTINUOUS ATTACKS:
   while true; do nmap -p 2222,8080,2121 {ip_address}; sleep 3; done

💡 WHAT YOUR GUIDE WILL SEE:
   - Network topology updating with attacker IP
   - Attack feed scrolling in real-time  
   - Threat scores increasing
   - All metrics updating live

🎯 DASHBOARD PAGES TO SHOW:
   1. Live Monitor - See attacks happening
   2. Attack Feed - Real-time log scrolling
   3. Statistics - Charts updating live
""")
    
    print("─"*80)
    input("\n📍 Press ENTER when ready to start dashboard...")
    
    # Start dashboard
    dashboard_path = Path(__file__).parent / "4_soc_dashboard" / "live_dashboard.py"
    
    print("\n🎬 Starting live dashboard...\n")
    
    try:
        subprocess.run([
            sys.executable, "-m", "streamlit", "run",
            str(dashboard_path),
            "--server.address", "0.0.0.0"
        ])
    except KeyboardInterrupt:
        print("\n\n✅ Demo stopped. Great job!\n")

if __name__ == "__main__":
    main()