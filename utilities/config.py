"""
Configuration file for AI Cyber Deception and SOC Monitoring System
All system parameters and settings
"""

import os
from pathlib import Path

# Base paths
BASE_DIR = Path(__file__).resolve().parent.parent
LOGS_DIR = BASE_DIR / "logs"
DATA_DIR = BASE_DIR / "data"
MODELS_DIR = BASE_DIR / "models"

# Create directories if they don't exist
for directory in [LOGS_DIR, DATA_DIR, MODELS_DIR]:
    directory.mkdir(exist_ok=True)

# Polymorphic Process Mirage Configuration
MIRAGE_CONFIG = {
    'mutation_interval': 30,  # seconds between mutations
    'max_active_mirages': 15,
    'process_types': ['database', 'web_server', 'ssh_daemon', 'backup_service', 
                     'cache_server', 'api_gateway', 'file_server', 'mail_server'],
    'mutation_strategies': ['name', 'memory', 'cpu', 'network', 'files'],
    'genetic_diversity_threshold': 0.5
}

# Genetic Algorithm Configuration
GA_CONFIG = {
    'population_size': 20,
    'max_generations': 100,
    'mutation_rate': 0.2,
    'crossover_rate': 0.8,
    'elite_size': 4,  # Top performers to preserve
    'fitness_weights': {
        'engagement_time': 0.3,
        'data_quality': 0.25,
        'confusion_score': 0.25,
        'genetic_diversity': 0.2
    }
}

# Mathematical Deception Configuration
MATH_DECEPTION_CONFIG = {
    'fractal_depth': 4,
    'chaos_parameter': 3.9,  # Logistic map parameter (chaotic regime)
    'fibonacci_services': True,
    'entropy_threshold': 0.7,
    'lsystem_rules': {
        'F': 'F[+D][-D]F',
        'D': 'DD[+F]'
    }
}

# AI Detection Models Configuration
AI_CONFIG = {
    'isolation_forest': {
        'contamination': 0.1,
        'n_estimators': 100,
        'max_samples': 256
    },
    'lstm': {
        'sequence_length': 50,
        'hidden_units': 64,
        'epochs': 50,
        'batch_size': 32
    },
    'autoencoder': {
        'encoding_dim': 32,
        'epochs': 100,
        'batch_size': 32
    },
    'random_forest': {
        'n_estimators': 100,
        'max_depth': 20
    },
    'ensemble_weights': {
        'isolation_forest': 0.3,
        'lstm': 0.3,
        'autoencoder': 0.2,
        'random_forest': 0.2
    }
}

# Honeypot Configuration
HONEYPOT_CONFIG = {
    'services': {
        'ssh': {'port': 2222, 'enabled': True},
        'ftp': {'port': 2121, 'enabled': True},
        'http': {'port': 8080, 'enabled': True},
        'mysql': {'port': 3307, 'enabled': True},
        'redis': {'port': 6380, 'enabled': True},
        'smtp': {'port': 2525, 'enabled': True}
    },
    'interaction_level': 'high',  # low, medium, high
    'data_collection_level': 'full'
}

# Attack Simulation Configuration
ATTACK_CONFIG = {
    'scenarios': ['port_scan', 'ssh_bruteforce', 'lateral_movement', 
                 'data_exfiltration', 'privilege_escalation', 'ddos'],
    'attacker_profiles': ['script_kiddie', 'professional', 'apt_group'],
    'simulation_duration': 300,  # seconds
    'attack_intensity': 'medium'  # low, medium, high
}

# SOC Dashboard Configuration
DASHBOARD_CONFIG = {
    'refresh_interval': 2,  # seconds
    'max_alerts_display': 50,
    'theme': 'dark',
    'real_time_update': True,
    'visualization_limit': 1000  # max data points for charts
}

# Network Monitoring Configuration
NETWORK_CONFIG = {
    'capture_interface': 'any',
    'packet_buffer_size': 1000,
    'capture_filter': '',  # BPF filter
    'feature_extraction_interval': 5,  # seconds
    'traffic_anomaly_threshold': 0.8
}

# Database Configuration
DATABASE_CONFIG = {
    'type': 'sqlite',  # sqlite or postgresql
    'name': 'cyber_deception.db',
    'path': str(DATA_DIR / 'cyber_deception.db'),
    'backup_enabled': True,
    'backup_interval': 3600  # seconds
}

# Logging Configuration
LOGGING_CONFIG = {
    'level': 'INFO',
    'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    'file_logging': True,
    'console_logging': True,
    'max_file_size': 10 * 1024 * 1024,  # 10 MB
    'backup_count': 5
}

# Alert Configuration
ALERT_CONFIG = {
    'severity_levels': ['LOW', 'MEDIUM', 'HIGH', 'CRITICAL'],
    'notification_channels': ['dashboard', 'log', 'email'],
    'auto_response_enabled': True,
    'threat_score_threshold': 0.7
}

# Performance Metrics
METRICS_CONFIG = {
    'track_cpu': True,
    'track_memory': True,
    'track_network': True,
    'track_detection_accuracy': True,
    'track_deception_effectiveness': True,
    'metrics_collection_interval': 10  # seconds
}

# Research Validation Metrics
RESEARCH_METRICS = {
    'calculate_genetic_diversity': True,
    'calculate_entropy_scores': True,
    'track_mutation_history': True,
    'measure_attacker_confusion': True,
    'benchmark_against_baseline': True
}

# Feature extraction for ML
FEATURE_CONFIG = {
    'network_features': [
        'packet_count', 'byte_count', 'duration', 'protocol',
        'src_port', 'dst_port', 'tcp_flags', 'packet_size_mean',
        'packet_size_std', 'inter_arrival_time_mean', 'inter_arrival_time_std',
        'flow_duration', 'fwd_packets', 'bwd_packets', 'fwd_bytes', 'bwd_bytes'
    ],
    'behavioral_features': [
        'login_attempts', 'failed_auth', 'commands_executed', 
        'files_accessed', 'unusual_times', 'privilege_escalation_attempts'
    ]
}

# Threat Intelligence
THREAT_INTEL_CONFIG = {
    'feeds_enabled': True,
    'update_interval': 3600,  # seconds
    'feeds': [
        'abuse.ch',
        'alienvault',
        'emergingthreats'
    ],
    'ioc_types': ['ip', 'domain', 'hash', 'url']
}

# Demo Configuration
DEMO_CONFIG = {
    'auto_start': False,
    'demo_duration': 300,  # seconds
    'attack_sequence_delay': 30,  # seconds between attacks
    'verbose_output': True,
    'save_results': True
}