# #!/usr/bin/env python
# import subprocess
# import sys
# import os




# def main():
#     # Commands to run
#     python_cmd = [
#         os.path.join(".", "venv", "Scripts", "python.exe"),
#         "-m", "uvicorn",
#         "app.main:app",
#         "--reload",
#         "--port", "9000",
#         "--host", "0.0.0.0"
#     ]
#     nextjs_cmd = ["yarn", "dev"]

#     # Open log files
#     python_log = open("python_service.log", "w")
#     nextjs_log = open("nextjs_service.log", "w")

#     # Start the Python FastAPI service
#     print("Starting Python FastAPI Service...")
#     python_process = subprocess.Popen(
#         python_cmd,
#         stdout=python_log,
#         stderr=subprocess.STDOUT,
#         shell=True
#     )

#     # Start the Next.js service (in the ./web_app folder)
#     print("Starting Next.js Service...")
#     nextjs_process = subprocess.Popen(
#         nextjs_cmd,
#         stdout=nextjs_log,
#         stderr=subprocess.STDOUT,
#         shell=True,
#         cwd="./web_app"  # run command from the "web_app" directory
#     )

#     # Wait for both processes to exit (e.g., if user kills the script)
#     try:
#         python_returncode = python_process.wait()
#         nextjs_returncode = nextjs_process.wait()
#     except KeyboardInterrupt:
#         print("Terminating both services...")
#         python_process.terminate()
#         nextjs_process.terminate()

#     # Close log files
#     python_log.close()
#     nextjs_log.close()

#     print("Services have stopped.")

# if __name__ == "__main__":
#     sys.exit(main())


#!/usr/bin/env python3
import subprocess
import sys
import os
import threading

def stream_output(pipe, prefix, log_file):
    """
    Reads lines from the given pipe, writes them to a log file,
    and prints them to the console in real-time.
    """
    try:
        for line in iter(pipe.readline, b''):
            decoded_line = line.decode(errors='replace')
            # Print to console (with prefix)
            print(prefix + decoded_line, end='')
            # Write to log file
            log_file.write(decoded_line)
            log_file.flush()
    finally:
        pipe.close()

def main():
    # Define commands
    python_cmd = [
        os.path.join(".", "venv", "Scripts", "python.exe"),
        "-m", "uvicorn",
        "app.main:app",
        "--reload",
        "--port", "9000",
        "--host", "0.0.0.0"
    ]
    nextjs_cmd = ["yarn", "dev"]

    # Start FastAPI (capture stdout/stderr in pipes)
    print("Starting Python FastAPI Service...")
    python_process = subprocess.Popen(
        python_cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=True  # Typically needed on Windows to allow command with spaces
    )

    # Start Next.js (capture stdout/stderr in pipes)
    print("Starting Next.js Service...")
    nextjs_process = subprocess.Popen(
        nextjs_cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=True,
        cwd="./web_app"  # run inside the "web_app" folder
    )

    # Open log files in "append" mode (or "w" if you prefer overwrite)
    python_log = open("logs/web_api.log", "a", encoding="utf-8")
    nextjs_log = open("logs/web_app.log", "a", encoding="utf-8")

    # Create threads to stream output
    # FastAPI stdout + stderr
    python_stdout_thread = threading.Thread(
        target=stream_output, args=(python_process.stdout, "\033[32m FastAPI> ", python_log)
    )
    python_stderr_thread = threading.Thread(
        target=stream_output, args=(python_process.stderr, "🔴 FastAPI_ERR> ", python_log)
    )

    # Next.js stdout + stderr
    nextjs_stdout_thread = threading.Thread(
        target=stream_output, args=(nextjs_process.stdout, "\033[33m NextJS> ", nextjs_log)
    )
    nextjs_stderr_thread = threading.Thread(
        target=stream_output, args=(nextjs_process.stderr, "🔴 NextJS_ERR> ", nextjs_log)
    )

    # Start threads
    python_stdout_thread.start()
    python_stderr_thread.start()
    nextjs_stdout_thread.start()
    nextjs_stderr_thread.start()

    try:
        # Wait for both processes to complete
        python_process.wait()
        nextjs_process.wait()
    except KeyboardInterrupt:
        print("Received KeyboardInterrupt. Terminating both services...")
        python_process.terminate()
        nextjs_process.terminate()

    # Ensure threads terminate
    python_stdout_thread.join()
    python_stderr_thread.join()
    nextjs_stdout_thread.join()
    nextjs_stderr_thread.join()

    # Close log files
    python_log.close()
    nextjs_log.close()

    print("Services have stopped.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
