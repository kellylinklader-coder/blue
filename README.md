# Blue Eye Recon Toolkit v2.1 Extended - Modular Edition

**Professional OSINT Reconnaissance Framework**

## Overview

Blue Eye is a modular OSINT reconnaissance toolkit designed for ethical security research and penetration testing. This refactored version provides:

- **Modular Architecture**: Enable/disable individual reconnaissance modules
- **Configuration-Driven**: YAML-based configuration for easy customization
- **Multiple Output Formats**: HTML, JSON, and text reports
- **Professional Logging**: Color-coded output with detailed logging
- **CLI Interface**: Command-line arguments for quick customization

## Features

- **IP Geolocation**: Fetch IP and geolocation information
- **DNS Enumeration**: Extract MX, NS, and TXT records
- **Subdomain Discovery**: Brute-force subdomain enumeration
- **Certificate Scanning**: Extract certificate data from crt.sh
- **Technology Detection**: Identify web technologies and frameworks
- **GitHub Enumeration**: Find GitHub users and email addresses
- **Email Harvesting**: Gather email addresses from multiple sources
- **Report Generation**: Create professional reconnaissance reports

## Installation

```bash
# Clone the repository
git clone https://github.com/kellylinklader-coder/blue.git
cd blue

# Install dependencies
pip install -r requirements.txt
```

## Configuration

Edit `config.yaml` to customize the toolkit:

```yaml
target:
  domain: "example.com"
  company_name: "example"

modules:
  ip_geolocation: true
  dns_records: true
  subdomains: true
  # ... more modules

output:
  report_dir: "reports"
  report_format: "html"  # html, json, txt
```

## Usage

### Interactive Mode

```bash
python blue_eye.py -c config.yaml
```

You'll be prompted to enter:
- Target domain
- Company name

### Quick Scan

```bash
python blue_eye.py -t example.com -n "Example Inc" -c config.yaml
```

### Module Control

```bash
# Disable specific modules
python blue_eye.py -t example.com --disable-modules github_users email_harvesting

# Enable only specific modules
python blue_eye.py -t example.com --enable-modules subdomains technologies
```

## Configuration Options

### Modules

Toggle individual reconnaissance modules:

- `ip_geolocation` - IP and geolocation lookup
- `http_headers` - HTTP header analysis
- `nmap_scan` - Nmap port scanning
- `dns_records` - DNS enumeration
- `certificates` - Certificate scanning
- `subdomains` - Subdomain discovery
- `technologies` - Technology detection
- `github_users` - GitHub user enumeration
- `email_harvesting` - Email address harvesting
- `html_report` - HTML report generation

### Output Formats

- `html` - Professional HTML report (default)
- `json` - Machine-readable JSON report
- `txt` - Plain text report

### Settings

- `timeout` - Request timeout in seconds
- `user_agent` - Custom User-Agent string
- `delay_between_requests` - Delay between requests (seconds)

## Project Structure

```
.
├── blue_eye.py              # Main entry point
├── config.yaml              # Configuration file
├── config.py                # Configuration manager
├── logger.py                # Logging utility
├── report_generator.py      # Report generation
├── modules/
│   ├── __init__.py
│   ├── ip_geolocation.py   # IP geolocation module
│   ├── dns_records.py      # DNS enumeration module
│   ├── subdomains.py       # Subdomain scanner
│   ├── certificates.py     # Certificate scanner
│   ├── technologies.py     # Technology detection
│   └── github.py           # GitHub enumeration & email harvesting
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

## Example Output

HTML reports include:
- IP and geolocation information
- DNS records (MX, NS, TXT)
- Discovered subdomains with IPs
- Detected web technologies
- SSL certificates
- GitHub users and emails
- Professional styling with gradient backgrounds

## Legal Disclaimer

**Important**: This tool is intended for authorized security testing and educational purposes only. Users are responsible for ensuring they have proper authorization before conducting any reconnaissance activities. Unauthorized access to computer systems is illegal.

## Author

**Jolanda de Koff (Bulls Eye)**
- GitHub: https://github.com/BullsEye0
- Website: https://HackingPassion.com
- LinkedIn: https://www.linkedin.com/in/jolandadekoff

## License

Copyright (c) 2019 - 2025 Jolanda de Koff. All rights reserved.

## Contributing

Contributions are welcome! Please ensure:
- Code follows the existing style
- New modules are added to `modules/` directory
- Configuration options are documented in `config.yaml`
- Changes maintain backward compatibility

## Support

For issues, questions, or feature requests, please open an issue on GitHub.
