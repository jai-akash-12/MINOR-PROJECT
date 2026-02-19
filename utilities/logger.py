"""
Logging utility for AI Cyber Deception System
Comprehensive logging for all system components
"""

import logging
import sys
from pathlib import Path
from logging.handlers import RotatingFileHandler
from datetime import datetime
import json

# Import config
import sys
sys.path.append(str(Path(__file__).parent.parent))
from utilities.config import LOGGING_CONFIG, LOGS_DIR


class CyberDeceptionLogger:
    """
    Centralized logging system for all components
    """
    
    _instances = {}
    
    def __new__(cls, name):
        if name not in cls._instances:
            cls._instances[name] = super(CyberDeceptionLogger, cls).__new__(cls)
        return cls._instances[name]
    
    def __init__(self, name):
        if hasattr(self, 'logger'):
            return
            
        self.logger = logging.getLogger(name)
        self.logger.setLevel(getattr(logging, LOGGING_CONFIG['level']))
        
        # Clear existing handlers
        self.logger.handlers = []
        
        # Create formatters
        self.formatter = logging.Formatter(LOGGING_CONFIG['format'])
        
        # Console handler
        if LOGGING_CONFIG['console_logging']:
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setFormatter(self.formatter)
            self.logger.addHandler(console_handler)
        
        # File handler with rotation
        if LOGGING_CONFIG['file_logging']:
            log_file = LOGS_DIR / f"{name}.log"
            file_handler = RotatingFileHandler(
                log_file,
                maxBytes=LOGGING_CONFIG['max_file_size'],
                backupCount=LOGGING_CONFIG['backup_count']
            )
            file_handler.setFormatter(self.formatter)
            self.logger.addHandler(file_handler)
    
    def info(self, message):
        self.logger.info(message)
    
    def warning(self, message):
        self.logger.warning(message)
    
    def error(self, message):
        self.logger.error(message)
    
    def critical(self, message):
        self.logger.critical(message)
    
    def debug(self, message):
        self.logger.debug(message)


class AttackLogger:
    """
    Specialized logger for attack events and interactions
    """
    
    def __init__(self):
        self.logger = CyberDeceptionLogger('attack_events')
        self.attack_log_file = LOGS_DIR / "attack_events.jsonl"
    
    def log_attack(self, attack_data):
        """
        Log attack event with structured data
        """
        attack_record = {
            'timestamp': datetime.now().isoformat(),
            'attack_type': attack_data.get('type', 'unknown'),
            'source_ip': attack_data.get('source_ip', 'unknown'),
            'target': attack_data.get('target', 'unknown'),
            'severity': attack_data.get('severity', 'MEDIUM'),
            'threat_score': attack_data.get('threat_score', 0.0),
            'deception_triggered': attack_data.get('deception_triggered', False),
            'ai_detection': attack_data.get('ai_detection', {}),
            'details': attack_data.get('details', {})
        }
        
        # Log to file
        self.logger.info(f"Attack detected: {attack_record['attack_type']} from {attack_record['source_ip']}")
        
        # Write structured log
        with open(self.attack_log_file, 'a') as f:
            f.write(json.dumps(attack_record) + '\n')
        
        return attack_record


class DeceptionLogger:
    """
    Specialized logger for deception activities
    """
    
    def __init__(self):
        self.logger = CyberDeceptionLogger('deception_events')
        self.deception_log_file = LOGS_DIR / "deception_events.jsonl"
    
    def log_mirage_mutation(self, mirage_data):
        """
        Log polymorphic process mirage mutations
        """
        mutation_record = {
            'timestamp': datetime.now().isoformat(),
            'mirage_id': mirage_data.get('id', 'unknown'),
            'mutation_type': mirage_data.get('mutation_type', 'unknown'),
            'genetic_diversity_score': mirage_data.get('diversity_score', 0.0),
            'attacker_interactions': mirage_data.get('interactions', 0),
            'details': mirage_data.get('details', {})
        }
        
        self.logger.info(f"Mirage mutation: {mutation_record['mirage_id']} - {mutation_record['mutation_type']}")
        
        with open(self.deception_log_file, 'a') as f:
            f.write(json.dumps(mutation_record) + '\n')
        
        return mutation_record
    
    def log_genetic_evolution(self, ga_data):
        """
        Log genetic algorithm evolution events
        """
        ga_record = {
            'timestamp': datetime.now().isoformat(),
            'generation': ga_data.get('generation', 0),
            'best_fitness': ga_data.get('best_fitness', 0.0),
            'avg_fitness': ga_data.get('avg_fitness', 0.0),
            'best_chromosome': ga_data.get('best_chromosome', {}),
            'improvement': ga_data.get('improvement', 0.0)
        }
        
        self.logger.info(f"GA Generation {ga_record['generation']}: Fitness = {ga_record['best_fitness']:.2f}")
        
        with open(self.deception_log_file, 'a') as f:
            f.write(json.dumps(ga_record) + '\n')
        
        return ga_record


class MetricsLogger:
    """
    Performance and research metrics logger
    """
    
    def __init__(self):
        self.logger = CyberDeceptionLogger('metrics')
        self.metrics_log_file = LOGS_DIR / "metrics.jsonl"
    
    def log_metrics(self, metrics_data):
        """
        Log system performance and research metrics
        """
        metrics_record = {
            'timestamp': datetime.now().isoformat(),
            'detection_accuracy': metrics_data.get('detection_accuracy', 0.0),
            'deception_effectiveness': metrics_data.get('deception_effectiveness', 0.0),
            'false_positive_rate': metrics_data.get('false_positive_rate', 0.0),
            'mean_time_to_detect': metrics_data.get('mttd', 0.0),
            'attacker_engagement_time': metrics_data.get('engagement_time', 0.0),
            'genetic_diversity': metrics_data.get('genetic_diversity', 0.0),
            'system_resources': metrics_data.get('resources', {})
        }
        
        with open(self.metrics_log_file, 'a') as f:
            f.write(json.dumps(metrics_record) + '\n')
        
        return metrics_record


# Convenience functions
def get_logger(name):
    """Get or create a logger instance"""
    return CyberDeceptionLogger(name)


def log_attack(attack_data):
    """Quick attack logging"""
    return AttackLogger().log_attack(attack_data)


def log_deception(deception_data):
    """Quick deception logging"""
    return DeceptionLogger().log_mirage_mutation(deception_data)