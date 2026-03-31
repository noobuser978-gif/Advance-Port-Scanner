 🛡️ Advanced Port Scanner
v2.0 | A fast, multi-threaded Python scanner with service detection.

PythonLicense

⚡ Features

Multi-Protocol: Supports TCP Connect, SYN Stealth, and UDP scans.

Service Detection: Identifies services and grabs banners (HTTP, SSH, FTP, etc.).

Vulnerability Scanning: Flags potential CVEs based on version banners.

Reporting: Exports results to JSON and XML.

Network Sweep: Scans single IPs or entire CIDR ranges (e.g., 192.168.1.0/24).

📦 Requirements

Python 3.6+

Root/Admin access (required for SYN scans and OS fingerprinting).

🚀 Installation

No external packages needed. Just run the script:

git clone https://github.com/your-username/repo.gitcd repopython3 scanner.py -h

📖 Usage

bash

python3 scanner.py -t <TARGET_IP> [OPTIONS]

Options:

Flag                   Description                Default
-t              	Target IP or CIDR (Required)       	-
-p	               Ports (e.g., 1-1000, 22,80)	    1-1024
--threads	            Thread count	                 200
--type	                tcp, udp, or syn	            tcp

Examples
Standard Scan:

bash

python3 scanner.py -t 192.168.1.5
Stealth SYN Scan (Root):

bash

sudo python3 scanner.py -t 192.168.1.5 --type syn
Full Network Sweep:

bash

python3 scanner.py -t 192.168.1.0/24 --threads 500
📊 Output
Results are saved automatically to scan_results.json and scan_results.xml.

Sample JSON Output:

json

{
  "target": "192.168.1.5",
  "stats": { "open_ports": 2 },
  "results": [
    { "port": 80, "status": "open", "service": "http", "vuln": "Check nginx CVE-2021-23017" }
  ]
}

⚠️ Use responsibly. Only scan networks you own.
