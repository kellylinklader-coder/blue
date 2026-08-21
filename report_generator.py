from datetime import datetime
from pathlib import Path
from logger import Logger
import json

class ReportGenerator:
    """Generate reconnaissance reports"""
    
    def __init__(self, config):
        self.config = config
        self.logger = Logger()
    
    def generate(self, report_data):
        """Generate report in configured format"""
        report_format = self.config.get('output.report_format', 'html')
        
        if report_format == 'html':
            return self.generate_html(report_data)
        elif report_format == 'json':
            return self.generate_json(report_data)
        elif report_format == 'txt':
            return self.generate_txt(report_data)
        else:
            self.logger.error(f"Unknown report format: {report_format}")
            return None
    
    def generate_html(self, report_data):
        """Generate HTML report"""
        try:
            filename = f"blue_eye_report_{report_data['target'].replace('.', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
            filepath = Path(self.config.get('output.report_dir')) / filename
            
            html_content = self._build_html(report_data)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            self.logger.success(f"Report saved: {filepath}")
            return str(filepath)
        except Exception as e:
            self.logger.error(f"HTML report generation error: {str(e)}")
            return None
    
    def generate_json(self, report_data):
        """Generate JSON report"""
        try:
            filename = f"blue_eye_report_{report_data['target'].replace('.', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            filepath = Path(self.config.get('output.report_dir')) / filename
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(report_data, f, indent=2)
            
            self.logger.success(f"Report saved: {filepath}")
            return str(filepath)
        except Exception as e:
            self.logger.error(f"JSON report generation error: {str(e)}")
            return None
    
    def generate_txt(self, report_data):
        """Generate text report"""
        try:
            filename = f"blue_eye_report_{report_data['target'].replace('.', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            filepath = Path(self.config.get('output.report_dir')) / filename
            
            txt_content = self._build_txt(report_data)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(txt_content)
            
            self.logger.success(f"Report saved: {filepath}")
            return str(filepath)
        except Exception as e:
            self.logger.error(f"TXT report generation error: {str(e)}")
            return None
    
    def _build_html(self, data):
        """Build HTML report content"""
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Blue Eye Recon Report - {data['target']}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        body {{
            font-family: 'Courier New', monospace;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: #fff;
            padding: 20px;
            line-height: 1.6;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: rgba(0, 0, 0, 0.7);
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.5);
        }}
        .header {{
            text-align: center;
            padding: 20px 0;
            border-bottom: 3px solid #667eea;
            margin-bottom: 30px;
        }}
        h1 {{
            color: #667eea;
            font-size: 2.5em;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
        }}
        .subtitle {{
            color: #a8b3ff;
            font-size: 1.2em;
        }}
        .section {{
            margin: 30px 0;
            padding: 20px;
            background: rgba(255,255,255,0.05);
            border-radius: 8px;
            border-left: 4px solid #667eea;
        }}
        h2 {{
            color: #667eea;
            margin-bottom: 15px;
            font-size: 1.8em;
        }}
        .badge {{
            display: inline-block;
            background: #667eea;
            color: white;
            padding: 5px 15px;
            border-radius: 20px;
            font-size: 0.9em;
            margin: 5px;
        }}
        ul {{
            list-style: none;
        }}
        li {{
            padding: 8px 0;
            border-bottom: 1px solid rgba(255,255,255,0.1);
        }}
        li:before {{
            content: "▸ ";
            color: #667eea;
            font-weight: bold;
            margin-right: 10px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Blue Eye Recon Report</h1>
            <div class="subtitle">Professional OSINT Reconnaissance Report</div>
            <div style="margin-top: 20px;">
                <span class="badge">Target: {data['target']}</span>
                <span class="badge">Scan Date: {data['scan_time']}</span>
            </div>
        </div>
        {self._build_html_sections(data)}
    </div>
</body>
</html>
"""
    
    def _build_html_sections(self, data):
        """Build HTML sections from report data"""
        sections = ""
        
        # IP Info
        if data.get('ip_info'):
            sections += f"""
        <div class="section">
            <h2>IP & Geolocation</h2>
            <ul>
                <li>IP: {data['ip_info'].get('query', 'N/A')}</li>
                <li>Country: {data['ip_info'].get('country', 'N/A')}</li>
                <li>Region: {data['ip_info'].get('regionName', 'N/A')}</li>
                <li>City: {data['ip_info'].get('city', 'N/A')}</li>
                <li>ISP: {data['ip_info'].get('isp', 'N/A')}</li>
            </ul>
        </div>
"""
        
        # Subdomains
        if data.get('subdomains'):
            sections += f"""
        <div class="section">
            <h2>Discovered Subdomains ({len(data['subdomains'])})</h2>
            <ul>
"""
            for sub in data['subdomains']:
                sections += f"<li>{sub['subdomain']} → {sub['ip']}</li>"
            sections += "</ul></div>"
        
        # Technologies
        if data.get('technologies'):
            sections += f"""
        <div class="section">
            <h2>Detected Technologies ({len(data['technologies'])})</h2>
            <ul>
"""
            for tech in data['technologies']:
                sections += f"<li>{tech['type']}: {tech['name']}</li>"
            sections += "</ul></div>"
        
        # DNS Records
        if data.get('dns_records'):
            sections += "<div class='section'><h2>DNS Records</h2>"
            if data['dns_records'].get('mx'):
                sections += "<h3>Mail Servers</h3><ul>"
                for mx in data['dns_records']['mx']:
                    sections += f"<li>{mx}</li>"
                sections += "</ul>"
            sections += "</div>"
        
        # GitHub Users
        if data.get('github_users'):
            sections += f"""
        <div class="section">
            <h2>GitHub Users ({len(data['github_users'])})</h2>
            <ul>
"""
            for user in data['github_users']:
                sections += f"<li><a href='{user}' style='color: #667eea;'>{user}</a></li>"
            sections += "</ul></div>"
        
        # Emails
        if data.get('emails'):
            sections += f"""
        <div class="section">
            <h2>Discovered Emails ({len(data['emails'])})</h2>
            <ul>
"""
            for email in data['emails']:
                sections += f"<li>{email}</li>"
            sections += "</ul></div>"
        
        return sections
    
    def _build_txt(self, data):
        """Build text report content"""
        lines = [
            "=" * 60,
            "BLUE EYE RECON REPORT",
            "=" * 60,
            f"Target: {data['target']}",
            f"Scan Time: {data['scan_time']}",
            ""
        ]
        
        if data.get('ip_info'):
            lines.extend([
                "IP & GEOLOCATION",
                "-" * 60,
                f"IP: {data['ip_info'].get('query', 'N/A')}",
                f"Country: {data['ip_info'].get('country', 'N/A')}",
                f"City: {data['ip_info'].get('city', 'N/A')}",
                ""
            ])
        
        if data.get('subdomains'):
            lines.extend([
                f"SUBDOMAINS ({len(data['subdomains'])})",
                "-" * 60
            ])
            for sub in data['subdomains']:
                lines.append(f"{sub['subdomain']} -> {sub['ip']}")
            lines.append("")
        
        if data.get('emails'):
            lines.extend([
                f"EMAILS ({len(data['emails'])})",
                "-" * 60
            ])
            for email in data['emails']:
                lines.append(email)
            lines.append("")
        
        return "\n".join(lines)
