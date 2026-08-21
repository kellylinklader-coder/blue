import yaml
import os
from pathlib import Path

class Config:
    """Configuration manager for Blue Eye"""
    
    def __init__(self, config_file="config.yaml"):
        self.config_file = config_file
        self.config = self.load_config()
        self.setup_directories()
    
    def load_config(self):
        """Load configuration from YAML file"""
        if not os.path.exists(self.config_file):
            raise FileNotFoundError(f"Config file not found: {self.config_file}")
        
        with open(self.config_file, 'r') as f:
            return yaml.safe_load(f)
    
    def setup_directories(self):
        """Create necessary directories"""
        for directory in [self.config['output']['report_dir'], 
                         self.config['output']['log_dir']]:
            Path(directory).mkdir(parents=True, exist_ok=True)
    
    def get(self, key, default=None):
        """Get configuration value by dot notation (e.g., 'target.domain')"""
        keys = key.split('.')
        value = self.config
        for k in keys:
            value = value.get(k, default)
            if value is None:
                return default
        return value
    
    def set(self, key, value):
        """Set configuration value by dot notation"""
        keys = key.split('.')
        config = self.config
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        config[keys[-1]] = value
    
    def is_module_enabled(self, module_name):
        """Check if a module is enabled"""
        return self.config['modules'].get(module_name, False)
    
    def get_subdomain_wordlist(self):
        """Get subdomain wordlist from config"""
        return self.config.get('subdomain_wordlist', [])
