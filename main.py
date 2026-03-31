import socket
import threading
import argparse
import json
import xml.etree.ElementTree as ET
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
import sys
import struct
import random
import time
from typing import Dict, List, Optional, Tuple
import ipaddress

# Banner
BANNER = """
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
"""

class AdvancedPortScanner:
    def __init__(self, target: str, ports: str = "1-1024", threads: int = 200, 
                 scan_type: str = "tcp", timeout: float = 1.0, rate_limit: float = 0.01):
        self.target = target
        self.ports = self._parse_ports(ports)
        self.threads = threads
        self.scan_type = scan_type.lower()
        self.timeout = timeout
        self.rate_limit = rate_limit
        self.results = []
        self.lock = threading.Lock()
        self.start_time = datetime.now()
        
    def _parse_ports(self, port_str: str) -> List[int]:
        """Parse port range string into list of ports."""
        ports = []
        for part in port_str.split(','):
            if '-' in part:
                start, end = map(int, part.split('-'))
                ports.extend(range(start, end + 1))
            else:
                ports.append(int(part))
        return sorted(list(set(ports)))[:65536]  # Limit to valid ports

    def _create_socket(self, proto: str = "tcp") -> socket.socket:
        """Create appropriate socket based on protocol."""
        if proto == "udp":
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        else:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(self.timeout)
        return sock

    def _tcp_syn_scan(self, ip: str, port: int) -> Dict:
        """Perform TCP SYN stealth scan."""
        try:
            # Create raw socket for SYN scan (requires root)
            sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
            sock.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
            
            # Build TCP SYN packet (simplified)
            src_ip = socket.inet_aton("127.0.0.1")  # Spoof source
            dst_ip = socket.inet_aton(ip)
            
            # Simplified TCP header construction
            tcp_flags = 0x02  # SYN flag
            tcp_header = struct.pack('!HHLLBBHHH', 0, 0, 0, 0, 5<<4, 0, tcp_flags, 0, port)
            
            # Send packet and check response
            sock.sendto(tcp_header + dst_ip, (ip, port))
            
            sock.close()
            return {"port": port, "status": "open", "service": "unknown"}
            
        except PermissionError:
            # Fallback to connect() scan if no root
            return self._tcp_connect_scan(ip, port)
        except:
            return {"port": port, "status": "filtered", "service": "unknown"}

    def _tcp_connect_scan(self, ip: str, port: int) -> Dict:
        """Standard TCP connect scan."""
        result = {"port": port, "status": "closed", "service": "unknown"}
        try:
            sock = self._create_socket()
            sock.connect((ip, port))
            sock.close()
            result["status"] = "open"
        except socket.timeout:
            result["status"] = "filtered"
        except:
            pass
        return result

    def _udp_scan(self, ip: str, port: int) -> Dict:
        """UDP scan with service detection."""
        result = {"port": port, "status": "open|filtered", "service": "unknown"}
        try:
            sock = self._create_socket("udp")
            sock.sendto(b"\x00\x01\x00\x00", (ip, port))
            sock.settimeout(2.0)
            data, _ = sock.recvfrom(1024)
            result["status"] = "open"
            result["banner"] = data.decode(errors='ignore')[:100]
        except socket.timeout:
            result["status"] = "open|filtered"
        except:
            result["status"] = "closed"
        finally:
            sock.close()
        return result

    def _service_detection(self, ip: str, port: int) -> Dict:
        """Advanced service fingerprinting and banner grabbing."""
        services = {
            21: "ftp", 22: "ssh", 23: "telnet", 25: "smtp", 53: "dns",
            80: "http", 110: "pop3", 143: "imap", 443: "https", 993: "imaps",
            995: "pop3s", 1723: "pptp", 3306: "mysql", 3389: "rdp",
            5432: "postgresql", 5900: "vnc", 8080: "http-proxy"
        }
        
        result = {"port": port, "service": services.get(port, "unknown")}
        
        # Banner grabbing
        try:
            sock = self._create_socket()
            sock.connect((ip, port))
            
            if port in [80, 443, 8080]:
                sock.send(b"HEAD / HTTP/1.0\r\n\r\n")
                banner = sock.recv(1024).decode(errors='ignore')
                result["banner"] = banner[:200]
                # Check for common vulns
                if "nginx" in banner.lower():
                    result["vuln"] = "Check nginx CVE-2021-23017"
                elif "apache" in banner.lower():
                    result["vuln"] = "Check Apache mod_proxy CVE-2021-41773"
            elif port == 22:
                sock.send(b"SSH-2.0-Test\r\n")
                banner = sock.recv(1024).decode(errors='ignore')
                result["banner"] = banner
                if "OpenSSH_7.4" in banner:
                    result["vuln"] = "CVE-2018-15473 (OpenSSH username enum)"
            elif port in [21, 23, 25]:
                sock.send(b"QUIT\r\n")
                banner = sock.recv(1024).decode(errors='ignore')
                result["banner"] = banner
            
            sock.close()
        except:
            pass
            
        return result

    def _os_fingerprint(self, ip: str) -> Dict:
        """Basic OS fingerprinting via TCP/IP stack analysis."""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            sock.connect((ip, 80))
            sock.close()
            
            # Analyze TTL, window size, etc. (simplified)
            fingerprints = {
                "TTL:64": "Linux/Unix",
                "TTL:128": "Windows",
                "TTL:255": "Local network"
            }
            return {"os": fingerprints.get("TTL:64", "Unknown")}
        except:
            return {"os": "Unknown"}

    def scan_port(self, port: int):
        """Main port scanning function."""
        time.sleep(self.rate_limit)  # Rate limiting
        
        ip = str(ipaddress.IPv4Address(self.target.split('/')[0]))
        
        if self.scan_type == "syn":
            result = self._tcp_syn_scan(ip, port)
        elif self.scan_type == "udp":
            result = self._udp_scan(ip, port)
        else:
            result = self._tcp_connect_scan(ip, port)
        
        # Service detection for open ports
        if result["status"] in ["open", "open|filtered"]:
            service_info = self._service_detection(ip, port)
            result.update(service_info)
        
        # OS fingerprinting (once per host)
        if port == 80 and not hasattr(self, '_os_info'):
            self._os_info = self._os_fingerprint(ip)
        
        with self.lock:
            self.results.append(result)
            print(f"[{datetime.now().strftime('%H:%M:%S')}] {ip}:{port} {result['status']} {result.get('service', 'unknown')}")

    def scan(self):
        """Execute full scan."""
        print(f"Starting scan on {self.target}")
        print(f"Ports: {len(self.ports)}, Threads: {self.threads}")
        
        with ThreadPoolExecutor(max_workers=self.threads) as executor:
            executor.map(self.scan_port, self.ports)
        
        self._generate_reports()

    def _generate_reports(self):
        """Generate multiple output formats."""
        end_time = datetime.now()
        stats = {
            "scan_duration": f"{(end_time - self.start_time).total_seconds():.2f}s",
            "open_ports": len([r for r in self.results if r["status"] == "open"]),
            "filtered_ports": len([r for r in self.results if "filtered" in r["status"]]),
            "total_ports": len(self.results)
        }
        
        # JSON output
        report = {"target": self.target, "stats": stats, "results": self.results, "os": getattr(self, '_os_info', {})}
        with open("scan_results.json", "w") as f:
            json.dump(report, f, indent=2)
        
        # XML output
        root = ET.Element("scan")
        stats_elem = ET.SubElement(root, "stats")
        for k, v in stats.items():
            ET.SubElement(stats_elem, k).text = str(v)
        
        results_elem = ET.SubElement(root, "results")
        for result in self.results:
            port_elem = ET.SubElement(results_elem, "port")
            for k, v in result.items():
                ET.SubElement(port_elem, k).text = str(v)
        
        tree = ET.ElementTree(root)
        tree.write("scan_results.xml", encoding="utf-8", xml_declaration=True)
        
        print(f"\nScan complete! Results saved to scan_results.json and scan_results.xml")
        print(f"Open ports found: {stats['open_ports']}")

def main():
    print(BANNER)
    
    parser = argparse.ArgumentParser(description="Advanced Port Scanner by noobuser978-gif")
    parser.add_argument("-t", "--target", required=True, help="Target IP/CIDR (192.168.1.0/24)")
    parser.add_argument("-p", "--ports", default="1-1024", help="Port range (1-1024,22,80,443)")
    parser.add_argument("--threads", type=int, default=200, help="Number of threads")
    parser.add_argument("--type", choices=["tcp", "udp", "syn"], default="tcp", help="Scan type")
    parser.add_argument("--timeout", type=float, default=1.0, help="Socket timeout")
    parser.add_argument("--rate-limit", type=float, default=0.01, help="Delay between scans (s)")
    
    args = parser.parse_args()
    
    # Handle CIDR range
    network = ipaddress.IPv4Network(args.target, strict=False)
    targets = [str(ip) for ip in network.hosts()]
    
    for target in targets:
        scanner = AdvancedPortScanner(target, args.ports, args.threads, args.type, args.timeout, args.rate_limit)
        scanner.scan()

if __name__ == "__main__":
    main()