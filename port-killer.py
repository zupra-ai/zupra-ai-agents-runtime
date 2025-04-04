#!/usr/bin/env python3
import sys
import subprocess
import platform

def kill_process_using_port(port):
    """
    Finds the process(es) listening on a given port and kills them.
    This function attempts to be cross-platform, using:
      - On Windows: netstat -ano + taskkill
      - On Unix-like: lsof -i :port or netstat -anp + kill
    """
    system_name = platform.system().lower()
    if 'windows' in system_name:
        # Use netstat -ano and parse the PID
        # Example output line:
        #   TCP    0.0.0.0:8080           0.0.0.0:0              LISTENING       1234
        cmd = f'netstat -ano | findstr :{port}'
        try:
            netstat_output = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT)
            lines = netstat_output.decode().strip().split('\n')
            
            pids = set()
            for line in lines:
                parts = line.split()
                if len(parts) >= 5:
                    pid = parts[-1]
                    pids.add(pid)
            
            if not pids:
                print(f"No process found listening on port {port}.")
                return
            
            for pid in pids:
                try:
                    taskkill_cmd = f'taskkill /F /PID {pid}'
                    subprocess.check_call(taskkill_cmd, shell=True)
                    print(f"Killed process with PID {pid} on port {port}.")
                except subprocess.CalledProcessError:
                    print(f"Failed to kill process with PID {pid}.")
        except subprocess.CalledProcessError:
            print(f"No process found listening on port {port} (Windows).")
    else:
        # On macOS / Linux, try lsof first; if not installed, fallback to netstat.
        # 1) lsof approach
        #   lsof -t -i :<port> gives only PIDs in plain text, one per line.
        #   (Optionally filter by LISTEN, e.g. -sTCP:LISTEN on newer lsof)
        
        lsof_cmd = f'lsof -t -i :{port}'
        try:
            lsof_output = subprocess.check_output(lsof_cmd, shell=True, stderr=subprocess.STDOUT)
            pids = set(l.strip() for l in lsof_output.decode().split('\n') if l.strip())
            if not pids:
                print(f"No process found listening on port {port}.")
                return
            
            for pid in pids:
                try:
                    kill_cmd = f'kill -9 {pid}'
                    subprocess.check_call(kill_cmd, shell=True)
                    print(f"Killed process with PID {pid} on port {port}.")
                except subprocess.CalledProcessError:
                    print(f"Failed to kill PID {pid}.")
        except subprocess.CalledProcessError:
            # If lsof fails, we can attempt netstat.
            # netstat -anp might require sudo on some systems, so be aware.
            # Sample line:
            # tcp        0      0 0.0.0.0:9000            0.0.0.0:*               LISTEN      1234/python
            print("`lsof` not available or no process found; trying netstat fallback.")
            cmd = f'netstat -anp 2>/dev/null | grep :{port} | grep LISTEN'
            try:
                netstat_output = subprocess.check_output(cmd, shell=True)
                lines = netstat_output.decode().strip().split('\n')
                
                pids = set()
                for line in lines:
                    parts = line.split()
                    # Usually the PID/program is in the last column in format "1234/program"
                    # Let's parse that for the PID:
                    if len(parts) >= 7:
                        pid_program = parts[-1]
                        if '/' in pid_program:
                            pid = pid_program.split('/')[0]
                            pids.add(pid)
                
                if not pids:
                    print(f"No process found listening on port {port} (netstat).")
                    return
                
                for pid in pids:
                    try:
                        kill_cmd = f'kill -9 {pid}'
                        subprocess.check_call(kill_cmd, shell=True)
                        print(f"Killed process with PID {pid} on port {port}.")
                    except subprocess.CalledProcessError:
                        print(f"Failed to kill PID {pid}.")
            except subprocess.CalledProcessError:
                print(f"No process found listening on port {port} (Unix netstat).")

def main():
    if len(sys.argv) < 2:
        print("Usage: python kill_port.py <port>")
        sys.exit(1)
    
    port = sys.argv[1]
    kill_process_using_port(port)
    sys.exit(0)

if __name__ == "__main__":
    main()
