#!/usr/bin/env python3
"""Blue Eye Recon Toolkit v2.1 Extended - Modular Version

Author: Jolanda de Koff
GitHub: https://github.com/BullsEye0
"""

import argparse
import sys
import time
from datetime import datetime

from config import Config
from logger import Logger
from report_generator import ReportGenerator
from modules.ip_geolocation import IPGeolocation
from modules.dns_records import DNSRecords
from modules.subdomains import SubdomainScanner
from modules.certificates import CertificateScanner
from modules.technologies import TechnologyDetection
from modules.github import GitHubScanner


class BlueEye:
    """Main Blue Eye orchestrator"""
    
    BANNER = """
            \033[1;34m
         ▄▄▄▄    ██▓     █    ██ ▓█████    ▓█████▓██   ██▓▓█████
        ▓█████▄ ▓██▒     ██  ▓██▒▓█   ▀    ▓█   ▀ ▒██  ██▒▓█   ▀
        ▒██▒ ▄██▒██░    ▓██  ▒██░▒███      ▒███    ▒██ ██░▒███
        ▒██░█▀  ▒██░    ▓▓█  ░██░▒▓█  ▄    ▒▓█  ▄  ░ ▐██▓░▒▓█  ▄
        ░▓█  ▀█▓░██████▒▒▒█████▓ ░▒████▒   ░▒████▒ ░ ██▒▓░░▒████▒
        ░▒▓███▀▒░ ▒░▓  ░░▒▓▒ ▒ ▒ ░░ ▒░ ░   ░░ ▒░ ░  ██▒▒▒ ░░ ▒░ ░
        ▒░▒   ░ ░ ░ ▒  ░░░▒░ ░ ░  ░ ░  ░    ░ ░  ░▓██ ░▒░  ░ ░  ░
         ░    ░   ░ ░    ░░░ ░ ░    ░         ░   ▒ ▒ ░░     ░
         ░          ░  ░   ░        ░  ░      ░  ░░ ░        ░  ░
              ░                                   ░ ░   v2.1 Extended
            \033[1;m

        \033[34mBlue Eye\033[0m Recon Toolkit

        Author:  Jolanda de Koff Bulls Eye
        Github:  https://github.com/BullsEye0
        Website: https://HackingPassion.com

            \033[1;31mHi there, Shall we play a game..?\033[0m 😃
            """
    
    def __init__(self, config):
        self.config = config
        self.logger = Logger(config.get('output.verbose', True))
        self.report_data = {
            'target': '',
            'scan_time': '',
            'ip_info': {},
            'dns_records': {},
            'subdomains': [],
            'technologies': [],
            'certificates': [],
            'github_users': [],
            'emails': []
        }
    
    def print_banner(self):
        """Display the Blue Eye banner"""
        print(self.BANNER)
        time.sleep(0.4)
    
    def scan(self, target, company_name):
        """Execute reconnaissance scan"""
        self.logger.section(f"Starting scan for {target}")
        self.report_data['target'] = target
        self.report_data['scan_time'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        comp = target.partition(".")[0]
        
        # IP Geolocation
        if self.config.is_module_enabled('ip_geolocation'):
            self.logger.section("IP Geolocation Scan")
            scanner = IPGeolocation(self.config)
            self.report_data['ip_info'] = scanner.scan(target)
        
        # DNS Records
        if self.config.is_module_enabled('dns_records'):
            self.logger.section("DNS Records Scan")
            scanner = DNSRecords(self.config)
            self.report_data['dns_records'] = scanner.scan(target, comp)
        
        # Subdomains
        if self.config.is_module_enabled('subdomains'):
            self.logger.section("Subdomain Scan")
            scanner = SubdomainScanner(self.config)
            self.report_data['subdomains'] = scanner.scan(target)
        
        # Certificates
        if self.config.is_module_enabled('certificates'):
            self.logger.section("Certificate Scan")
            scanner = CertificateScanner(self.config)
            self.report_data['certificates'] = scanner.scan(target)
        
        # Technologies
        if self.config.is_module_enabled('technologies'):
            self.logger.section("Technology Detection")
            scanner = TechnologyDetection(self.config)
            self.report_data['technologies'] = scanner.scan(target)
        
        # GitHub
        if self.config.is_module_enabled('github_users') or self.config.is_module_enabled('email_harvesting'):
            github = GitHubScanner(self.config)
            
            if self.config.is_module_enabled('github_users'):
                self.logger.section("GitHub User Enumeration")
                users = github.get_users(comp, target)
                self.report_data['github_users'] = [f"https://github.com/{u}" for u in users]
            else:
                users = github.get_users(comp, target)
            
            if self.config.is_module_enabled('email_harvesting'):
                self.logger.section("Email Harvesting")
                emails = github.harvest_emails(target, users if users else [])
                self.report_data['emails'] = emails
        
        # Generate Report
        if self.config.is_module_enabled('html_report'):
            self.logger.section("Generating Report")
            generator = ReportGenerator(self.config)
            report_path = generator.generate(self.report_data)
            if report_path:
                self.logger.success(f"Report generated: {report_path}")
        
        self.logger.section("Scan Complete!")
        print(f"\n\t\033[34mI like to See Ya, Hacking\033[0m 😃\n")


def main():
    parser = argparse.ArgumentParser(
        description='Blue Eye Recon Toolkit - Modular OSINT Framework',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Interactive mode with config file
  python blue_eye.py -c config.yaml
  
  # Quick scan with specific target
  python blue_eye.py -t example.com -c config.yaml
  
  # Quick scan with specific target and company
  python blue_eye.py -t example.com -n "Example Inc" -c config.yaml
        """
    )
    
    parser.add_argument('-c', '--config', default='config.yaml',
                       help='Configuration file path (default: config.yaml)')
    parser.add_argument('-t', '--target', help='Target domain')
    parser.add_argument('-n', '--name', help='Company name')
    parser.add_argument('--disable-modules', nargs='+',
                       help='Disable specific modules (space-separated)')
    parser.add_argument('--enable-modules', nargs='+',
                       help='Enable only specific modules (space-separated)')
    
    args = parser.parse_args()
    
    try:
        # Load configuration
        config = Config(args.config)
        
        # Apply CLI overrides
        if args.disable_modules:
            for module in args.disable_modules:
                config.set(f'modules.{module}', False)
        
        if args.enable_modules:
            # Disable all, then enable only specified
            for module in config.config.get('modules', {}):
                config.set(f'modules.{module}', False)
            for module in args.enable_modules:
                config.set(f'modules.{module}', True)
        
        # Initialize Blue Eye
        blue_eye = BlueEye(config)
        blue_eye.print_banner()
        
        # Get target and company name
        if args.target:
            target = args.target
            company_name = args.name or target.partition(".")[0]
        else:
            target = input("[+] \033[34mWhat domain do you want to search: \033[0m").strip()
            company_name = input("[+] \033[34mEnter the company name: \033[0m").strip()
        
        # Execute scan
        blue_eye.scan(target, company_name)
        
    except KeyboardInterrupt:
        print("\n\n[-] Scan interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n[!] Error: {str(e)}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
