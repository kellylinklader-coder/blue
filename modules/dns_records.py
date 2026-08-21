import dns.resolver
import socket
import time
from logger import Logger

class DNSRecords:
    """DNS record enumeration"""
    
    def __init__(self, config):
        self.config = config
        self.logger = Logger()
    
    def scan(self, target, comp):
        """Scan DNS records (MX, NS, TXT)"""
        result = {'mx': [], 'ns': [], 'txt': []}
        
        try:
            # MX Records
            self.logger.info("Scanning MX records")
            for mx in dns.resolver.query(target, "MX"):
                result['mx'].append(mx.to_text())
                self.logger.success(f"MX: {mx.to_text()}")
            
            time.sleep(self.config.get('settings.delay_between_requests'))
            
            # TXT Records
            self.logger.info("Scanning TXT records")
            for txt in dns.resolver.query(target, "TXT"):
                result['txt'].append(txt.to_text())
                self.logger.success(f"TXT: {txt.to_text()}")
            
            time.sleep(self.config.get('settings.delay_between_requests'))
            
            # NS Records
            self.logger.info("Scanning NS records")
            for ns in dns.resolver.query(target, "NS"):
                result['ns'].append(ns.to_text())
                self.logger.success(f"NS: {ns.to_text()}")
            
            # Check for interesting hosts
            self.logger.info("Checking for interesting hosts")
            hosts = [
                f"{comp}.okta.com",
                f"webmail.{comp}.com",
                f"email.{comp}.com",
                f"{comp}.slack.com"
            ]
            
            for host in hosts:
                try:
                    ip = socket.gethostbyname(host)
                    self.logger.success(f"Host of interest: {host} -> {ip}")
                except:
                    pass
            
            return result
        except Exception as e:
            self.logger.error(f"DNS Records error: {str(e)}")
            return result
