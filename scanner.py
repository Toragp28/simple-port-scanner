import socket
import sys

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

 # Function to scan ports on a target IP address
def scan(target):
    print(f"Scanning ports on {target}...\n")
    for port in range(1, 65535):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((target, port))
        
        if result == 0:
            print(f"Port {port} is OPEN")
        sock.close()

# Main execution
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 scanner.py <target_ip>")
        sys.exit(1)

    target_ip = sys.argv[1]
    scan(target_ip)
