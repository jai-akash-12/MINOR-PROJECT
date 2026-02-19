"""
Credential Generator
Generates believable fake credentials using mathematical deception
"""

import random
import string
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parent.parent))
from deception_layer.mathematical_deception import MathematicalDeception
from utilities.logger import get_logger

logger = get_logger('credential_generator')


class CredentialGenerator:
    """
    Generates fake but believable credentials
    Uses chaos theory for unpredictable but realistic patterns
    """
    
    def __init__(self):
        self.math_deception = MathematicalDeception()
        self.common_usernames = [
            'admin', 'administrator', 'root', 'user', 'test',
            'backup', 'support', 'webmaster', 'developer', 'manager'
        ]
    
    def generate_credential_set(self, count=20):
        """Generate a set of fake credentials"""
        credentials = []
        
        # Use chaos theory for half
        for username in random.sample(self.common_usernames, min(count//2, len(self.common_usernames))):
            chaotic_creds = self.math_deception.generate_chaotic_credentials(username, 1)
            credentials.extend(chaotic_creds)
        
        # Generate traditional ones for the rest
        remaining = count - len(credentials)
        for i in range(remaining):
            credentials.append(self._generate_traditional_credential())
        
        logger.info(f"Generated {len(credentials)} fake credentials")
        return credentials
    
    def _generate_traditional_credential(self):
        """Generate credential using traditional methods"""
        username = f"user{random.randint(100, 999)}"
        password = self._generate_password()
        
        return {
            'username': username,
            'password': password,
            'method': 'traditional'
        }
    
    def _generate_password(self, length=12):
        """Generate a strong-looking password"""
        chars = string.ascii_letters + string.digits + "!@#$%^&*()"
        return ''.join(random.choice(chars) for _ in range(length))