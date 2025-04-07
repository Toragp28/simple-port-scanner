import socket
import sys
import threading
from queue import Queue

ascii_art = '''
  ____               _____                     
 |  __ \             |  __ \                    
 | |__) |__ _ __ ___ | |__) |__  _ __ ___   __ _ 
 |  ___/ _ \ '__/ _ \|  ___/ _ \| '_ ` _ \ / _` |
 | |  |  __/ | | (_) | |  | (_) | | | | | | (_| |
 |_|   \___|_|  \___/|_|   \___/|_| |_| |_|\__, |
                                              __/ |
                                             |___/ 
'''

print(ascii_art)

# Configuration
NUM_THREADS = 100
queue = Queue()
open_ports = []

# Dictionnaire de ports communs (comme Nmap le fait)
common_ports = {
    21: 'FTP',
    22: 'SSH',
    23: 'Telnet',
    25: 'SMTP',
    53: 'DNS',
    80: 'HTTP',
    110: 'POP3',
    143: 'IMAP',
    443: 'HTTPS',
    3306: 'MySQL',
    3389: 'RDP',
    8080: 'HTTP-Proxy'
}

def scan_port(target, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.5)
        result = sock.connect_ex((target, port))
        if result == 0:
            service = common_ports.get(port, 'Unknown service')
            print(f"[OPEN] Port {port} ({service})")
            open_ports.append(port)
        sock.close()
    except:
        pass

def threader(target):
    while True:
        port = queue.get()
        scan_port(target, port)
        queue.task_done()

def run_scanner(target):
    print(f"\nScanning ports on {target} with {NUM_THREADS} threads...\n")

    for _ in range(NUM_THREADS):
        t = threading.Thread(target=threader, args=(target,), daemon=True)
        t.start()

    for port in range(1, 1000):  # ports 1 to 999
        queue.put(port)

    queue.join()

    print(f"\nScan finished! {len(open_ports)} open ports found.\n")

# Main
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python scanner.py <target_ip>")
        sys.exit(1)

    target_ip = sys.argv[1]
    try:
        run_scanner(target_ip)
    except Exception as e:
        print(f"An error occurred: {e}")

