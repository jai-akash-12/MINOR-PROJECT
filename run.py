"""
MAIN RUN FILE
Start the complete AI Cyber Deception and SOC Monitoring System

Options:
1. Run live demo
2. Start dashboard only
3. Run attack simulation
4. Full system deployment
"""

import sys
import subprocess
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent))

from utilities.logger import get_logger

logger = get_logger('main')


def print_banner():
    """Print system banner"""
    banner = """
╔═══════════════════════════════════════════════════════════════════════════════╗
║                                                                               ║
║          🛡️  AI POWERED CYBER DECEPTION AND SOC MONITORING SYSTEM  🛡️          ║
║                                                                               ║
║                    Polymorphic Deception • Genetic Evolution                 ║
║                    Mathematical Primitives • Multi-Model AI                  ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
    """
    print(banner)


def show_menu():
    """Show main menu"""
    print("\n" + "="*80)
    print("CHOOSE AN OPTION:")
    print("="*80)
    print("\n1. 🎬 Run Live Demo (For Guide Presentation)")
    print("2. 📊 Start SOC Dashboard Only")
    print("3. 🎯 Run Attack Simulation")
    print("4. 🚀 Full System Deployment")
    print("5. 🧪 Test Individual Components")
    print("6. ❌ Exit")
    print("\n" + "="*80)


def run_live_demo():
    """Run the complete live demonstration"""
    logger.info("Starting live demonstration...")
    from demo_orchestrator import DemoOrchestrator
    
    demo = DemoOrchestrator()
    demo.setup_system()
    demo.run_live_demonstration(duration_seconds=60)
    
    print("\n✅ Demo complete!")
    print("💡 To view the dashboard, run: streamlit run 4_soc_dashboard/streamlit_app.py")


def start_dashboard():
    """Start the Streamlit dashboard"""
    logger.info("Starting SOC Dashboard...")
    dashboard_path = Path(__file__).parent / "4_soc_dashboard" / "streamlit_app.py"
    
    print("\n🚀 Starting dashboard...")
    print("📊 Dashboard will open in your browser at http://localhost:8501")
    print("\nPress Ctrl+C to stop the dashboard\n")
    
    subprocess.run(["streamlit", "run", str(dashboard_path)])


def run_attack_simulation():
    """Run attack simulation only"""
    logger.info("Running attack simulation...")
    from attack_simulation.attack_simulator import AttackSimulator
    
    simulator = AttackSimulator()
    
    print("\n🎯 Running full attack scenario...")
    results = simulator.run_full_attack_scenario()
    
    print("\n📊 Results:")
    print(f"   Duration: {results['scenario_duration']:.2f}s")
    print(f"   Total Attacks: {results['total_attacks']}")
    print(f"   Deceptions Triggered: {results['deceptions_triggered']}")
    print(f"   Average Threat Score: {results['avg_threat_score']:.2f}")


def full_system_deployment():
    """Deploy full system"""
    logger.info("Deploying full system...")
    from demo_orchestrator import DemoOrchestrator
    
    demo = DemoOrchestrator()
    demo.setup_system()
    
    print("\n✅ System deployed successfully!")
    print("\nSystem Components:")
    print("   ✅ Polymorphic Process Mirages")
    print("   ✅ Genetic Algorithm Evolution")
    print("   ✅ Mathematical Deception")
    print("   ✅ Honeypot Services")
    print("   ✅ AI Detection Models")
    
    print("\n💡 Next steps:")
    print("   1. Run dashboard: streamlit run 4_soc_dashboard/streamlit_app.py")
    print("   2. Monitor logs in: logs/")


def test_components():
    """Test individual components"""
    print("\n🧪 COMPONENT TESTING")
    print("="*80)
    
    # Test 1: Polymorphic Mirages
    print("\n[1/5] Testing Polymorphic Process Mirages...")
    from deception_layer.polymorphic_process import PolymorphicProcessMirage
    
    mirage_system = PolymorphicProcessMirage()
    mirage = mirage_system.create_mirage('database')
    mutated = mirage_system.morph_characteristics(mirage['id'])
    
    print(f"   ✅ Created mirage: {mirage['id']}")
    print(f"   ✅ Mutation successful")
    print(f"   ✅ Genetic diversity: {mutated['genetic_diversity_scores'][-1]:.3f}")
    
    # Test 2: Genetic Algorithm
    print("\n[2/5] Testing Genetic Algorithm...")
    from deception_layer.genetic_deception import GeneticDeceptionEvolver
    
    ga = GeneticDeceptionEvolver()
    print(f"   ✅ Population size: {len(ga.population)}")
    print(f"   ✅ Initial best fitness: {ga.get_best_chromosome()['fitness']:.2f}")
    
    # Test 3: Mathematical Deception
    print("\n[3/5] Testing Mathematical Deception...")
    from deception_layer.mathematical_deception import MathematicalDeception
    
    math_dec = MathematicalDeception()
    fractal_fs = math_dec.generate_fractal_filesystem(depth=3)
    chaotic_creds = math_dec.generate_chaotic_credentials('admin', 3)
    
    print(f"   ✅ Fractal filesystem: {len(fractal_fs['files'])} files")
    print(f"   ✅ Chaotic credentials: {len(chaotic_creds)} generated")
    print(f"   ✅ Entropy: {fractal_fs['entropy_score']:.3f}")
    
    # Test 4: AI Detection
    print("\n[4/5] Testing AI Detection Engine...")
    from core_engine.ensemble_engine import EnsembleAIDetector
    
    detector = EnsembleAIDetector()
    detector.initialize_models()
    
    detection = detector.detect_threat({
        'packet_count': 500,
        'byte_count': 50000,
        'duration': 5,
        'dst_port': 22,
        'port_scan_score': 0.8,
        'brute_force_score': 0.3,
        'timestamp': ''
    })
    
    print(f"   ✅ AI models initialized")
    print(f"   ✅ Test detection: Threat Score = {detection['threat_score']:.2f}")
    print(f"   ✅ Classification: {detection['threat_level']}")
    
    # Test 5: Attack Simulator
    print("\n[5/5] Testing Attack Simulator...")
    from attack_simulation.attack_simulator import AttackSimulator
    
    simulator = AttackSimulator()
    attack = simulator.launch_port_scan(num_ports=10)
    
    print(f"   ✅ Attack simulation successful")
    print(f"   ✅ Attack type: {attack['type']}")
    print(f"   ✅ Threat score: {attack['threat_score']:.2f}")
    
    print("\n" + "="*80)
    print("✅ ALL COMPONENTS TESTED SUCCESSFULLY!")
    print("="*80)


def main():
    """Main function"""
    print_banner()
    
    while True:
        show_menu()
        
        choice = input("\nEnter your choice (1-6): ").strip()
        
        if choice == '1':
            run_live_demo()
            input("\nPress Enter to return to menu...")
        
        elif choice == '2':
            start_dashboard()
        
        elif choice == '3':
            run_attack_simulation()
            input("\nPress Enter to return to menu...")
        
        elif choice == '4':
            full_system_deployment()
            input("\nPress Enter to return to menu...")
        
        elif choice == '5':
            test_components()
            input("\nPress Enter to return to menu...")
        
        elif choice == '6':
            print("\n👋 Goodbye!\n")
            break
        
        else:
            print("\n❌ Invalid choice. Please try again.")


if __name__ == "__main__":
    main()