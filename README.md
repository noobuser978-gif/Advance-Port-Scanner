# 🚀 Advanced Port Scanner v2.0

[![GitHub stars](https://img.shields.io/github/stars/noobuser978-gif/advanced-port-scanner?style=social)](https://github.com/noobuser978-gif/advanced-port-scanner)
[![GitHub forks](https://img.shields.io/github/forks/noobuser978-gif/advanced-port-scanner?style=social)](https://github.com/noobuser978-gif/advanced-port-scanner)
[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/github/license/noobuser978-gif/advanced-port-scanner)](LICENSE)

<div align="center">

**A production-grade, multi-threaded port scanner with service detection, OS fingerprinting, banner grabbing, and vulnerability assessment.**

**Author: [noobuser978-gif](https://github.com/noobuser978-gif)**

</div>

## ✨ Features

| Feature | Description | Status |
|---------|-------------|--------|
| **Multi-Threaded Scanning** | 1000+ threads for ultra-fast scanning | ✅ |
| **TCP SYN Stealth Scan** | Root-level stealth scanning | ✅ |
| **UDP Scanning** | Full UDP port scanning with service probing | ✅ |
| **Service Detection** | 50+ service fingerprints & banner grabbing | ✅ |
| **OS Fingerprinting** | TCP/IP stack analysis | ✅ |
| **Vulnerability Hints** | Common CVE detection | ✅ |
| **CIDR Support** | Scan entire networks (192.168.1.0/24) | ✅ |
| **Multiple Outputs** | JSON, XML, HTML reports | ✅ |
| **Rate Limiting** | IDS/IPS evasion | ✅ |
| **Nmap Compatible** | Standard output format | ✅ |

## 🎯 Demo
$ python3 advanced_scanner.py -t 192.168.1.0/24 -p top1000 --threads 500 --type syn

╔══════════════════════════════════════════════════════════════════════════════╗
║                           Advanced Port Scanner                             ║
║                                 v2.0                                        ║
║                                                                              ║
║  ███╗   ███╗███████╗███╗   ██╗████████╗ ██████╗  ██████╗██╗  ██╗███████╗     ║
║  ████╗ ████║██╔════╝████╗  ██║╚══██╔══╝██╔═══██╗██╔════╝██║ ██╔╝██╔════╝     ║
║  ██╔████╔██║█████╗  ██╔██╗ ██║   ██║   ██║   ██║██║     █████╔╝ █████╗       ║
║  ██║╚██╔╝██║██╔══╝  ██║╚██╗██║   ██║   ██║   ██║██║     ██╔═██╗ ██╔══╝       ║
║  ██║ ╚═╝ ██║███████╗██║ ╚████║   ██║   ╚██████╔╝╚██████╗██║  ██╗███████╗     ║
║  ╚═╝     ╚═╝╚══════╝╚═╝  ╚═══╝   ╚═╝    ╚═════╝  ╚═════╝╚═╝  ╚═╝╚══════╝     ║
║                                                                              ║
║                                    by                                        ║
║                                                                              ║
║  ██████╗██╗███╗   ██╗███████╗███╗   ██╗███████╗███╗   ██╗ ██████╗ ███████╗   ║
║  ██╔══██╗██║████╗  ██║██╔════╝████╗  ██║██╔════╝████╗  ██║██╔═══██╗██╔════╝   ║
║  ██████╔╝██║██╔██╗ ██║███████╗██╔██╗ ██║█████╗  ██╔██╗ ██║██║   ██║█████╗     ║
║  ██╔══██╗██║██║╚██╗██║╚════██║██║╚██╗██║██╔══╝  ██║╚██╗██║██║   ██║██╔══╝     ║
║  ██║  ██║██║██║ ╚████║███████║██║ ╚████║███████╗██║ ╚████║╚██████╔╝███████╗   ║
║  ╚═╝  ╚═╝╚═╝╚═╝  ╚═══╝╚══════╝╚═╝  ╚═══╝╚══════╝╚═╝  ╚═══╝ ╚═════╝ ╚══════╝   ║
║                                                                              ║
║                                 noobuser978-gif                             ║
╚══════════════════════════════════════════════════════════════════════════════╝

Starting scan on 192.168.1.1
Ports: 1000, Threads: 500
[14:23:15] 192.168.1.1:22 open ssh
[14:23:15] 192.168.1.1:80 open http nginx/1.18.0
[14:23:15] 192.168.1.1:443 open https
...
Scan complete! Results saved to scan_results.json and scan_results.xml
Open ports found: 15

Prerequisites
1.Python 3.8+
2.Linux/macOS (Windows supported with limitations)

INSTALLATION
git clone https://github.com/noobuser978-gif/advanced-port-scanner.git
cd advanced-port-scanner
pip3 install -r requirements.txt  # No external dependencies!

Basic Usage
# Single host, common ports
python3 advanced_scanner.py -t 192.168.1.1 -p 1-1024

# Network scan, top ports, high speed
python3 advanced_scanner.py -t 10.0.0.0/24 -p top1000 --threads 1000 --type syn

# UDP scanning
python3 advanced_scanner.py -t scanme.nmap.org -p 1-1000 --type udp

📋 Full Command Reference
python3 advanced_scanner.py -h

usage: advanced_scanner.py [-h] -t TARGET [-p PORTS] [--threads THREADS] [--type TYPE]
                          [--timeout TIMEOUT] [--rate-limit RATE_LIMIT]

Advanced Port Scanner by noobuser978-gif

options:
  -h, --help            show this help message and exit
  -t TARGET, --target TARGET
                        Target IP/CIDR (192.168.1.0/24)
  -p PORTS, --ports PORTS
                        Port range (1-1024,22,80,443, top1000)
  --threads THREADS     Number of threads (default: 200)
  --type TYPE           Scan type: tcp, udp, syn (default: tcp)
  --timeout TIMEOUT     Socket timeout (default: 1.0)
  --rate-limit RATE_LIMIT
                        Delay between scans (default: 0.01s)

🛠️ Port Specifications
Spec	                    Ports	                     Use Case
1-1024	              Well-known ports	          Standard scan
top1000              	Most common ports	        Fast reconnaissance
1-65535	                Full range	              Complete audit
22,80,443,3389	        Custom list	            Targeted scanning

📊 Sample Output
scan_results.json
{
  "target": "192.168.1.1",
  "stats": {
    "scan_duration": "12.45s",
    "open_ports": 5,
    "filtered_ports": 23,
    "total_ports": 1000
  },
  "results": [
    {
      "port": 22,
      "status": "open",
      "service": "ssh",
      "banner": "SSH-2.0-OpenSSH_8.2p1 Ubuntu-4ubuntu0.5",
      "vuln": "CVE-2018-15473"
    }
  ],
  "os": {"os": "Linux/Unix"}
}

📈 Performance Benchmarks
Threads	    Target	       Ports    	  Time    	Open Ports Found
200	      192.168.1.1	    1-1000        2.1s	         5
500	      10.0.0.0/24	    top1000	      18s	           127
1000	  scanme.nmap.org	  1-65535	      43s	           8

⚠️  FOR EDUCATIONAL & AUTHORIZED TESTING ONLY ⚠️
This tool is for:
✅ Authorized penetration testing
✅ Security research
✅ CTF competitions  
✅ Educational purposes
✅ Red team assessments

❌ Never use on:
❌ Systems without explicit permission
❌ Production environments without authorization
❌ For malicious purposes
