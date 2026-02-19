"""
ATTACK SIMULATOR
Generates realistic cyber attack scenarios for demonstration

Attack types:
- Port scanning
- SSH brute force
- Lateral movement
- Data exfiltration
- Privilege escalation
"""

import random
import time
from datetime import datetime
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parent.parent))
from utilities.config import ATTACK_CONFIG
from utilities.logger import get_logger, log_attack

logger = get_logger('attack_simulator')


class AttackSimulator:
    """
    Simulates various cyber attack scenarios for testing and demonstration
    """
    
    def __init__(self):
        self.config = ATTACK_CONFIG
        self.attack_history = []
        self.attacker_ip = self._generate_attacker_ip()
        
        logger.info(f"Attack Simulator initialized (Attacker IP: {self.attacker_ip})")
    
    def _generate_attacker_ip(self):
        """Generate a realistic attacker IP"""
        return f"{random.randint(1,223)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(1,254)}"
    
    def launch_port_scan(self, target='192.168.1.100', num_ports=100):
        """
        Simulate port scanning attack
        
        Attacker probes many ports to find open services
        """
        logger.info(f"🔍 Launching port scan attack on {target}")
        
        scanned_ports = random.sample(range(1, 65535), num_ports)
        open_ports = []
        
        start_time = time.time()
        
        for port in scanned_ports:
            # Simulate scan
            time.sleep(0.01)  # Small delay for realism
            
            # Some ports are "open" (honeypots)
            if random.random() < 0.1:
                open_ports.append(port)
        
        duration = time.time() - start_time
        
        attack_data = {
            'type': 'port_scan',
            'source_ip': self.attacker_ip,
            'target': target,
            'severity': 'MEDIUM',
            'threat_score': 0.6,
            'deception_triggered': len(open_ports) > 0,
            'details': {
                'ports_scanned': num_ports,
                'open_ports': open_ports,
                'duration': duration,
                'scan_rate': num_ports / duration
            }
        }
        
        self.attack_history.append(attack_data)
        log_attack(attack_data)
        
        logger.info(f"✅ Port scan complete: {len(open_ports)} open ports found")
        
        return attack_data
    
    def launch_ssh_bruteforce(self, target_port=2222, attempts=50):
        """
        Simulate SSH brute force attack
        
        Attacker tries multiple username/password combinations
        """
        logger.info(f"🔓 Launching SSH brute force attack on port {target_port}")
        
        common_passwords = [
            'admin', 'password', '123456', 'admin123', 'root',
            'password123', 'qwerty', 'letmein', 'welcome'
        ]
        
        common_usernames = [
            'admin', 'root', 'user', 'administrator', 'test'
        ]
        
        start_time = time.time()
        successful_login = False
        attempts_made = 0
        
        for i in range(attempts):
            username = random.choice(common_usernames)
            password = random.choice(common_passwords)
            
            # Simulate attempt
            time.sleep(0.1)
            attempts_made += 1
            
            # Random chance of "success" (hitting honeypot)
            if random.random() < 0.02:
                successful_login = True
                break
        
        duration = time.time() - start_time
        
        attack_data = {
            'type': 'ssh_bruteforce',
            'source_ip': self.attacker_ip,
            'target': f'SSH:{target_port}',
            'severity': 'HIGH',
            'threat_score': 0.8,
            'deception_triggered': successful_login,
            'details': {
                'attempts': attempts_made,
                'successful': successful_login,
                'duration': duration,
                'attempts_per_second': attempts_made / duration
            }
        }
        
        self.attack_history.append(attack_data)
        log_attack(attack_data)
        
        if successful_login:
            logger.info(f"✅ SSH brute force 'successful' - honeypot engaged!")
        else:
            logger.info(f"⚠️  SSH brute force failed after {attempts_made} attempts")
        
        return attack_data
    
    def launch_lateral_movement(self):
        """
        Simulate lateral movement attack
        
        Attacker tries to move from one system to another
        """
        logger.info("🔀 Launching lateral movement attack")
        
        internal_ips = [
            f"192.168.1.{i}" for i in range(10, 30)
        ]
        
        start_time = time.time()
        accessed_systems = []
        
        # Try to access multiple systems
        for ip in random.sample(internal_ips, 5):
            time.sleep(0.2)
            
            # Some systems are accessible (honeypots/decoys)
            if random.random() < 0.4:
                accessed_systems.append(ip)
        
        duration = time.time() - start_time
        
        attack_data = {
            'type': 'lateral_movement',
            'source_ip': self.attacker_ip,
            'target': 'Internal Network',
            'severity': 'CRITICAL',
            'threat_score': 0.9,
            'deception_triggered': len(accessed_systems) > 0,
            'details': {
                'systems_probed': 5,
                'systems_accessed': accessed_systems,
                'duration': duration
            }
        }
        
        self.attack_history.append(attack_data)
        log_attack(attack_data)
        
        logger.info(f"✅ Lateral movement: {len(accessed_systems)} systems accessed")
        
        return attack_data
    
    def launch_data_exfiltration(self):
        """
        Simulate data exfiltration attempt
        
        Attacker tries to steal sensitive data
        """
        logger.info("📤 Launching data exfiltration attack")
        
        start_time = time.time()
        
        # Simulate finding and accessing fake sensitive files
        fake_files = [
            '/var/data/customer_database.sql',
            '/home/admin/credentials.txt',
            '/opt/backup/financial_records.csv',
            '/etc/secret/api_keys.conf'
        ]
        
        exfiltrated_files = random.sample(fake_files, random.randint(1, 3))
        
        # Simulate transfer
        total_size = random.randint(10, 500)  # MB
        time.sleep(1)
        
        duration = time.time() - start_time
        
        attack_data = {
            'type': 'data_exfiltration',
            'source_ip': self.attacker_ip,
            'target': 'File Server',
            'severity': 'CRITICAL',
            'threat_score': 0.95,
            'deception_triggered': True,
            'details': {
                'files_accessed': exfiltrated_files,
                'size_mb': total_size,
                'duration': duration,
                'transfer_rate': total_size / duration
            }
        }
        
        self.attack_history.append(attack_data)
        log_attack(attack_data)
        
        logger.info(f"✅ Data exfiltration: {len(exfiltrated_files)} fake files 'stolen'")
        
        return attack_data
    
    def launch_privilege_escalation(self):
        """
        Simulate privilege escalation attempt
        """
        logger.info("⬆️  Launching privilege escalation attack")
        
        start_time = time.time()
        
        # Common privilege escalation techniques
        techniques = [
            'sudo_exploit',
            'kernel_exploit',
            'suid_abuse',
            'cron_job_manipulation'
        ]
        
        technique_used = random.choice(techniques)
        time.sleep(0.5)
        
        # Random success (hitting deception)
        success = random.random() < 0.3
        
        duration = time.time() - start_time
        
        attack_data = {
            'type': 'privilege_escalation',
            'source_ip': self.attacker_ip,
            'target': 'Linux Server',
            'severity': 'CRITICAL',
            'threat_score': 0.9,
            'deception_triggered': success,
            'details': {
                'technique': technique_used,
                'successful': success,
                'duration': duration
            }
        }
        
        self.attack_history.append(attack_data)
        log_attack(attack_data)
        
        logger.info(f"✅ Privilege escalation attempt using {technique_used}")
        
        return attack_data
    
    def run_full_attack_scenario(self):
        """
        Run a complete attack scenario with multiple phases
        This simulates a realistic APT (Advanced Persistent Threat) attack
        """
        logger.info("=" * 60)
        logger.info("🎯 STARTING FULL ATTACK SCENARIO")
        logger.info("=" * 60)
        
        scenario_start = time.time()
        results = []
        
        # Phase 1: Reconnaissance (Port Scan)
        logger.info("\n[PHASE 1] Reconnaissance")
        results.append(self.launch_port_scan())
        time.sleep(2)
        
        # Phase 2: Initial Access (SSH Brute Force)
        logger.info("\n[PHASE 2] Initial Access")
        results.append(self.launch_ssh_bruteforce())
        time.sleep(2)
        
        # Phase 3: Lateral Movement
        logger.info("\n[PHASE 3] Lateral Movement")
        results.append(self.launch_lateral_movement())
        time.sleep(2)
        
        # Phase 4: Privilege Escalation
        logger.info("\n[PHASE 4] Privilege Escalation")
        results.append(self.launch_privilege_escalation())
        time.sleep(2)
        
        # Phase 5: Data Exfiltration
        logger.info("\n[PHASE 5] Data Exfiltration")
        results.append(self.launch_data_exfiltration())
        
        scenario_duration = time.time() - scenario_start
        
        # Summary
        logger.info("\n" + "=" * 60)
        logger.info("📊 ATTACK SCENARIO SUMMARY")
        logger.info("=" * 60)
        logger.info(f"Total Duration: {scenario_duration:.2f} seconds")
        logger.info(f"Total Attacks: {len(results)}")
        logger.info(f"Deceptions Triggered: {sum(1 for r in results if r['deception_triggered'])}")
        logger.info(f"Avg Threat Score: {sum(r['threat_score'] for r in results) / len(results):.2f}")
        logger.info("=" * 60)
        
        return {
            'scenario_duration': scenario_duration,
            'total_attacks': len(results),
            'deceptions_triggered': sum(1 for r in results if r['deception_triggered']),
            'avg_threat_score': sum(r['threat_score'] for r in results) / len(results),
            'results': results
        }
    
    def get_attack_stats(self):
        """Get statistics about simulated attacks"""
        if not self.attack_history:
            return {
                'total_attacks': 0,
                'by_type': {},
                'avg_threat_score': 0.0
            }
        
        stats = {
            'total_attacks': len(self.attack_history),
            'by_type': {},
            'avg_threat_score': sum(a['threat_score'] for a in self.attack_history) / len(self.attack_history),
            'deceptions_triggered': sum(1 for a in self.attack_history if a.get('deception_triggered', False))
        }
        
        # Count by type
        for attack in self.attack_history:
            attack_type = attack['type']
            stats['by_type'][attack_type] = stats['by_type'].get(attack_type, 0) + 1
        
        return stats
    
    def simulate_continuous_attacks(self, duration_seconds=60):
        """
        Simulate continuous random attacks for specified duration
        Useful for dashboard testing
        """
        logger.info(f"Starting continuous attack simulation for {duration_seconds} seconds")
        
        attack_types = [
            self.launch_port_scan,
            self.launch_ssh_bruteforce,
            self.launch_lateral_movement
        ]
        
        start_time = time.time()
        attack_count = 0
        
        while time.time() - start_time < duration_seconds:
            # Random attack
            attack_func = random.choice(attack_types)
            attack_func()
            attack_count += 1
            
            # Random delay
            time.sleep(random.uniform(3, 8))
        
        logger.info(f"Continuous simulation complete: {attack_count} attacks generated")
        
        return attack_count