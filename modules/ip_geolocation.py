import json
import urllib.request
import time
from logger import Logger

class IPGeolocation:
    """IP and geolocation information gathering"""
    
    def __init__(self, config):
        self.config = config
        self.logger = Logger()
    
    def scan(self, target):
        """Get IP and geolocation info using ip-api.com"""
        try:
            self.logger.info(f"Fetching geolocation for {target}")
            url = f"http://ip-api.com/json/{target}"
            response = urllib.request.urlopen(url)
            data = json.loads(response.read())
            time.sleep(self.config.get('settings.delay_between_requests'))
            
            self.logger.success(f"IP: {data.get('query')}")
            self.logger.success(f"Country: {data.get('country')}")
            self.logger.success(f"Region: {data.get('regionName')}")
            self.logger.success(f"City: {data.get('city')}")
            self.logger.success(f"ISP: {data.get('isp')}")
            self.logger.success(f"Lat & Lon: {data.get('lat')} & {data.get('lon')}")
            self.logger.success(f"Timezone: {data.get('timezone')}")
            self.logger.success(f"AS: {data.get('as')}")
            
            return data
        except Exception as e:
            self.logger.error(f"IP Geolocation error: {str(e)}")
            return {}
