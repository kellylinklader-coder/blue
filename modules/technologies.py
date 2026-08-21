import requests
from logger import Logger

class TechnologyDetection:
    """Detect web technologies"""
    
    def __init__(self, config):
        self.config = config
        self.logger = Logger()
    
    def scan(self, target):
        """Detect technologies used by target"""
        technologies = []
        
        try:
            self.logger.info(f"Detecting technologies for {target}")
            
            url = f"https://{target}" if not target.startswith('http') else target
            response = requests.get(url, timeout=self.config.get('settings.timeout'), allow_redirects=True)
            headers = response.headers
            content = response.text.lower()
            
            # Web Server
            if 'server' in headers:
                server = headers['server']
                technologies.append({'type': 'Web Server', 'name': server})
                self.logger.success(f"Web Server: {server}")
            
            # Powered By
            if 'x-powered-by' in headers:
                powered = headers['x-powered-by']
                technologies.append({'type': 'Powered By', 'name': powered})
                self.logger.success(f"Powered By: {powered}")
            
            # Framework/CMS Detection
            detections = {
                'WordPress': ['wp-content', 'wp-includes'],
                'Joomla': ['joomla', '/components/com_'],
                'Drupal': ['drupal', 'sites/all/'],
                'React': ['react', 'react-dom'],
                'Vue.js': ['vue.js', 'vue.min.js'],
                'Angular': ['angular', 'ng-app'],
                'jQuery': ['jquery'],
                'Bootstrap': ['bootstrap'],
                'Laravel': ['laravel'],
                'Django': ['django', 'csrfmiddlewaretoken'],
                'Flask': ['flask'],
                'Express': ['express'],
                'Cloudflare': ['cloudflare']
            }
            
            for tech, signatures in detections.items():
                for sig in signatures:
                    if sig in content:
                        technologies.append({'type': 'Framework/CMS', 'name': tech})
                        self.logger.success(f"Detected: {tech}")
                        break
            
            # CDN Detection
            if 'cf-ray' in headers:
                technologies.append({'type': 'CDN', 'name': 'Cloudflare'})
                self.logger.success("CDN: Cloudflare")
            
            self.logger.info(f"Detected {len(technologies)} technologies")
        except Exception as e:
            self.logger.error(f"Technology detection error: {str(e)}")
        
        return technologies
