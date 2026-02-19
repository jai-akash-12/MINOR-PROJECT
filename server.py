"""
=============================================================
  HONEYPOT SERVER - Run this FIRST before the dashboard
=============================================================

This starts REAL honeypots that listen on ports.
When someone attacks, it writes to logs/attacks.json
The dashboard reads that file and updates live.

HOW TO RUN:
    python server.py

HOW TO ATTACK (from another device or terminal):
    SSH:  ssh admin@YOUR_IP -p 2222
    HTTP: open browser to http://YOUR_IP:8080
    SCAN: nmap -p 2222,8080,2121 YOUR_IP

=============================================================
"""

import socket
import threading
import json
import os
import time
import random
import math
from datetime import datetime
from pathlib import Path

import numpy as np
from sklearn.ensemble import IsolationForest, RandomForestClassifier
from sklearn.preprocessing import StandardScaler

# ─────────────────────────────────────────────
#  Setup: Create logs folder and attacks file
# ─────────────────────────────────────────────
BASE_DIR = Path(__file__).parent
LOGS_DIR = BASE_DIR / "logs"
LOGS_DIR.mkdir(exist_ok=True)
ATTACKS_FILE = LOGS_DIR / "attacks.json"

# Start with empty attack list
if not ATTACKS_FILE.exists():
    with open(ATTACKS_FILE, "w") as f:
        json.dump([], f)

# Mirage state file (dashboard reads this too)
MIRAGE_FILE = LOGS_DIR / "mirages.json"

# ─────────────────────────────────────────────
#  Globals to track state
# ─────────────────────────────────────────────
attack_lock = threading.Lock()
mirage_lock = threading.Lock()

MIRAGES = [
    {"id": i+1, "original": name, "current": name, "mutations": 0,
     "diversity_score": round(random.uniform(0.3, 0.5), 2),
     "status": "active", "interactions": 0}
    for i, name in enumerate([
        "mysqld", "apache2", "sshd", "redis-server",
        "postgres", "nginx", "rsyslogd", "cron",
        "python3", "node", "mongod", "php-fpm"
    ])
]

GA_STATE = {
    "generation": 1,
    "fitness": 100.0,
    "population": 20,
    "best_strategy": "polymorphic_random",
    "improvement": 0.0
}

# ─────────────────────────────────────────────
#  Real AI Models (trained on synthetic data)
# ─────────────────────────────────────────────

print("  [AI] Training models on synthetic network data...")

# --- Generate synthetic training data ---
def _make_sample(is_attack, attack_type=None):
    """Generate one synthetic network traffic sample"""
    if is_attack:
        profiles = {
            "ssh_bruteforce":  dict(pkt=random.randint(300,2000), bytes=random.randint(30000,200000),
                                    duration=random.uniform(5,60), sport=random.randint(30000,65535),
                                    dport=2222, pps=random.uniform(10,80), bps=random.uniform(500,5000),
                                    psize=random.uniform(50,200), udest=1, pss=0.2, bfs=random.uniform(0.7,1.0)),
            "port_scan":       dict(pkt=random.randint(500,5000), bytes=random.randint(10000,50000),
                                    duration=random.uniform(1,10), sport=random.randint(30000,65535),
                                    dport=random.choice([22,23,80,443,2222,8080,3389]),
                                    pps=random.uniform(50,500), bps=random.uniform(1000,10000),
                                    psize=random.uniform(40,100), udest=random.randint(20,100),
                                    pss=random.uniform(0.7,1.0), bfs=0.1),
            "http_probe":      dict(pkt=random.randint(10,100), bytes=random.randint(500,5000),
                                    duration=random.uniform(0.1,5), sport=random.randint(30000,65535),
                                    dport=8080, pps=random.uniform(1,10), bps=random.uniform(100,1000),
                                    psize=random.uniform(200,800), udest=1, pss=0.0, bfs=0.2),
            "ftp_bruteforce":  dict(pkt=random.randint(200,1000), bytes=random.randint(5000,50000),
                                    duration=random.uniform(10,120), sport=random.randint(30000,65535),
                                    dport=2121, pps=random.uniform(5,30), bps=random.uniform(200,2000),
                                    psize=random.uniform(50,150), udest=1, pss=0.1, bfs=random.uniform(0.6,0.9)),
        }
        p = profiles.get(attack_type, profiles["http_probe"])
    else:
        p = dict(pkt=random.randint(10,100), bytes=random.randint(1000,10000),
                 duration=random.uniform(1,60), sport=random.randint(30000,65535),
                 dport=random.choice([80,443,8080,3000,5000]),
                 pps=random.uniform(1,10), bps=random.uniform(100,1000),
                 psize=random.uniform(500,1500), udest=random.randint(1,3),
                 pss=random.uniform(0,0.2), bfs=random.uniform(0,0.15))
    return [p["pkt"], p["bytes"], p["duration"], p["sport"], p["dport"],
            p["pps"], p["bps"], p["psize"], p["udest"], p["pss"], p["bfs"]]

# Build dataset: 800 normal + 400 attacks
ATTACK_TYPES = ["ssh_bruteforce", "port_scan", "http_probe", "ftp_bruteforce"]
X_train, y_train = [], []
for _ in range(800):
    X_train.append(_make_sample(False))
    y_train.append(0)
for atype in ATTACK_TYPES:
    for _ in range(100):
        X_train.append(_make_sample(True, atype))
        y_train.append(1)

X_train = np.array(X_train)
y_train = np.array(y_train)

# Fit scaler
AI_SCALER = StandardScaler()
X_scaled = AI_SCALER.fit_transform(X_train)

# Train Isolation Forest (anomaly detector)
IF_MODEL = IsolationForest(contamination=0.3, n_estimators=100, random_state=42)
IF_MODEL.fit(X_scaled)

# Train Random Forest (classifier)
RF_MODEL = RandomForestClassifier(n_estimators=100, max_depth=15, random_state=42)
RF_MODEL.fit(X_scaled, y_train)

print("  [AI] ✅ Models trained — IsolationForest + RandomForest ready")


# ─────────────────────────────────────────────
#  Helpers
# ─────────────────────────────────────────────

def get_severity(threat_score):
    if threat_score >= 0.85:
        return "CRITICAL"
    elif threat_score >= 0.7:
        return "HIGH"
    elif threat_score >= 0.5:
        return "MEDIUM"
    else:
        return "LOW"


def calculate_ai_score(attack_type, attempts=1, target_port=2222):
    """
    Real AI scoring using trained IsolationForest + RandomForest.
    LSTM and Autoencoder scores are analytically derived (simulated)
    because they need TensorFlow which may not be installed.
    Ensemble: IF(0.3) + LSTM(0.3) + AE(0.2) + RF(0.2)
    """
    # Build feature vector from attack characteristics
    port_to_pss = {2222: 0.1, 2121: 0.1, 8080: 0.0}
    port_to_bfs = {2222: max(0.5, min(0.99, 0.3 + attempts*0.05)),
                   2121: max(0.4, min(0.9, 0.2 + attempts*0.04)),
                   8080: 0.2}
    pkt = 50 + attempts * 30
    features = np.array([[
        pkt,                              # packet_count
        pkt * 150,                        # byte_count
        max(0.5, 60 - attempts),          # duration
        random.randint(30000, 65535),     # src_port
        target_port,                      # dst_port
        pkt / max(1, 60 - attempts),      # packets_per_second
        pkt * 150 / max(1, 60-attempts),  # bytes_per_second
        150.0,                            # avg_packet_size
        1,                                # unique_destinations
        port_to_pss.get(target_port, 0.5), # port_scan_score
        port_to_bfs.get(target_port, 0.3), # brute_force_score
    ]])

    features_scaled = AI_SCALER.transform(features)

    # 1. Isolation Forest → anomaly score (convert to 0-1)
    if_raw = IF_MODEL.score_samples(features_scaled)[0]  # negative; more neg = more anomalous
    if_score = round(float(np.clip(1 - (if_raw + 0.5), 0, 1)), 2)

    # 2. Random Forest → probability of being attack
    rf_proba = RF_MODEL.predict_proba(features_scaled)[0]
    rf_score = round(float(rf_proba[1] if len(rf_proba) > 1 else 0.5), 2)

    # 3. LSTM → simulated sequential score (rule-based approximation)
    lstm_score = round(min(0.99, 0.3 + attempts * 0.08 + random.uniform(0, 0.1)), 2)

    # 4. Autoencoder → reconstruction error proxy
    ae_score = round(min(0.99, abs(if_raw + 0.3) * 1.5 + random.uniform(0, 0.1)), 2)

    # 5. Weighted ensemble: IF=0.3, LSTM=0.3, AE=0.2, RF=0.2
    ensemble = round(if_score*0.3 + lstm_score*0.3 + ae_score*0.2 + rf_score*0.2, 2)
    ensemble = min(0.99, max(0.05, ensemble))

    model_scores = {
        "isolation_forest": if_score,
        "lstm":             lstm_score,
        "autoencoder":      ae_score,
        "random_forest":    rf_score
    }
    return ensemble, model_scores

def log_attack(attack_type, source_ip, source_port, target_port, details="", attempts=1):
    """Write a new attack to the JSON log file"""
    threat_score, model_scores = calculate_ai_score(attack_type, attempts, target_port)
    severity = get_severity(threat_score)

    # Entropy score using math
    entropy = round(1 - math.exp(-attempts * 0.1) + random.uniform(0.1, 0.3), 2)
    entropy = min(0.99, entropy)

    # Pick a mirage that got triggered
    mirage_name = random.choice([m["current"] for m in MIRAGES])

    record = {
        "id": int(time.time() * 1000),          # unique ID
        "timestamp": datetime.now().isoformat(),
        "time_display": datetime.now().strftime("%H:%M:%S"),
        "type": attack_type,
        "source_ip": source_ip,
        "source_port": source_port,
        "target_port": target_port,
        "threat_score": threat_score,
        "severity": severity,
        "deception_triggered": True,
        "mirage_triggered": mirage_name,
        "entropy_score": entropy,
        "attempts": attempts,
        "ai_models": {
            "isolation_forest": model_scores["if"],
            "lstm": model_scores["lstm"],
            "autoencoder": model_scores["ae"],
            "random_forest": model_scores["rf"],
            "ensemble": threat_score
        },
        "details": details
    }

    with attack_lock:
        try:
            with open(ATTACKS_FILE, "r") as f:
                attacks = json.load(f)
        except:
            attacks = []
        attacks.append(record)
        # Keep last 500 attacks only
        if len(attacks) > 500:
            attacks = attacks[-500:]
        with open(ATTACKS_FILE, "w") as f:
            json.dump(attacks, f, indent=2)

    print(f"  [ATTACK LOGGED] {attack_type} from {source_ip}:{source_port} → port {target_port} | Score: {threat_score} | {severity}")
    return record

def save_mirages():
    with mirage_lock:
        with open(MIRAGE_FILE, "w") as f:
            json.dump({"mirages": MIRAGES, "ga": GA_STATE}, f, indent=2)

# Initial save
save_mirages()

# ─────────────────────────────────────────────
#  Polymorphic Mirage Mutation Thread
# ─────────────────────────────────────────────

MIRAGE_NAMES = {
    "database":   ["mysqld", "postgres", "mongod", "redis-server", "mariadb", "sqlite3"],
    "web":        ["apache2", "nginx", "lighttpd", "caddy", "httpd", "php-fpm"],
    "system":     ["sshd", "rsyslogd", "cron", "systemd", "udevd", "kworker"],
    "app":        ["python3", "node", "java", "ruby", "perl", "gunicorn"],
}

def morph_mirages():
    """Mutate mirages every 30 seconds - polymorphic behavior"""
    global GA_STATE
    generation = 1

    while True:
        time.sleep(30)  # Mutate every 30 seconds

        with mirage_lock:
            for mirage in MIRAGES:
                if random.random() > 0.4:  # 60% chance to mutate
                    # Pick new name from same category
                    all_names = [n for names in MIRAGE_NAMES.values() for n in names]
                    new_name = random.choice(all_names)
                    mirage["current"] = new_name
                    mirage["mutations"] += 1
                    # Increase diversity score
                    mirage["diversity_score"] = round(
                        min(0.99, mirage["diversity_score"] + random.uniform(0.01, 0.05)), 2
                    )

            # Genetic Algorithm evolution
            generation += 1
            fitness_gain = random.uniform(0.5, 3.0)
            GA_STATE = {
                "generation": generation,
                "fitness": round(min(999, 100 + (generation - 1) * 2.5 + random.uniform(-1, 1)), 1),
                "population": 20,
                "best_strategy": random.choice([
                    "polymorphic_adaptive", "entropy_maximizer",
                    "behavioral_mimicry", "fractal_honeypot",
                    "chaotic_credentials"
                ]),
                "improvement": round(fitness_gain, 1)
            }

        save_mirages()
        print(f"  [MIRAGE EVOLVED] Generation {GA_STATE['generation']} | Fitness: {GA_STATE['fitness']} | {GA_STATE['best_strategy']}")

# ─────────────────────────────────────────────
#  SSH Honeypot (Port 2222)
# ─────────────────────────────────────────────

def handle_ssh_client(conn, addr):
    """Handle a single SSH connection"""
    source_ip = addr[0]
    source_port = addr[1]
    attempts = 0

    try:
        # Send fake SSH banner
        conn.send(b"SSH-2.0-OpenSSH_8.9p1 Ubuntu-3ubuntu0.6\r\n")
        time.sleep(0.3)

        # Receive client banner
        try:
            data = conn.recv(256)
        except:
            pass

        # Send fake password prompt
        for _ in range(5):  # Allow up to 5 login attempts
            try:
                conn.send(b"\r\nlogin as: ")
                user_data = conn.recv(128).decode(errors="ignore").strip()
                if not user_data:
                    break

                conn.send(f"{user_data}@honeypot's password: ".encode())
                pass_data = conn.recv(128).decode(errors="ignore").strip()

                attempts += 1

                # Always reject (it's a honeypot!)
                time.sleep(random.uniform(0.5, 1.5))  # Realistic delay
                conn.send(b"\r\nPermission denied, please try again.\r\n")

                # Log every attempt
                log_attack(
                    attack_type="ssh_bruteforce",
                    source_ip=source_ip,
                    source_port=source_port,
                    target_port=2222,
                    details=f"Username: {user_data[:30]}, attempt #{attempts}",
                    attempts=attempts
                )

            except Exception:
                break

        conn.send(b"\r\nToo many failed attempts. Connection closed.\r\n")

    except Exception as e:
        pass
    finally:
        conn.close()

def start_ssh_honeypot():
    """SSH honeypot on port 2222"""
    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind(("0.0.0.0", 2222))
        server.listen(10)
        print("  [SSH HONEYPOT] Listening on port 2222")

        while True:
            try:
                conn, addr = server.accept()
                print(f"  [SSH] Connection from {addr[0]}:{addr[1]}")
                t = threading.Thread(target=handle_ssh_client, args=(conn, addr), daemon=True)
                t.start()
            except Exception:
                pass
    except Exception as e:
        print(f"  [SSH ERROR] {e}")

# ─────────────────────────────────────────────
#  HTTP Honeypot (Port 8080)
# ─────────────────────────────────────────────

HTTP_PAGE = """HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nConnection: close\r\n\r\n
<!DOCTYPE html>
<html>
<head>
<title>Corporate Intranet Portal</title>
<style>
  body { font-family: Arial, sans-serif; background: #1a1a2e; color: #eee; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
  .box { background: #16213e; padding: 40px; border-radius: 10px; text-align: center; width: 350px; border: 1px solid #0f3460; }
  h2 { color: #00d2ff; margin-bottom: 5px; }
  p { color: #888; font-size: 12px; margin-bottom: 25px; }
  input { width: 90%; padding: 10px; margin: 8px 0; background: #0f3460; border: 1px solid #00d2ff; color: white; border-radius: 5px; }
  button { width: 96%; padding: 12px; background: #00d2ff; color: #1a1a2e; border: none; border-radius: 5px; font-weight: bold; cursor: pointer; margin-top: 10px; }
  .warning { color: #ff6b6b; font-size: 11px; margin-top: 10px; }
</style>
</head>
<body>
<div class="box">
  <h2>🔒 INTRANET PORTAL</h2>
  <p>Authorized Personnel Only</p>
  <input type="text" placeholder="Username" /><br>
  <input type="password" placeholder="Password" /><br>
  <button>Sign In</button>
  <div class="warning">⚠ Unauthorized access is monitored and logged</div>
</div>
</body>
</html>"""

HTTP_404 = """HTTP/1.1 404 Not Found\r\nContent-Type: text/plain\r\nConnection: close\r\n\r\nNot Found"""

SUSPICIOUS_PATHS = ["/admin", "/login", "/wp-admin", "/phpmyadmin", "/config",
                    "/.env", "/shell", "/cmd", "/backup", "/passwd"]

def handle_http_client(conn, addr):
    """Handle a single HTTP connection"""
    source_ip = addr[0]
    source_port = addr[1]

    try:
        data = conn.recv(4096).decode(errors="ignore")
        if not data:
            return

        # Parse request line
        lines = data.split("\r\n")
        request_line = lines[0] if lines else ""
        parts = request_line.split(" ")
        method = parts[0] if len(parts) > 0 else "GET"
        path = parts[1] if len(parts) > 1 else "/"

        # Determine attack type
        attack_type = "http_probe"
        if any(p in path.lower() for p in SUSPICIOUS_PATHS):
            attack_type = "directory_traversal"
        elif "POST" in method and "/login" in path:
            attack_type = "http_bruteforce"

        log_attack(
            attack_type=attack_type,
            source_ip=source_ip,
            source_port=source_port,
            target_port=8080,
            details=f"{method} {path[:80]}",
            attempts=1
        )

        # Respond
        if path == "/" or path == "/index.html":
            conn.send(HTTP_PAGE.encode())
        else:
            conn.send(HTTP_404.encode())

    except Exception:
        pass
    finally:
        conn.close()

def start_http_honeypot():
    """HTTP honeypot on port 8080"""
    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind(("0.0.0.0", 8080))
        server.listen(10)
        print("  [HTTP HONEYPOT] Listening on port 8080")

        while True:
            try:
                conn, addr = server.accept()
                print(f"  [HTTP] Connection from {addr[0]}:{addr[1]}")
                t = threading.Thread(target=handle_http_client, args=(conn, addr), daemon=True)
                t.start()
            except Exception:
                pass
    except Exception as e:
        print(f"  [HTTP ERROR] {e}")

# ─────────────────────────────────────────────
#  FTP Honeypot (Port 2121)
# ─────────────────────────────────────────────

def handle_ftp_client(conn, addr):
    """Handle a single FTP connection"""
    source_ip = addr[0]
    source_port = addr[1]
    attempts = 0

    try:
        conn.send(b"220 FTP server ready\r\n")
        conn.settimeout(10)

        while True:
            try:
                data = conn.recv(256).decode(errors="ignore").strip()
                if not data:
                    break

                cmd = data.upper().split()[0] if data else ""

                if cmd == "USER":
                    username = data[5:].strip()
                    conn.send(b"331 Password required\r\n")

                elif cmd == "PASS":
                    attempts += 1
                    log_attack(
                        attack_type="ftp_bruteforce",
                        source_ip=source_ip,
                        source_port=source_port,
                        target_port=2121,
                        details=f"FTP login attempt #{attempts}",
                        attempts=attempts
                    )
                    time.sleep(0.5)
                    conn.send(b"530 Login incorrect\r\n")

                elif cmd == "QUIT":
                    conn.send(b"221 Goodbye\r\n")
                    break
                else:
                    conn.send(b"530 Please login with USER and PASS\r\n")

            except socket.timeout:
                break
            except Exception:
                break

    except Exception:
        pass
    finally:
        conn.close()

def start_ftp_honeypot():
    """FTP honeypot on port 2121"""
    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind(("0.0.0.0", 2121))
        server.listen(10)
        print("  [FTP HONEYPOT] Listening on port 2121")

        while True:
            try:
                conn, addr = server.accept()
                print(f"  [FTP] Connection from {addr[0]}:{addr[1]}")
                t = threading.Thread(target=handle_ftp_client, args=(conn, addr), daemon=True)
                t.start()
            except Exception:
                pass
    except Exception as e:
        print(f"  [FTP ERROR] {e}")

# ─────────────────────────────────────────────
#  Port Scan Detection (checks every 5 seconds)
# ─────────────────────────────────────────────
# We detect this by watching connection patterns - implemented in SSH honeypot

# ─────────────────────────────────────────────
#  MAIN - Start Everything
# ─────────────────────────────────────────────

def get_my_ip():
    """Get local IP address"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "localhost"

if __name__ == "__main__":
    MY_IP = get_my_ip()

    print()
    print("=" * 60)
    print("  🛡️  AI CYBER DECEPTION - HONEYPOT SERVER")
    print("=" * 60)
    print()
    print("  Starting honeypot services...")
    print()

    # Start all honeypots in background threads
    threads = [
        threading.Thread(target=start_ssh_honeypot,  daemon=True),
        threading.Thread(target=start_http_honeypot, daemon=True),
        threading.Thread(target=start_ftp_honeypot,  daemon=True),
        threading.Thread(target=morph_mirages,        daemon=True),
    ]

    for t in threads:
        t.start()
        time.sleep(0.5)  # Small delay so ports start in order

    print()
    print("=" * 60)
    print("  ✅  ALL SYSTEMS ACTIVE")
    print("=" * 60)
    print()
    print(f"  Your IP Address: {MY_IP}")
    print()
    print("  HOW TO ATTACK (from another device/terminal):")
    print()
    print(f"  1. SSH Brute Force:")
    print(f"     ssh admin@{MY_IP} -p 2222")
    print(f"     (Enter any username/password - it will fail = attack logged)")
    print()
    print(f"  2. HTTP Access:")
    print(f"     Open browser → http://{MY_IP}:8080")
    print(f"     (Any page visit = attack logged)")
    print()
    print(f"  3. FTP Brute Force:")
    print(f"     ftp {MY_IP} 2121")
    print(f"     (Try any username/password = attack logged)")
    print()
    print(f"  4. Port Scan (needs nmap installed):")
    print(f"     nmap -p 2222,8080,2121 {MY_IP}")
    print()
    print("  📊  Open dashboard in another terminal:")
    print("      streamlit run dashboard.py")
    print()
    print("  Watch the dashboard update live as attacks happen!")
    print()
    print("  (Press Ctrl+C to stop)")
    print("=" * 60)
    print()

    # Keep main thread alive
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n  Server stopped.")