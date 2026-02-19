"""
MATHEMATICAL DECEPTION PRIMITIVES - CORE INNOVATION
Uses fractal geometry, chaos theory, and mathematical patterns for deception

RESEARCH NOVELTY: Almost non-existent in cybersecurity literature
- Fractal-based file systems (L-systems)
- Chaos theory for credential generation
- Fibonacci network topologies
- Shannon entropy validation
"""

import random
import numpy as np
import hashlib
from datetime import datetime
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parent.parent))
from utilities.config import MATH_DECEPTION_CONFIG
from utilities.logger import get_logger
from utilities.metrics import global_metrics

logger = get_logger('mathematical_deception')


class MathematicalDeception:
    """
    Uses mathematical and fractal principles for believable deception
    """
    
    def __init__(self):
        self.fractal_depth = MATH_DECEPTION_CONFIG['fractal_depth']
        self.chaos_parameter = MATH_DECEPTION_CONFIG['chaos_parameter']
        self.lsystem_rules = MATH_DECEPTION_CONFIG['lsystem_rules']
        self.entropy_threshold = MATH_DECEPTION_CONFIG['entropy_threshold']
        
        logger.info("Mathematical Deception system initialized")
    
    def generate_fractal_filesystem(self, root_path='/fake_data', depth=None):
        """
        INNOVATION: Generate believable directory structure using L-systems
        
        L-systems create organic, self-similar patterns like real file systems
        - F = File
        - D = Directory
        Rules simulate natural growth
        """
        if depth is None:
            depth = self.fractal_depth
        
        # Start with axiom
        axiom = "D"
        pattern = axiom
        
        # Apply L-system rules iteratively
        for iteration in range(depth):
            new_pattern = ""
            for char in pattern:
                new_pattern += self.lsystem_rules.get(char, char)
            pattern = new_pattern
        
        # Interpret pattern into actual file system structure
        filesystem = self._interpret_lsystem(pattern, root_path)
        
        logger.info(f"Generated fractal filesystem with {len(filesystem['files']) + len(filesystem['directories'])} items")
        
        return filesystem
    
    def _interpret_lsystem(self, pattern, root_path):
        """
        Convert L-system string into actual file/directory structure
        
        Grammar:
        D = Directory (creates subdirectory)
        F = File (creates file)
        [+...] = Branch into subdirectory
        [-...] = Branch into sibling directory
        """
        filesystem = {
            'root': root_path,
            'directories': [],
            'files': [],
            'structure': {}
        }
        
        current_path = root_path
        depth_stack = [root_path]
        dir_counter = 0
        file_counter = 0
        
        i = 0
        while i < len(pattern):
            char = pattern[i]
            
            if char == 'D':
                # Create directory
                dir_name = self._generate_directory_name(dir_counter)
                dir_path = f"{current_path}/{dir_name}"
                filesystem['directories'].append(dir_path)
                dir_counter += 1
                
            elif char == 'F':
                # Create file
                file_name = self._generate_file_name(file_counter)
                file_path = f"{current_path}/{file_name}"
                filesystem['files'].append(file_path)
                file_counter += 1
                
            elif char == '[':
                # Branch into subdirectory
                if filesystem['directories']:
                    current_path = filesystem['directories'][-1]
                    depth_stack.append(current_path)
                
            elif char == ']':
                # Return to parent
                if len(depth_stack) > 1:
                    depth_stack.pop()
                    current_path = depth_stack[-1]
            
            i += 1
        
        # Calculate entropy of structure
        structure_entropy = global_metrics.calculate_entropy(str(filesystem['files']))
        filesystem['entropy_score'] = structure_entropy
        
        logger.debug(f"Filesystem entropy: {structure_entropy:.3f}")
        
        return filesystem
    
    def _generate_directory_name(self, counter):
        """Generate realistic directory names"""
        prefixes = ['data', 'config', 'backup', 'cache', 'logs', 'temp', 'archive', 'reports']
        suffixes = ['prod', 'dev', 'staging', 'old', 'new', 'v2', '2024', '2025']
        
        if random.random() < 0.3:
            return f"{random.choice(prefixes)}_{random.choice(suffixes)}_{counter}"
        else:
            return f"{random.choice(prefixes)}_{counter}"
    
    def _generate_file_name(self, counter):
        """Generate realistic file names"""
        prefixes = ['database', 'config', 'secret', 'key', 'backup', 'dump', 'export', 'log']
        extensions = ['.db', '.conf', '.sql', '.txt', '.json', '.xml', '.csv', '.key']
        
        timestamp = f"{random.randint(2020, 2025)}{random.randint(1,12):02d}{random.randint(1,28):02d}"
        
        return f"{random.choice(prefixes)}_{timestamp}_{counter}{random.choice(extensions)}"
    
    def generate_chaotic_credentials(self, seed_username, count=10):
        """
        INNOVATION: Use chaos theory to generate realistic credentials
        
        Logistic Map: x_{n+1} = r * x_n * (1 - x_n)
        - When r ≈ 3.9, system exhibits chaotic behavior
        - Generates unpredictable but deterministic sequences
        - Appears human-generated but mathematically derived
        """
        r = self.chaos_parameter
        
        # Initial condition from username hash
        x = (int(hashlib.md5(seed_username.encode()).hexdigest(), 16) % 10000) / 10000.0
        
        credentials = []
        
        for i in range(count):
            # Iterate logistic map
            x = r * x * (1 - x)
            
            # Generate password from chaotic value
            password_length = int(8 + x * 8)  # 8-16 characters
            password = self._chaotic_string_generator(x, password_length)
            
            # Generate username variation
            username_variation = self._chaotic_username_variant(seed_username, x, i)
            
            # Calculate entropy of password
            password_entropy = global_metrics.calculate_entropy(password)
            
            credentials.append({
                'username': username_variation,
                'password': password,
                'chaos_value': x,
                'entropy': password_entropy,
                'strength': 'strong' if password_entropy > 3.5 else 'medium'
            })
        
        logger.info(f"Generated {count} chaotic credentials with avg entropy {np.mean([c['entropy'] for c in credentials]):.3f}")
        
        return credentials
    
    def _chaotic_string_generator(self, chaos_value, length):
        """Generate password string from chaotic value"""
        # Character sets
        lowercase = 'abcdefghijklmnopqrstuvwxyz'
        uppercase = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        digits = '0123456789'
        special = '!@#$%^&*()_+-=[]{}|;:,.<>?'
        
        all_chars = lowercase + uppercase + digits + special
        
        # Use chaos value to seed deterministic generation
        rng = random.Random(int(chaos_value * 1000000))
        
        password = ''.join(rng.choice(all_chars) for _ in range(length))
        
        return password
    
    def _chaotic_username_variant(self, base_username, chaos_value, iteration):
        """Generate username variants using chaos"""
        variations = [
            f"{base_username}",
            f"{base_username}{iteration}",
            f"{base_username}_admin",
            f"{base_username}_backup",
            f"admin_{base_username}",
            f"{base_username}_prod",
            f"{base_username}_{int(chaos_value * 1000)}",
            f"user_{base_username}",
        ]
        
        # Use chaos value to select
        index = int(chaos_value * len(variations)) % len(variations)
        return variations[index]
    
    def generate_fibonacci_network_topology(self):
        """
        INNOVATION: Network services distributed by Fibonacci sequence
        
        Makes the network appear organically grown (like real networks)
        instead of artificially planned (like honeypots)
        """
        fibonacci = self._generate_fibonacci(8)
        
        service_types = ['web', 'database', 'cache', 'api', 'storage', 'compute', 'message_queue', 'analytics']
        
        topology = {}
        
        for i, (service, fib_count) in enumerate(zip(service_types, fibonacci)):
            base_port = 8000 + i * 1000
            
            topology[service] = {
                'instance_count': fib_count,
                'port_base': base_port,
                'ports': [base_port + j for j in range(fib_count)],
                'fibonacci_value': fib_count,
                'distribution': 'fibonacci'
            }
        
        logger.info(f"Generated Fibonacci network topology with {sum(fibonacci)} total services")
        
        return topology
    
    def _generate_fibonacci(self, n):
        """Generate Fibonacci sequence"""
        if n <= 0:
            return []
        elif n == 1:
            return [1]
        elif n == 2:
            return [1, 1]
        
        fib = [1, 1]
        for i in range(2, n):
            fib.append(fib[i-1] + fib[i-2])
        
        return fib
    
    def generate_golden_ratio_data_distribution(self, total_items=100):
        """
        Distribute fake data using golden ratio (φ ≈ 1.618)
        
        Creates natural-looking distributions
        """
        phi = (1 + np.sqrt(5)) / 2  # Golden ratio
        
        # Distribute items using golden ratio
        categories = ['critical', 'important', 'normal', 'low_priority']
        distribution = {}
        
        remaining = total_items
        for i, category in enumerate(categories[:-1]):
            count = int(remaining / phi)
            distribution[category] = count
            remaining -= count
        
        distribution[categories[-1]] = remaining
        
        logger.debug(f"Golden ratio distribution: {distribution}")
        
        return distribution
    
    def calculate_deception_entropy(self, deception_data):
        """
        Calculate Shannon entropy of deception data
        
        Higher entropy = more unpredictable = harder to detect as fake
        """
        if isinstance(deception_data, dict):
            deception_str = str(sorted(deception_data.items()))
        else:
            deception_str = str(deception_data)
        
        entropy = global_metrics.calculate_entropy(deception_str)
        
        return {
            'entropy': entropy,
            'quality': 'high' if entropy > self.entropy_threshold else 'medium'
        }
    
    def generate_sierpinski_honeypot_placement(self, depth=3):
        """
        INNOVATION: Place honeypots using Sierpinski triangle fractal
        
        Creates non-obvious patterns that are harder to detect
        """
        points = []
        
        # Initial triangle vertices
        vertices = [
            (0, 0),
            (100, 0),
            (50, 86.6)  # Equilateral triangle
        ]
        
        # Current point
        point = (50, 28.9)
        
        # Generate points using chaos game
        for _ in range(2 ** depth):
            # Choose random vertex
            vertex = random.choice(vertices)
            
            # Move halfway to vertex
            point = (
                (point[0] + vertex[0]) / 2,
                (point[1] + vertex[1]) / 2
            )
            
            points.append(point)
        
        # Normalize to network coordinates
        honeypot_locations = []
        for x, y in points:
            honeypot_locations.append({
                'x': int(x),
                'y': int(y),
                'subnet': f"192.168.{int(x % 255)}.{int(y % 255)}"
            })
        
        logger.info(f"Generated {len(honeypot_locations)} Sierpinski honeypot locations")
        
        return honeypot_locations
    
    def generate_mandelbrot_complexity_map(self, width=50, height=50):
        """
        Use Mandelbrot set to determine deception complexity levels
        
        Areas of high complexity get more sophisticated deception
        """
        complexity_map = np.zeros((height, width))
        
        for y in range(height):
            for x in range(width):
                # Map to complex plane
                c = complex(
                    (x - width/2) * 4.0 / width,
                    (y - height/2) * 4.0 / height
                )
                
                # Calculate iterations to escape
                z = 0
                iterations = 0
                max_iterations = 50
                
                while abs(z) < 2 and iterations < max_iterations:
                    z = z*z + c
                    iterations += 1
                
                complexity_map[y, x] = iterations / max_iterations
        
        logger.debug("Generated Mandelbrot complexity map")
        
        return complexity_map
    
    def validate_mathematical_properties(self, generated_data):
        """
        Validate that generated deception data has desired mathematical properties
        """
        validation = {
            'entropy': self.calculate_deception_entropy(generated_data),
            'complexity': len(str(generated_data)),
            'uniqueness': len(set(str(generated_data))) / len(str(generated_data)) if generated_data else 0,
            'passes_validation': False
        }
        
        # Check if meets thresholds
        if validation['entropy']['entropy'] > self.entropy_threshold:
            validation['passes_validation'] = True
        
        return validation


class FractalFileSystem:
    """
    Specialized class for fractal-based file system generation
    """
    
    def __init__(self):
        self.math_deception = MathematicalDeception()
    
    def create_believable_filesystem(self, root='/var/fake', depth=4):
        """
        Create a complete, believable fake file system
        """
        # Generate fractal structure
        base_structure = self.math_deception.generate_fractal_filesystem(root, depth)
        
        # Add realistic content hints
        for file_path in base_structure['files']:
            base_structure['structure'][file_path] = {
                'size': random.randint(1024, 1024*1024*10),  # 1KB to 10MB
                'modified': self._generate_realistic_timestamp(),
                'permissions': random.choice(['644', '640', '600', '755']),
                'contains': self._guess_file_content(file_path)
            }
        
        for dir_path in base_structure['directories']:
            base_structure['structure'][dir_path] = {
                'permissions': '755',
                'modified': self._generate_realistic_timestamp()
            }
        
        return base_structure
    
    def _generate_realistic_timestamp(self):
        """Generate believable file timestamps"""
        year = random.randint(2022, 2025)
        month = random.randint(1, 12)
        day = random.randint(1, 28)
        hour = random.randint(0, 23)
        minute = random.randint(0, 59)
        
        return f"{year}-{month:02d}-{day:02d} {hour:02d}:{minute:02d}"
    
    def _guess_file_content(self, file_path):
        """Guess what a file might contain based on its name"""
        if '.db' in file_path or 'database' in file_path:
            return 'Database file with customer records'
        elif '.conf' in file_path or 'config' in file_path:
            return 'Configuration file with system settings'
        elif 'key' in file_path or 'secret' in file_path:
            return 'Encryption keys or credentials'
        elif 'backup' in file_path:
            return 'Backup archive'
        elif '.sql' in file_path:
            return 'SQL dump file'
        else:
            return 'Data file'