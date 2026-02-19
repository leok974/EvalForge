import sys
from pathlib import Path

def main():
    root = Path(".")
    outputs = root / "outputs"
    outputs.mkdir(exist_ok=True)
    
    # Process netstat output to extract ports
    # Input: fixtures/netstat.txt
    # Format: Proto LocalAddress ...
    #         tcp   0.0.0.0:8000 ...
    
    public_ports = []
    localhost_ports = []

    try:
        with open("fixtures/netstat.txt", "r", encoding="utf-8") as f:
            lines = f.readlines()
            
        # Skip header? Header usually line 1.
        # Logic: split by whitespace. column 1 (0-indexed) is Proto, col 2 is LocalAddress.
        # address is IP:PORT.
        
        for line in lines[1:]: # detailed logic: tail -n +2
            parts = line.strip().split()
            if len(parts) < 4: continue
            
            local_addr = parts[1]
            prog = parts[3] # col 4
            
            if ":" in local_addr:
                host, port = local_addr.split(":", 1)
                
                # Logic from task.sh:
                # if host=="0.0.0.0" print port, prog -> public loops
                # if host=="127.0.0.1" print port, prog -> localhost loops
                
                if host == "0.0.0.0":
                    public_ports.append((int(port), prog))
                elif host == "127.0.0.1":
                    localhost_ports.append((int(port), prog))
                    
        # Sort by numeric port
        public_ports.sort(key=lambda x: x[0])
        localhost_ports.sort(key=lambda x: x[0])
        
        with open(outputs / "public_ports.txt", "w", encoding="utf-8") as f:
            for p, prog in public_ports:
                f.write(f"{p} {prog}\n")
                
        with open(outputs / "localhost_ports.txt", "w", encoding="utf-8") as f:
            for p, prog in localhost_ports:
                f.write(f"{p} {prog}\n")
                
    except Exception as e:
        print(f"Error processing netstat: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
