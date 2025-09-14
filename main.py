import subprocess
import time
import os


user_path = os.path.expanduser("~")+"/"
data_path = user_path+".local/share/LibreRecall"
config_path = user_path+ ".config/LibreRecall"

os.makedirs(data_path, exist_ok=True)
os.makedirs(config_path, exist_ok=True)

working_path = "/usr/bin/LibreRecall"


# File di configurazione
config_file = f"{config_path}/service.conf"

# Comandi dei processi (nome: comando)
process_commands = {
    "LibreRecall_daemon": ["python", "-u", f"{working_path}/take-screenshot.py"]    
}

# Stato dei processi attivi (nome: subprocess)
active_processes = {}

def read_config():
    """Legge il file e restituisce un dizionario {processo: True/False}"""
    config = {}
    try:
        with open(config_file, "r") as f:
            for line in f:
                line = line.strip()
                if not line or "=" not in line:
                    continue
                name, status = line.split("=", 1)
                config[name.strip()] = status.strip().lower() == "enable"
    except FileNotFoundError:
        pass
    return config

def update_processes():
    global active_processes
    config = read_config()
    
    for name, command in process_commands.items():
        enabled = config.get(name, False)
        running = name in active_processes

        if enabled and not running:
            # Avvia processo
            print(f"Avvio processo: {name}")
            active_processes[name] = subprocess.Popen(command)
        elif not enabled and running:
            # Ferma processo
            print(f"Fermo processo: {name}")
            active_processes[name].terminate()
            try:
                active_processes[name].wait(timeout=5)
            except subprocess.TimeoutExpired:
                active_processes[name].kill()
            del active_processes[name]

def main():
    try:
        while True:
            update_processes()
            time.sleep(2)
    except KeyboardInterrupt:
        print("Terminazione script...")
        # Ferma tutti i processi attivi
        for p in active_processes.values():
            p.terminate()
            try:
                p.wait(timeout=5)
            except subprocess.TimeoutExpired:
                p.kill()

if __name__ == "__main__":
    main()
