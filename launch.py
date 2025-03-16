import subprocess
import threading
import platform


def stream_output(process, prefix):
    """
    Stream output from a process (stdout and stderr).
    """
    for line in iter(process.stdout.readline, b""):
        print(f"{prefix}: {line.strip()}")
    process.stdout.close()

    for line in iter(process.stderr.readline, b""):
        print(f"{prefix} (ERR): {line.strip()}")
    process.stderr.close()


def run_apps():
    # Command to run the React app
    react_command = "yarn dev"  # Replace with `npm start` if you use npm

    # Command to run the FastAPI app
    # Adjust `main:app` to match your FastAPI app module
    fastapi_command = "./venv/Scripts/python.exe -m uvicorn app.main:app --reload --port 9000 --host 0.0.0.0"

    # Determine the shell option based on the operating system
    shell_option = platform.system() == "Windows"

    # Start the React app
    # react_process = subprocess.Popen(
    #     react_command,
    #     shell=shell_option,
    #     cwd="./web_app",  # Replace with the path to your React app
    #     stdout=subprocess.PIPE,
    #     stderr=subprocess.PIPE
    # )

    # Start the FastAPI app
    fastapi_process = subprocess.Popen(
        fastapi_command,
        shell=shell_option,
        cwd="./",  # Replace with the path to your FastAPI app
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    print("React and FastAPI apps are running...")

    # Start threads to stream logs from both processes
    
    fastapi_thread = threading.Thread(
        target=stream_output, args=(fastapi_process, "FastAPI"))
    
    # react_thread = threading.Thread(
    #     target=stream_output, args=(react_process, "React"))

    fastapi_thread.start()
    # react_thread.start()

    try:
        # Wait for the processes to complete
      
        fastapi_process.wait()
        # react_process.wait()
    except KeyboardInterrupt:
        print("\nShutting down...")
        # Terminate both processes on Ctrl+C
        # react_process.terminate()
        fastapi_process.terminate()


if __name__ == "__main__":
    run_apps()
