import subprocess, time, os, signal, sys

cwd = os.path.join(os.path.dirname(__file__), "backend")
pid_file = os.path.join(cwd, "server.pid")

def start():
    # Kill existing
    if os.path.exists(pid_file):
        try:
            with open(pid_file) as f:
                pid = int(f.read().strip())
            os.kill(pid, signal.SIGTERM)
            time.sleep(2)
        except:
            pass

    proc = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"],
        cwd=cwd,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        creationflags=subprocess.DETACHED_PROCESS,
        close_fds=True,
    )
    with open(pid_file, "w") as f:
        f.write(str(proc.pid))
    print(f"Server started (PID: {proc.pid})")

    # Wait for it
    import urllib.request
    for i in range(20):
        try:
            r = urllib.request.urlopen("http://localhost:8000/health", timeout=2)
            print(f"Server ready: {r.read().decode()}")
            return
        except:
            time.sleep(1)
    print("Server failed to start")

if __name__ == "__main__":
    start()
