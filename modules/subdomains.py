import socket
import time
from logger import Logger

class SubdomainScanner:
    """Subdomain enumeration"""
    
    def __init__(self, config):
        self.config = config
        self.logger = Logger()
    
    def scan(self, target):
        """Brute force subdomains"""
        subdomains = self.config.get_subdomain_wordlist()
        found = []
        
        self.logger.info(f"Scanning subdomains for {target}")
        
        for subdomain_name in subdomains:
            subdomain = f"{subdomain_name}.{target}"
            try:
                ip = socket.gethostbyname(subdomain)
                found.append({'subdomain': subdomain, 'ip': ip})
                self.logger.success(f"{subdomain} -> {ip}")
                time.sleep(0.1)
            except:
                pass
        
        self.logger.info(f"Found {len(found)} subdomains")
        return found
