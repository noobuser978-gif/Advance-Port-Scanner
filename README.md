Advanced Port Scanner
Multi-threaded port scanner with service detection and multiple output formats.

Features
-TCP, UDP, and SYN scans

-Multi-threaded with configurable threads

-Service detection and banner grabbing

-JSON and XML output

-CIDR subnet support

Installation

   git clone https://github.com/yourusername/advanced-port-scanner.git
   cd advanced-port-scanner
   
Usage

   python main.py -t <target> [options]

Examples
   # Scan single host default ports (1-1024)
      
   python main.py -t 192.168.1.1
   
   # Scan full subnet with custom ports
   
   python main.py -t 192.168.1.0/24 -p 1-1000
   
   # UDP scan on specific ports
   
   python main.py -t 10.0.0.1 -p 22,80,443 --type udp
   
   # Full port scan with more threads
   
   python main.py -t example.com -p 1-65535 --threads 500
   
Options
Option	       |         Description	           |   Default

-t,--target	  |       IP address or CIDR	      |   Required

-p, --ports	  |         Port range	            |     1-1024

--threads	    |       Number of threads	       |       200

--type        |      	tcp, udp, or syn	        |       tcp

--timeout	    |       Socket timeout           |      	1.0

--rate-limit  |    	Delay between scans        |      	0.01

