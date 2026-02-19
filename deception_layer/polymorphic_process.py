"""
POLYMORPHIC PROCESS MIRAGE - SIGNATURE INNOVATION
Dynamic process deception that continuously morphs to confuse attackers

This is the core innovation that makes this project research-worthy
"""

import random
import time
import uuid
import hashlib
import numpy as np
from datetime import datetime
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parent.parent))
from utilities.config import MIRAGE_CONFIG
from utilities.logger import get_logger, log_deception
from utilities.metrics import global_metrics

logger = get_logger('polymorphic_mirage')


class PolymorphicProcessMirage:
    """
    Creates fake processes that dynamically change their characteristics
    to evade detection and confuse attackers
    
    RESEARCH NOVELTY: Processes that evolve their identity in real-time
    """
    
    def __init__(self):
        self.active_mirages = {}
        self.mutation_interval = MIRAGE_CONFIG['mutation_interval']
        self.max_mirages = MIRAGE_CONFIG['max_active_mirages']
        self.process_types = MIRAGE_CONFIG['process_types']
        self.mutation_history = []
        
        logger.info("Polymorphic Process Mirage system initialized")
    
    def create_mirage(self, process_type=None):
        """
        Create a new polymorphic process mirage
        """
        if process_type is None:
            process_type = random.choice(self.process_types)
        
        mirage_id = str(uuid.uuid4())[:8]
        
        mirage = {
            'id': mirage_id,
            'type': process_type,
            'pid': self._generate_realistic_pid(),
            'name': self._generate_process_name(process_type),
            'memory': self._generate_memory_pattern(process_type),
            'cpu': self._generate_cpu_pattern(process_type),
            'network_connections': self._create_fake_connections(process_type),
            'command_line': self._generate_cmdline(process_type),
            'open_files': self._generate_file_handles(process_type),
            'user': self._generate_user(process_type),
            'creation_time': datetime.now().isoformat(),
            'last_mutation': datetime.now().isoformat(),
            'mutation_count': 0,
            'mutation_history': [],
            'attacker_interactions': 0,
            'genetic_diversity_scores': [],
            'active': True
        }
        
        self.active_mirages[mirage_id] = mirage
        logger.info(f"Created polymorphic mirage: {mirage_id} ({process_type})")
        
        return mirage
    
    def morph_characteristics(self, mirage_id):
        """
        CORE INNOVATION: Polymorphic mutation of process characteristics
        This makes the process unrecognizable to attackers over time
        """
        if mirage_id not in self.active_mirages:
            logger.warning(f"Mirage {mirage_id} not found")
            return None
        
        mirage = self.active_mirages[mirage_id]
        
        # Save previous state for diversity calculation
        previous_state = {
            'name': mirage['name'],
            'memory': mirage['memory'],
            'cpu': mirage['cpu'],
            'network_connections': len(mirage['network_connections'])
        }
        
        # Select mutation strategies
        mutation_strategies = random.sample(
            MIRAGE_CONFIG['mutation_strategies'], 
            k=random.randint(2, 4)
        )
        
        mutations_applied = []
        
        # Apply mutations
        for strategy in mutation_strategies:
            if strategy == 'name':
                mirage['name'] = self._mutate_process_name(mirage)
                mutations_applied.append('name_mutation')
            
            elif strategy == 'memory':
                mirage['memory'] = self._mutate_memory_footprint(mirage)
                mutations_applied.append('memory_mutation')
            
            elif strategy == 'cpu':
                mirage['cpu'] = self._mutate_cpu_pattern(mirage)
                mutations_applied.append('cpu_mutation')
            
            elif strategy == 'network':
                mirage['network_connections'] = self._mutate_network_behavior(mirage)
                mutations_applied.append('network_mutation')
            
            elif strategy == 'files':
                mirage['open_files'] = self._mutate_file_operations(mirage)
                mutations_applied.append('file_mutation')
        
        # Calculate genetic diversity score
        current_state = {
            'name': mirage['name'],
            'memory': mirage['memory'],
            'cpu': mirage['cpu'],
            'network_connections': len(mirage['network_connections'])
        }
        
        diversity_score = self._calculate_genetic_diversity(current_state, previous_state)
        mirage['genetic_diversity_scores'].append(diversity_score)
        
        # Update mutation tracking
        mutation_record = {
            'timestamp': datetime.now().isoformat(),
            'mutations': mutations_applied,
            'genetic_diversity': diversity_score,
            'previous_state': previous_state,
            'new_state': current_state
        }
        
        mirage['mutation_history'].append(mutation_record)
        mirage['mutation_count'] += 1
        mirage['last_mutation'] = datetime.now().isoformat()
        
        # Log deception event
        log_deception({
            'id': mirage_id,
            'mutation_type': ', '.join(mutations_applied),
            'diversity_score': diversity_score,
            'interactions': mirage['attacker_interactions'],
            'details': mutation_record
        })
        
        logger.info(f"Mirage {mirage_id} morphed: {', '.join(mutations_applied)} (diversity: {diversity_score:.3f})")
        
        return mirage
    
    def _calculate_genetic_diversity(self, current, previous):
        """
        NOVEL METRIC: Genetic Diversity Score
        Measures how different the current state is from previous state
        """
        return global_metrics.calculate_genetic_diversity_score(current, [previous])
    
    def _generate_realistic_pid(self):
        """Generate a believable process ID"""
        # Linux PIDs typically range from 1 to 32768
        # System processes: 1-999
        # User processes: 1000+
        return random.randint(1000, 32768)
    
    def _generate_process_name(self, process_type):
        """Generate believable process names based on type"""
        process_names = {
            'database': ['mysqld', 'postgres', 'mongod', 'redis-server', 'mariadbd'],
            'web_server': ['nginx', 'apache2', 'httpd', 'node', 'gunicorn'],
            'ssh_daemon': ['sshd', 'ssh-agent', 'ssh-keygen'],
            'backup_service': ['rsync', 'backup-daemon', 'tar', 'duplicity'],
            'cache_server': ['memcached', 'redis', 'varnishd'],
            'api_gateway': ['api-gateway', 'kong', 'nginx-api'],
            'file_server': ['nfsd', 'smbd', 'vsftpd'],
            'mail_server': ['postfix', 'dovecot', 'exim4']
        }
        
        return random.choice(process_names.get(process_type, ['generic-daemon']))
    
    def _generate_memory_pattern(self, process_type):
        """Generate realistic memory usage (in MB)"""
        memory_ranges = {
            'database': (200, 2048),
            'web_server': (50, 512),
            'ssh_daemon': (2, 20),
            'backup_service': (10, 200),
            'cache_server': (100, 1024),
            'api_gateway': (50, 300),
            'file_server': (20, 150),
            'mail_server': (30, 200)
        }
        
        min_mem, max_mem = memory_ranges.get(process_type, (10, 100))
        return random.randint(min_mem, max_mem)
    
    def _generate_cpu_pattern(self, process_type):
        """Generate realistic CPU usage (0-100%)"""
        cpu_ranges = {
            'database': (5, 40),
            'web_server': (2, 30),
            'ssh_daemon': (0, 5),
            'backup_service': (10, 60),
            'cache_server': (1, 15),
            'api_gateway': (5, 25),
            'file_server': (2, 20),
            'mail_server': (1, 15)
        }
        
        min_cpu, max_cpu = cpu_ranges.get(process_type, (0, 10))
        return round(random.uniform(min_cpu, max_cpu), 2)
    
    def _create_fake_connections(self, process_type):
        """Create believable network connections"""
        port_ranges = {
            'database': [(3306, 'mysql'), (5432, 'postgres'), (27017, 'mongodb')],
            'web_server': [(80, 'http'), (443, 'https'), (8080, 'http-alt')],
            'ssh_daemon': [(22, 'ssh'), (2222, 'ssh-alt')],
            'cache_server': [(6379, 'redis'), (11211, 'memcache')],
            'api_gateway': [(8000, 'api'), (8443, 'api-ssl')],
            'file_server': [(21, 'ftp'), (445, 'smb'), (2049, 'nfs')],
            'mail_server': [(25, 'smtp'), (587, 'submission'), (993, 'imaps')]
        }
        
        possible_ports = port_ranges.get(process_type, [(8000, 'generic')])
        num_connections = random.randint(1, 5)
        
        connections = []
        for _ in range(num_connections):
            port, service = random.choice(possible_ports)
            connections.append({
                'local_port': port,
                'remote_ip': f"192.168.{random.randint(1,254)}.{random.randint(1,254)}",
                'remote_port': random.randint(30000, 65535),
                'state': random.choice(['ESTABLISHED', 'LISTEN', 'TIME_WAIT']),
                'service': service
            })
        
        return connections
    
    def _generate_cmdline(self, process_type):
        """Generate believable command line arguments"""
        cmdlines = {
            'database': [
                'mysqld --datadir=/var/lib/mysql --socket=/var/run/mysqld/mysqld.sock',
                'postgres -D /var/lib/postgresql/data',
                'mongod --dbpath=/var/lib/mongodb --port=27017'
            ],
            'web_server': [
                'nginx: master process /usr/sbin/nginx',
                '/usr/sbin/apache2 -k start',
                'node /app/server.js'
            ],
            'ssh_daemon': [
                'sshd: /usr/sbin/sshd -D',
                '/usr/sbin/sshd -p 22'
            ]
        }
        
        return random.choice(cmdlines.get(process_type, ['daemon --config=/etc/config']))
    
    def _generate_file_handles(self, process_type):
        """Generate open file handles"""
        num_files = random.randint(5, 30)
        files = []
        
        for i in range(num_files):
            files.append({
                'fd': i,
                'path': f"/var/lib/{process_type}/data/{random.randint(1000,9999)}.db",
                'mode': random.choice(['r', 'w', 'rw'])
            })
        
        return files
    
    def _generate_user(self, process_type):
        """Generate process owner"""
        system_users = ['mysql', 'postgres', 'www-data', 'nginx', 'redis', 'mongodb']
        return random.choice(system_users)
    
    def _mutate_process_name(self, mirage):
        """Mutate process name slightly"""
        current_name = mirage['name']
        
        # Add suffix/prefix
        mutations = [
            f"{current_name}-worker",
            f"{current_name}d",
            f"new-{current_name}",
            f"{current_name}-primary",
            f"{current_name}.{random.randint(1,9)}"
        ]
        
        return random.choice(mutations)
    
    def _mutate_memory_footprint(self, mirage):
        """Change memory usage pattern"""
        current_memory = mirage['memory']
        # ±20% variation
        delta = random.uniform(-0.2, 0.2) * current_memory
        new_memory = max(10, int(current_memory + delta))
        return new_memory
    
    def _mutate_cpu_pattern(self, mirage):
        """Change CPU usage pattern"""
        current_cpu = mirage['cpu']
        # ±30% variation
        delta = random.uniform(-0.3, 0.3) * current_cpu
        new_cpu = max(0, min(100, current_cpu + delta))
        return round(new_cpu, 2)
    
    def _mutate_network_behavior(self, mirage):
        """Change network connections"""
        # Add or remove connections
        current_connections = mirage['network_connections']
        
        if random.random() < 0.5 and len(current_connections) > 0:
            # Remove a connection
            current_connections.pop(random.randint(0, len(current_connections)-1))
        else:
            # Add a new connection
            new_conn = {
                'local_port': random.randint(30000, 65535),
                'remote_ip': f"10.0.{random.randint(1,254)}.{random.randint(1,254)}",
                'remote_port': random.randint(30000, 65535),
                'state': random.choice(['ESTABLISHED', 'TIME_WAIT']),
                'service': 'dynamic'
            }
            current_connections.append(new_conn)
        
        return current_connections
    
    def _mutate_file_operations(self, mirage):
        """Change open files"""
        current_files = mirage['open_files']
        
        # Close some files, open new ones
        num_to_close = random.randint(0, min(3, len(current_files)))
        for _ in range(num_to_close):
            if current_files:
                current_files.pop(random.randint(0, len(current_files)-1))
        
        # Open new files
        num_to_open = random.randint(1, 5)
        for i in range(num_to_open):
            current_files.append({
                'fd': len(current_files) + i,
                'path': f"/tmp/temp_{random.randint(1000,9999)}.dat",
                'mode': random.choice(['r', 'w', 'rw'])
            })
        
        return current_files
    
    def register_attacker_interaction(self, mirage_id):
        """Track when an attacker interacts with a mirage"""
        if mirage_id in self.active_mirages:
            self.active_mirages[mirage_id]['attacker_interactions'] += 1
            logger.info(f"Attacker interacted with mirage {mirage_id}")
    
    def get_all_active_mirages(self):
        """Get all currently active mirages"""
        return [m for m in self.active_mirages.values() if m['active']]
    
    def get_mirage_stats(self):
        """Get statistics about mirage system"""
        total_mirages = len(self.active_mirages)
        total_mutations = sum(m['mutation_count'] for m in self.active_mirages.values())
        total_interactions = sum(m['attacker_interactions'] for m in self.active_mirages.values())
        
        avg_diversity = 0.0
        if total_mirages > 0:
            all_diversity_scores = []
            for mirage in self.active_mirages.values():
                all_diversity_scores.extend(mirage['genetic_diversity_scores'])
            
            if all_diversity_scores:
                avg_diversity = np.mean(all_diversity_scores)
        
        return {
            'total_mirages': total_mirages,
            'total_mutations': total_mutations,
            'total_interactions': total_interactions,
            'average_genetic_diversity': avg_diversity
        }
    
    def continuous_morphing_loop(self):
        """
        Continuous background process that morphs all active mirages
        This would run in a separate thread in production
        """
        logger.info("Starting continuous morphing loop")
        
        while True:
            for mirage_id in list(self.active_mirages.keys()):
                self.morph_characteristics(mirage_id)
            
            time.sleep(self.mutation_interval)