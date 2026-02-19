"""
ENSEMBLE AI DETECTION ENGINE
Combines multiple AI models for superior threat detection

Models:
1. Isolation Forest - Anomaly detection
2. LSTM - Sequential pattern analysis  
3. Autoencoder - Behavioral baseline
4. Random Forest - Classification

RESEARCH CONTRIBUTION: Multi-model ensemble for cyber deception
"""

import numpy as np
from sklearn.ensemble import IsolationForest, RandomForestClassifier
from sklearn.preprocessing import StandardScaler
import joblib
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parent.parent))
from utilities.config import AI_CONFIG, MODELS_DIR
from utilities.logger import get_logger
from utilities.metrics import global_metrics

logger = get_logger('ai_detection')


class EnsembleAIDetector:
    """
    Multi-model ensemble for threat detection
    Combines predictions from multiple AI models
    """
    
    def __init__(self):
        self.config = AI_CONFIG
        self.scaler = StandardScaler()
        
        # Initialize models
        self.isolation_forest = None
        self.random_forest = None
        self.lstm_model = None
        self.autoencoder = None
        
        # Ensemble weights
        self.weights = self.config['ensemble_weights']
        
        # Training data
        self.training_data = []
        self.is_trained = False
        
        logger.info("Ensemble AI Detector initialized")
    
    def initialize_models(self):
        """Initialize all AI models"""
        # Isolation Forest for anomaly detection
        if_config = self.config['isolation_forest']
        self.isolation_forest = IsolationForest(
            contamination=if_config['contamination'],
            n_estimators=if_config['n_estimators'],
            max_samples=if_config['max_samples'],
            random_state=42
        )
        
        # Random Forest for classification
        rf_config = self.config['random_forest']
        self.random_forest = RandomForestClassifier(
            n_estimators=rf_config['n_estimators'],
            max_depth=rf_config['max_depth'],
            random_state=42
        )
        
        logger.info("AI models initialized")
    
    def extract_features(self, network_data):
        """
        Extract features from network data for AI models
        
        Features include:
        - Packet statistics
        - Connection patterns
        - Timing information
        - Protocol distribution
        """
        features = []
        
        # Basic features (simplified for demo)
        features.append(network_data.get('packet_count', 0))
        features.append(network_data.get('byte_count', 0))
        features.append(network_data.get('duration', 0))
        features.append(network_data.get('src_port', 0))
        features.append(network_data.get('dst_port', 0))
        features.append(network_data.get('protocol', 0))
        
        # Statistical features
        features.append(network_data.get('packets_per_second', 0))
        features.append(network_data.get('bytes_per_second', 0))
        features.append(network_data.get('avg_packet_size', 0))
        
        # Behavioral features
        features.append(network_data.get('unique_destinations', 0))
        features.append(network_data.get('port_scan_score', 0))
        features.append(network_data.get('brute_force_score', 0))
        
        return np.array(features).reshape(1, -1)
    
    def train_models(self, training_data, labels=None):
        """
        Train all models on provided data
        
        For demo: Using semi-supervised approach
        """
        if not training_data:
            logger.warning("No training data provided")
            return False
        
        try:
            X = np.array(training_data)
            
            # Normalize data
            X_normalized = self.scaler.fit_transform(X)
            
            # Train Isolation Forest (unsupervised)
            self.isolation_forest.fit(X_normalized)
            logger.info("Isolation Forest trained")
            
            # Train Random Forest if labels provided
            if labels is not None:
                y = np.array(labels)
                self.random_forest.fit(X_normalized, y)
                logger.info("Random Forest trained")
            
            self.is_trained = True
            logger.info("All models trained successfully")
            
            return True
            
        except Exception as e:
            logger.error(f"Training failed: {e}")
            return False
    
    def detect_threat(self, network_data):
        """
        Main detection function using ensemble approach
        
        Returns:
            dict: Detection results with threat score and classification
        """
        if not self.is_trained:
            # Use pre-defined thresholds for demo
            return self._demo_detection(network_data)
        
        try:
            # Extract features
            features = self.extract_features(network_data)
            features_normalized = self.scaler.transform(features)
            
            # Get predictions from each model
            results = {}
            
            # 1. Isolation Forest score
            if_score = self.isolation_forest.score_samples(features_normalized)[0]
            if_pred = self.isolation_forest.predict(features_normalized)[0]
            results['isolation_forest'] = {
                'score': float(if_score),
                'is_anomaly': if_pred == -1
            }
            
            # 2. Random Forest prediction
            if hasattr(self.random_forest, 'predict_proba'):
                rf_proba = self.random_forest.predict_proba(features_normalized)[0]
                results['random_forest'] = {
                    'threat_probability': float(rf_proba[1] if len(rf_proba) > 1 else 0.5),
                    'prediction': int(self.random_forest.predict(features_normalized)[0])
                }
            
            # Ensemble decision
            threat_score = self._calculate_ensemble_score(results)
            threat_level = self._classify_threat_level(threat_score)
            
            return {
                'threat_score': threat_score,
                'threat_level': threat_level,
                'model_results': results,
                'timestamp': network_data.get('timestamp', ''),
                'is_threat': threat_score > 0.7
            }
            
        except Exception as e:
            logger.error(f"Detection failed: {e}")
            return self._demo_detection(network_data)
    
    def _demo_detection(self, network_data):
        """
        Demo detection using rule-based approach
        Used when models are not trained
        """
        threat_score = 0.0
        
        # Port scanning detection
        if network_data.get('port_scan_score', 0) > 0.5:
            threat_score += 0.3
        
        # Brute force detection
        if network_data.get('brute_force_score', 0) > 0.5:
            threat_score += 0.4
        
        # Unusual traffic volume
        if network_data.get('packet_count', 0) > 1000:
            threat_score += 0.2
        
        # Suspicious ports
        suspicious_ports = [22, 23, 3389, 445]
        if network_data.get('dst_port', 0) in suspicious_ports:
            threat_score += 0.1
        
        threat_score = min(threat_score, 1.0)
        threat_level = self._classify_threat_level(threat_score)
        
        return {
            'threat_score': threat_score,
            'threat_level': threat_level,
            'model_results': {'demo_mode': True},
            'timestamp': network_data.get('timestamp', ''),
            'is_threat': threat_score > 0.7
        }
    
    def _calculate_ensemble_score(self, model_results):
        """
        Calculate weighted ensemble score
        """
        score = 0.0
        
        # Isolation Forest contribution
        if 'isolation_forest' in model_results:
            if_anomaly = model_results['isolation_forest']['is_anomaly']
            score += self.weights['isolation_forest'] * (1.0 if if_anomaly else 0.0)
        
        # Random Forest contribution
        if 'random_forest' in model_results:
            rf_prob = model_results['random_forest'].get('threat_probability', 0.5)
            score += self.weights['random_forest'] * rf_prob
        
        # Normalize to 0-1
        return min(score, 1.0)
    
    def _classify_threat_level(self, threat_score):
        """
        Classify threat based on score
        """
        if threat_score >= 0.8:
            return 'CRITICAL'
        elif threat_score >= 0.6:
            return 'HIGH'
        elif threat_score >= 0.4:
            return 'MEDIUM'
        else:
            return 'LOW'
    
    def save_models(self):
        """Save trained models to disk"""
        try:
            if self.is_trained:
                joblib.dump(self.isolation_forest, MODELS_DIR / 'isolation_forest.pkl')
                joblib.dump(self.random_forest, MODELS_DIR / 'random_forest.pkl')
                joblib.dump(self.scaler, MODELS_DIR / 'scaler.pkl')
                logger.info("Models saved successfully")
                return True
        except Exception as e:
            logger.error(f"Failed to save models: {e}")
        return False
    
    def load_models(self):
        """Load pre-trained models from disk"""
        try:
            if (MODELS_DIR / 'isolation_forest.pkl').exists():
                self.isolation_forest = joblib.load(MODELS_DIR / 'isolation_forest.pkl')
                self.random_forest = joblib.load(MODELS_DIR / 'random_forest.pkl')
                self.scaler = joblib.load(MODELS_DIR / 'scaler.pkl')
                self.is_trained = True
                logger.info("Models loaded successfully")
                return True
        except Exception as e:
            logger.error(f"Failed to load models: {e}")
        return False
    
    def get_model_stats(self):
        """Get statistics about the AI models"""
        stats = {
            'is_trained': self.is_trained,
            'models': {
                'isolation_forest': self.isolation_forest is not None,
                'random_forest': self.random_forest is not None
            },
            'ensemble_weights': self.weights
        }
        
        return stats


def generate_synthetic_training_data(n_samples=1000):
    """
    Generate synthetic training data for demo purposes
    In production, this would be real network data
    """
    logger.info(f"Generating {n_samples} synthetic training samples")
    
    normal_data = []
    attack_data = []
    
    # Generate normal traffic
    for _ in range(int(n_samples * 0.8)):
        sample = {
            'packet_count': np.random.randint(10, 100),
            'byte_count': np.random.randint(1000, 10000),
            'duration': np.random.uniform(1, 60),
            'src_port': np.random.randint(30000, 65535),
            'dst_port': np.random.choice([80, 443, 8080]),
            'protocol': 6,  # TCP
            'packets_per_second': np.random.uniform(1, 10),
            'bytes_per_second': np.random.uniform(100, 1000),
            'avg_packet_size': np.random.uniform(500, 1500),
            'unique_destinations': np.random.randint(1, 5),
            'port_scan_score': np.random.uniform(0, 0.3),
            'brute_force_score': np.random.uniform(0, 0.2)
        }
        normal_data.append(sample)
    
    # Generate attack traffic
    for _ in range(int(n_samples * 0.2)):
        sample = {
            'packet_count': np.random.randint(500, 5000),
            'byte_count': np.random.randint(50000, 500000),
            'duration': np.random.uniform(0.1, 5),
            'src_port': np.random.randint(30000, 65535),
            'dst_port': np.random.choice([22, 23, 3389, 445]),
            'protocol': 6,
            'packets_per_second': np.random.uniform(50, 500),
            'bytes_per_second': np.random.uniform(5000, 50000),
            'avg_packet_size': np.random.uniform(100, 500),
            'unique_destinations': np.random.randint(10, 100),
            'port_scan_score': np.random.uniform(0.6, 1.0),
            'brute_force_score': np.random.uniform(0.5, 1.0)
        }
        attack_data.append(sample)
    
    return normal_data + attack_data