"""
Honeypot Manager - Dynamic service deployment
Manages multiple honeypot services with integration to polymorphic system
"""

import socket
import threading
import random
from datetime import datetime
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parent.parent))
from utilities.config import HONEYPOT_CONFIG
from utilities.logger import get_logger, log_attack
from utilities.metrics import global_metrics

logger = get_logger('honeypot_manager')


class HoneypotService:
    """
    Base class for honeypot services
    """
    
    def __init__(self, service_type, port):
        self.service_type = service_type
        self.port = port
        self.running = False
        self.interactions = []
        self.socket = None
        self.thread = None
    
    def start(self):
        """Start the honeypot service"""
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.socket.bind(('0.0.0.0', self.port))
            self.socket.listen(5)
            self.running = True
            
            self.thread = threading.Thread(target=self._accept_connections, daemon=True)
            self.thread.start()
            
            logger.info(f"{self.service_type} honeypot started on port {self.port}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to start {self.service_type} honeypot: {e}")
            return False
    
    def stop(self):
        """Stop the honeypot service"""
        self.running = False
        if self.socket:
            self.socket.close()
        logger.info(f"{self.service_type} honeypot stopped")
    
    def _accept_connections(self):
        """Accept incoming connections (override in subclasses)"""
        while self.running:
            try:
                self.socket.settimeout(1.0)
                client, addr = self.socket.accept()
                
                # Log interaction
                interaction = {
                    'timestamp': datetime.now().isoformat(),
                    'source_ip': addr[0],
                    'source_port': addr[1],
                    'service': self.service_type
                }
                
                self.interactions.append(interaction)
                
                # Handle in separate thread
                threading.Thread(
                    target=self._handle_client, 
                    args=(client, addr), 
                    daemon=True
                ).start()
                
            except socket.timeout:
                continue
            except Exception as e:
                if self.running:
                    logger.error(f"Error accepting connection: {e}")
    
    def _handle_client(self, client, addr):
        """Handle client connection (override in subclasses)"""
        pass


class SSHHoneypot(HoneypotService):
    """SSH honeypot with fake authentication"""
    
    def __init__(self, port=2222):
        super().__init__('SSH', port)
        self.fake_credentials = [
            ('admin', 'admin123'),
            ('root', 'password'),
            ('user', 'user123')
        ]
    
    def _handle_client(self, client, addr):
        """Simulate SSH login"""
        try:
            # Send SSH banner
            banner = b"SSH-2.0-OpenSSH_8.9p1 Ubuntu-3ubuntu0.1\r\n"
            client.send(banner)
            
            # Wait for authentication attempt
            data = client.recv(1024)
            
            if data:
                log_attack({
                    'type': 'ssh_connection',
                    'source_ip': addr[0],
                    'target': f'SSH:{self.port}',
                    'severity': 'MEDIUM',
                    'threat_score': 0.6,
                    'deception_triggered': True,
                    'details': {'data_length': len(data)}
                })
                
                # Simulate delay
                import time
                time.sleep(random.uniform(0.5, 2.0))
                
                # Send fake authentication failed
                client.send(b"Permission denied (publickey,password).\r\n")
            
        except Exception as e:
            logger.debug(f"SSH interaction error: {e}")
        finally:
            client.close()


class HTTPHoneypot(HoneypotService):
    """HTTP honeypot with fake web interface"""
    
    def __init__(self, port=8080):
        super().__init__('HTTP', port)
    
    def _handle_client(self, client, addr):
        """Simulate HTTP server"""
        try:
            request = client.recv(4096).decode('utf-8', errors='ignore')
            
            if request:
                # Parse request
                lines = request.split('\r\n')
                if lines:
                    method_line = lines[0]
                    
                    log_attack({
                        'type': 'http_request',
                        'source_ip': addr[0],
                        'target': f'HTTP:{self.port}',
                        'severity': 'LOW',
                        'threat_score': 0.4,
                        'deception_triggered': True,
                        'details': {'request': method_line}
                    })
                
                # Send fake response
                response = (
                    "HTTP/1.1 200 OK\r\n"
                    "Server: nginx/1.18.0\r\n"
                    "Content-Type: text/html\r\n"
                    "\r\n"
                    "<html><body><h1>Corporate Intranet Portal</h1>"
                    "<form action='/login' method='post'>"
                    "<input type='text' name='username' placeholder='Username'>"
                    "<input type='password' name='password' placeholder='Password'>"
                    "<button>Login</button>"
                    "</form></body></html>"
                )
                
                client.send(response.encode())
                
        except Exception as e:
            logger.debug(f"HTTP interaction error: {e}")
        finally:
            client.close()


class FTPHoneypot(HoneypotService):
    """FTP honeypot"""
    
    def __init__(self, port=2121):
        super().__init__('FTP', port)
    
    def _handle_client(self, client, addr):
        """Simulate FTP server"""
        try:
            # Send FTP welcome
            welcome = b"220 ProFTPD Server (Corporate FTP) [192.168.1.100]\r\n"
            client.send(welcome)
            
            # Wait for commands
            while True:
                data = client.recv(1024)
                if not data:
                    break
                
                command = data.decode('utf-8', errors='ignore').strip()
                
                log_attack({
                    'type': 'ftp_command',
                    'source_ip': addr[0],
                    'target': f'FTP:{self.port}',
                    'severity': 'MEDIUM',
                    'threat_score': 0.5,
                    'deception_triggered': True,
                    'details': {'command': command}
                })
                
                # Send fake responses
                if command.startswith('USER'):
                    client.send(b"331 Password required\r\n")
                elif command.startswith('PASS'):
                    client.send(b"530 Login incorrect\r\n")
                else:
                    client.send(b"500 Unknown command\r\n")
            
        except Exception as e:
            logger.debug(f"FTP interaction error: {e}")
        finally:
            client.close()


class HoneypotManager:
    """
    Manages multiple honeypot services
    Integrates with polymorphic and genetic systems
    """
    
    def __init__(self):
        self.active_honeypots = {}
        self.config = HONEYPOT_CONFIG
        
        logger.info("Honeypot Manager initialized")
    
    def deploy_honeypots(self):
        """Deploy configured honeypots"""
        for service_type, config in self.config['services'].items():
            if config['enabled']:
                self.deploy_honeypot(service_type, config['port'])
    
    def deploy_honeypot(self, service_type, port):
        """Deploy a single honeypot service"""
        honeypot_classes = {
            'ssh': SSHHoneypot,
            'http': HTTPHoneypot,
            'ftp': FTPHoneypot
        }
        
        if service_type not in honeypot_classes:
            logger.warning(f"Unknown honeypot type: {service_type}")
            return False
        
        try:
            honeypot = honeypot_classes[service_type](port)
            if honeypot.start():
                self.active_honeypots[service_type] = honeypot
                logger.info(f"Deployed {service_type} honeypot on port {port}")
                return True
        except Exception as e:
            logger.error(f"Failed to deploy {service_type} honeypot: {e}")
        
        return False
    
    def stop_all_honeypots(self):
        """Stop all running honeypots"""
        for service_type, honeypot in self.active_honeypots.items():
            honeypot.stop()
        
        self.active_honeypots.clear()
        logger.info("All honeypots stopped")
    
    def get_honeypot_stats(self):
        """Get statistics from all honeypots"""
        stats = {
            'active_honeypots': len(self.active_honeypots),
            'total_interactions': 0,
            'by_service': {}
        }
        
        for service_type, honeypot in self.active_honeypots.items():
            interaction_count = len(honeypot.interactions)
            stats['total_interactions'] += interaction_count
            stats['by_service'][service_type] = {
                'port': honeypot.port,
                'interactions': interaction_count,
                'running': honeypot.running
            }
        
        return stats
    
    def get_recent_interactions(self, limit=50):
        """Get recent honeypot interactions"""
        all_interactions = []
        
        for honeypot in self.active_honeypots.values():
            all_interactions.extend(honeypot.interactions)
        
        # Sort by timestamp
        all_interactions.sort(key=lambda x: x['timestamp'], reverse=True)
        
        return all_interactions[:limit]