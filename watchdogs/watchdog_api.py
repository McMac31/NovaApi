import subprocess
import re
from datetime import datetime

SERVICE = "flaskapi.service"
LOG_PATTERN = re.compile(r"ProtocolError.*(404|504)")

def log(msg):
    with open("/var/log/watchdog_journal.log", "a") as f:
        f.write(f"{datetime.now()} - {msg}\n")

def restart_service():
    subprocess.run(["systemctl", "restart", SERVICE])
    log("Servicio reiniciado por watchdog de journal")

def monitor_journal():
    cmd = ["journalctl", "-u", SERVICE, "-f", "-n", "0"]
    with subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True) as proc:
        for line in proc.stdout:
            if LOG_PATTERN.search(line):
                log(f"Error detectado: {line.strip()}")
                restart_service()

if __name__ == "__main__":
    monitor_journal()
