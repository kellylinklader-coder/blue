import requests
import json
import dns.resolver
import time
from logger import Logger

class CertificateScanner:
    """SSL certificate enumeration via crt.sh"""
    
    def __init__(self, config):
        self.config = config
        self.logger = Logger()
    
    def scan(self, target):
        """Scan certificates from crt.sh"""
        certs = []
        
        try:
            self.logger.info(f"Scanning certificates for {target}")
            url = f"https://crt.sh/?q=%.{target}&output=json"
            headers = {"User-Agent": self.config.get('settings.user_agent')}
            
            response = requests.get(url, headers=headers, timeout=self.config.get('settings.timeout'))
            
            if response.status_code == 200:
                json_data = response.json()
                domains = []
                
                for item in json_data:
                    if 'name_value' in item:
                        for domain in item['name_value'].split('\n'):
                            domain = domain.strip()
                            if domain.startswith('*.'):
                                domain = domain[2:]
                            if domain and domain not in domains:
                                domains.append(domain)
                
                for idx, domain in enumerate(sorted(set(domains)), 1):
                    self.logger.success(f"{idx}. {domain}")
                    
                    try:
                        ns = dns.resolver.query(domain, "A")
                        for rdata in ns.response.answer:
                            for item in rdata.items:
                                ip = str(item)
                                certs.append({'domain': domain, 'ip': ip})
                                self.logger.success(f"  -> {domain} resolves to {ip}")
                    except:
                        pass
                
                self.logger.info(f"Found {len(set(domains))} domains")
        except Exception as e:
            self.logger.error(f"Certificate scan error: {str(e)}")
        
        return certs
