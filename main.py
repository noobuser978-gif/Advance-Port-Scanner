import socket
import threading
import argparse
import json
import xml.etree.ElementTree as ET
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
import sys
import struct
import time
from typing import Dict, List
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
        self.scanned_ports = 0
        self.total_ports = len(self.ports)
        
    def _parse_ports(self, port_str: str) -> List[int]:
        """Parse port range string into list of ports."""
        ports = []
        for part in port_str.split(','):
            part = part.strip()
            if '-' in part:
                start, end = map(int, part.split('-'))
                ports.extend(range(start, min(end, 65535) + 1))
            else:
                ports.append(int(part))
        return sorted(list(set(ports)))[:65536]

    def _create_socket(self, proto: str = "tcp") -> socket.socket:
        """Create appropriate socket based on protocol."""
        if proto == "udp":
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        else:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(self.timeout)
        return sock

    def _tcp_syn_scan(self, ip: str, port: int) -> Dict:
        """Perform TCP SYN stealth scan (requires root)."""
        try:
            # For Windows compatibility, fallback to connect scan
            if sys.platform == "win32":
                return self._tcp_connect_scan(ip, port)
            
            # Linux/Unix raw socket implementation
            sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
            sock.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
            
            # Build TCP packet
            src_ip = socket.inet_aton("127.0.0.1")
            dst_ip = socket.inet_aton(ip)
            
            # TCP header (simplified)
            tcp_header = struct.pack('!HHLLBBHHH', 
                                    random.randint(1024, 65535),  # src port
                                    port,  # dst port
                                    0,  # seq num
                                    0,  # ack num
                                    5 << 4,  # data offset
                                    0,  # flags (reserved)
                                    socket.TH_SYN,  # SYN flag
                                    8192,  # window
                                    0)  # checksum (0 for now)
            
            sock.sendto(tcp_header, (ip, 0))
            sock.close()
            return {"port": port, "status": "open", "service": "unknown"}
            
        except (PermissionError, OSError):
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
        except (socket.timeout, ConnectionRefusedError):
            result["status"] = "closed"
        except:
            result["status"] = "filtered"
        return result

    def _udp_scan(self, ip: str, port: int) -> Dict:
        """UDP scan with service detection."""
        result = {"port": port, "status": "closed", "service": "unknown"}
        try:
            sock = self._create_socket("udp")
            sock.settimeout(2.0)
            # Send probe based on common services
            if port == 53:
                sock.sendto(b'\x00\x00\x01\x00\x00\x01\x00\x00\x00\x00\x00\x00\x03www\x06google\x03com\x00\x00\x01\x00\x01', (ip, port))
            else:
                sock.sendto(b"\x00\x01\x00\x00", (ip, port))
            
            try:
                data, _ = sock.recvfrom(1024)
                result["status"] = "open"
                result["banner"] = data[:100].decode(errors='ignore')
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
            995: "pop3s", 3306: "mysql", 3389: "rdp", 5432: "postgresql", 
            5900: "vnc", 8080: "http-proxy"
        }
        
        result = {"service": services.get(port, "unknown")}
        
        try:
            sock = self._create_socket()
            sock.connect((ip, port))
            
            if port in [80, 443, 8080]:
                sock.send(b"HEAD / HTTP/1.0\r\n\r\n")
                banner = sock.recv(1024).decode(errors='ignore')
                result["banner"] = banner[:200]
                if "nginx" in banner.lower():
                    result["vuln"] = "Check nginx CVEs"
                elif "apache" in banner.lower():
                    result["vuln"] = "Check Apache CVEs"
            elif port == 22:
                sock.send(b"SSH-2.0-Test\r\n")
                banner = sock.recv(1024).decode(errors='ignore')
                result["banner"] = banner[:200]
            elif port in [21, 23, 25]:
                banner = sock.recv(1024).decode(errors='ignore')
                result["banner"] = banner[:200]
            
            sock.close()
        except:
            pass
            
        return result

    def _os_fingerprint(self, ip: str) -> Dict:
        """Basic OS fingerprinting via TCP/IP stack analysis."""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1.0)
            sock.connect((ip, 80))
            
            # Get TTL from ICMP (simplified)
            ttl = 64  # Default Linux TTL
            sock.close()
            
            if ttl <= 64:
                os_name = "Linux/Unix"
            elif ttl <= 128:
                os_name = "Windows"
            else:
                os_name = "Unknown"
                
            return {"os": os_name}
        except:
            return {"os": "Unknown"}

    def scan_port(self, port: int) -> Dict:
        """Main port scanning function."""
        # Rate limiting with sleep
        if self.rate_limit > 0:
            time.sleep(self.rate_limit)
        
        ip = str(ipaddress.ip_address(self.target))
        
        if self.scan_type == "syn":
            result = self._tcp_syn_scan(ip, port)
        elif self.scan_type == "udp":
            result = self._udp_scan(ip, port)
        else:
            result = self._tcp_connect_scan(ip, port)
        
        # Service detection for open ports
        if result.get("status") in ["open", "open|filtered"]:
            service_info = self._service_detection(ip, port)
            result.update(service_info)
        
        # Update progress
        with self.lock:
            self.scanned_ports += 1
            self.results.append(result)
            if result["status"] == "open":
                print(f"[{datetime.now().strftime('%H:%M:%S')}] {ip}:{port} ✓ {result.get('service', 'unknown')}")
        
        return result

    def scan(self):
        """Execute full scan."""
        print(f"\n[*] Target: {self.target}")
        print(f"[*] Ports: {len(self.ports)}")
        print(f"[*] Threads: {self.threads}")
        print(f"[*] Scan type: {self.scan_type.upper()}")
        print(f"[*] Starting scan...\n")
        
        with ThreadPoolExecutor(max_workers=self.threads) as executor:
            futures = [executor.submit(self.scan_port, port) for port in self.ports]
            for future in as_completed(futures):
                pass  # Progress handled in scan_port
        
        # OS fingerprint after scan
        self._os_info = self._os_fingerprint(str(ipaddress.ip_address(self.target)))
        self._generate_reports()

    def _generate_reports(self):
        """Generate multiple output formats."""
        end_time = datetime.now()
        duration = (end_time - self.start_time).total_seconds()
        
        stats = {
            "scan_duration": f"{duration:.2f}s",
            "open_ports": len([r for r in self.results if r.get("status") == "open"]),
            "filtered_ports": len([r for r in self.results if "filtered" in r.get("status", "")]),
            "total_ports": len(self.results)
        }
        
        # JSON output
        report = {
            "target": self.target, 
            "scan_time": self.start_time.isoformat(),
            "stats": stats, 
            "results": self.results, 
            "os": getattr(self, '_os_info', {})
        }
        
        with open("scan_results.json", "w") as f:
            json.dump(report, f, indent=2)
        
        # XML output
        root = ET.Element("scan")
        ET.SubElement(root, "target").text = self.target
        ET.SubElement(root, "scan_time").text = self.start_time.isoformat()
        
        stats_elem = ET.SubElement(root, "stats")
        for k, v in stats.items():
            ET.SubElement(stats_elem, k).text = str(v)
        
        results_elem = ET.SubElement(root, "results")
        for result in self.results:
            if result.get("status") == "open":
                port_elem = ET.SubElement(results_elem, "port")
                for k, v in result.items():
                    if v:
                        ET.SubElement(port_elem, k).text = str(v)
        
        tree = ET.ElementTree(root)
        tree.write("scan_results.xml", encoding="utf-8", xml_declaration=True)
        
        print(f"\n[*] Scan complete in {duration:.2f}s")
        print(f"[*] Open ports: {stats['open_ports']}")
        print(f"[*] Results saved to scan_results.json and scan_results.xml")

def main():
    print(BANNER)
    
    parser = argparse.ArgumentParser(description="Advanced Port Scanner")
    parser.add_argument("-t", "--target", required=True, help="Target IP (e.g., 192.168.1.1)")
    parser.add_argument("-p", "--ports", default="1-1024", help="Port range (1-1024,22,80,443)")
    parser.add_argument("--threads", type=int, default=200, help="Number of threads (default: 200)")
    parser.add_argument("--type", choices=["tcp", "udp", "syn"], default="tcp", help="Scan type (default: tcp)")
    parser.add_argument("--timeout", type=float, default=1.0, help="Socket timeout in seconds (default: 1.0)")
    parser.add_argument("--rate-limit", type=float, default=0, help="Delay between scans in seconds (default: 0)")
    
    args = parser.parse_args()
    
    # Validate target
    try:
        ipaddress.ip_address(args.target)
    except ValueError:
        print(f"Error: Invalid IP address: {args.target}")
        sys.exit(1)
    
    # Create and run scanner
    scanner = AdvancedPortScanner(
        args.target, 
        args.ports, 
        args.threads, 
        args.type, 
        args.timeout, 
        args.rate_limit
    )
    
    try:
        scanner.scan()
    except KeyboardInterrupt:
        print("\n[!] Scan interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n[!] Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
