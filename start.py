import subprocess
import os
import sys

def is_process_running(lock_file):
    return os.path.exists(lock_file)

def ensure_directory_exists(directory):
    if not os.path.exists(directory):
        try:
            os.makedirs(directory)
        except OSError as e:
            print(f"Failed to create directory {directory}: {e}")
            return False
    return True

def start_process(directory, script):
    directory_path = os.path.abspath(directory)
    if not ensure_directory_exists(directory_path):
        return
    script_path = os.path.join(directory_path, script)
    lock_file = f"{script_path}.lock"
    if is_process_running(lock_file):
        print(f"{script} is already running.")
        return
    try:
        with open(lock_file, 'w') as f:
            f.write("lock")
        process = subprocess.Popen([sys.executable, script_path], cwd=directory_path)
        print(f"Started {script} with PID {process.pid}")
        return process
    except Exception as e:
        print(f"Failed to start {script}: {e}")
    finally:
        if os.path.exists(lock_file):
            os.remove(lock_file)

if __name__ == "__main__":
    processes = []
    processes.append(start_process("bot", "main.py"))
    processes.append(start_process("webui", "app.py"))

    for process in processes:
        if process is not None:
            process.wait()
