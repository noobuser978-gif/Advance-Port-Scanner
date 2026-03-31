Advanced Port Scanner v2.0
VersionPythonLicense

╔══════════════════════════════════════════════════════════════════════════════╗║ Advanced Port Scanner ║║ v2.0 ║║ ║║ A high-performance, multi-threaded port scanner with service detection, ║║ OS fingerprinting, and vulnerability reporting. ║╚══════════════════════════════════════════════════════════════════════════════╝

Author: noobuser978-gif

📋 Table of Contents
Features
Requirements
Installation
Usage
Examples
Output Reports
Disclaimer
License
✨ Features
This tool is designed for network administrators and security enthusiasts to discover open ports and identify potential security risks.

🚀 High-Performance Scanning: Utilizes multi-threading (ThreadPoolExecutor) to scan thousands of ports rapidly.
🔍 Multiple Scan Types:
TCP Connect: Standard full-connection scan.
SYN Scan (Stealth): Half-open scan (requires root/admin privileges).
UDP Scan: Probes UDP ports (service detection enabled).
🌐 CIDR Support: Automatically scans entire subnets (e.g., 192.168.1.0/24).
📡 Service Detection:
Banner grabbing for HTTP, SSH, FTP, SMTP, and more.
Automatic service identification based on port numbers.
🛡️ Basic Vulnerability Detection: Identifies potential CVEs based on banners (e.g., Nginx, Apache, OpenSSH versions).
💻 OS Fingerprinting: Attempts to identify the target operating system (Linux/Windows) via TCP stack analysis.
📊 Multi-Format Reporting: Exports results to both JSON and XML files.
⚙️ Configurable: Adjustable thread counts, timeouts, and rate-limiting to avoid triggering IDS/IPS.
📦 Requirements
Python 3.6 or higher
Root/Admin Privileges (Required for SYN Stealth scans and Raw Sockets)
Operating System: Linux, macOS, or Windows (WSL recommended for raw socket features)
No external PyPI packages are required. This script runs on the Python Standard Library.

🚀 Installation
Clone the repository:
git clone https://github.com/your-username/your-repo-name.gitcd your-repo-name
Run the script directly:
bash

python3 scanner.py
Note: On Linux/macOS, you may need to use sudo for SYN scans:

bash

sudo python3 scanner.py -t 127.0.0.1 --type syn
📖 Usage
bash

python3 scanner.py -t <TARGET_IP> [OPTIONS]
Arguments
Argument
Short
Required
Description
--target	-t	Yes	Target IP address or CIDR range (e.g., 192.168.1.5 or 10.0.0.0/24).
--ports	-p	No	Port range to scan. Default: 1-1024. Supports formats: 80, 1-1000, 22,80,443.
--threads		No	Number of concurrent threads. Default: 200.
--type		No	Scan type: tcp (default), udp, or syn.
--timeout		No	Socket timeout in seconds. Default: 1.0.
--rate-limit		No	Delay between scans in seconds. Default: 0.01.

💡 Examples
1. Basic TCP Scan (Common Ports)
Scan a specific host for open ports on the default range (1-1024).

bash

python3 scanner.py -t 192.168.1.10
2. Scan Specific Ports
Scan ports 80, 443, 8080 and 22.

bash

python3 scanner.py -t 192.168.1.10 -p 22,80,443,8080
3. Scan a Whole Subnet (High Speed)
Scan the entire local network using 500 threads.

bash

python3 scanner.py -t 192.168.1.0/24 --threads 500
4. Stealth SYN Scan (Requires Root)
Perform a stealth scan (Half-open) which is harder to detect.

bash

sudo python3 scanner.py -t 192.168.1.10 --type syn
5. UDP Scan with Service Detection
Scan for open UDP services.

bash

python3 scanner.py -t 192.168.1.10 --type udp -p 53,67,123
📄 Output Reports
After the scan completes, two files are generated in the current directory:

1. scan_results.json
Contains detailed structured data including status, service, banners, and potential CVEs.

json

{
  "target": "192.168.1.10",
  "stats": {
    "scan_duration": "1.45s",
    "open_ports": 2,
    "total_ports": 1024
  },
  "results": [
    {
      "port": 80,
      "status": "open",
      "service": "http",
      "banner": "HTTP/1.1 200 OK\nServer: nginx/1.18.0...",
      "vuln": "Check nginx CVE-2021-23017"
    }
  ]
}
2. scan_results.xml
Standard XML format for integration with other tools or reporting systems.

⚠️ Disclaimer
This tool is intended for educational purposes and authorized network testing only. Scanning networks without permission is illegal. The authors are not responsible for any misuse of this software. Always obtain permission before scanning any network or device that you do not own.

📝 License
This project is licensed under the MIT License - see the LICENSE file for details.


Made with ❤️ by **noobuser978-gif**
