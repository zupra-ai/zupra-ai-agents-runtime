import re
from app.settings import settings
from app.tools_commons.base import build_core_class
from pathlib import Path
import time
from typing import Optional
import json
import os
import docker
from app.settings import settings
from fastapi import HTTPException
from app.clients.docker_client import docker_client as client

# try:
#     client = docker.from_env(
#         # version="auto",
#         # environment={
#         #     'DOCKER_TLS_VERIFY': '0', 
#         #     'DOCKER_HOST': 'tcp://192.168.1.154:2375',
#         # }
#     )
#     print("🟩   Connected docker")
# except Exception as e:
#     print("🔴   Error connection docker", f"{e}")


def remove_images_containers(image_name: str):
    try:

        # Step 1: List all containers using the image
        containers = client.containers.list(
            all=True, filters={'ancestor': image_name})
        
        print("Found", f"{len(containers)} containers associated to this image")

        # Step 2: Stop and remove each container
        for container in containers:
            print(f"Processing container {container.name} ({container.id})...")
            try:
                if container.status == 'running':
                    print(f"Stopping container {container.name}...")
                    container.stop()
                print(f"Removing container {container.name}...")
                container.remove()
                print(f"Container {container.name} removed successfully.")
            except docker.errors.APIError as e:
                print(f"Failed to remove container {container.name}: {e.explanation}")
    except:
        print("No containers found to remove.")


def remove_image(image_name: str):
    """
    Delete one image
    """
    try:
        remove_images_containers(image_name=image_name)
    except:
        pass
    try:
        client.images.remove(image=image_name, force=True)
    except docker.errors.ImageNotFound:
        raise HTTPException(
            status_code=500, detail=f"Image name [{image_name}] not found")


def create_docker_image_sources(unique_id: str,
                                base_image_name: str,
                                code: str,
                                requirements_txt: Optional[str],
                                environments_txt: Optional[str]):

    temp_dir = Path(f"/tmp/zupra-mcp--{unique_id}")
    temp_dir.mkdir(parents=True, exist_ok=True)

    # temp_dir = Path(f"/tmp/{unique_id}")
    # temp_dir.mkdir(parents=True, exist_ok=True)

    dockerfile_path = temp_dir / "Dockerfile"
    code_file_path = temp_dir / "code.py"
    zupra_code = temp_dir / "zupra_core.py"

    # Write the user's code to a file
    with open(code_file_path, encoding="utf-8", errors="replace", mode="w") as code_file:
        code_file.write(code)
        code_file.close()
    
    with open(zupra_code, encoding="utf-8", errors="replace", mode="w") as code_file:
        code_file.write(build_core_class())
        code_file.close()

    # If requirements are provided, save them to a file
    requirements_path = temp_dir / "requirements.txt"
    if requirements_txt is not None:
        with open(requirements_path, encoding="utf-8", errors="replace", mode="w") as req_file:
            req_file.write(requirements_txt + "\npython-dotenv\nrequests")

    environments_path = temp_dir / ".env"
    if environments_txt is not None:
        with open(environments_path, encoding="utf-8", errors="replace", mode="w") as req_file:
            req_file.write(environments_txt)

    # Create a Dockerfile dynamically
    # Create a Dockerfile dynamically with conditional requirements installation
    dockerfile_content = f"""
FROM {base_image_name}

# Create a non-root user
# RUN addgroup --system --gid 101 zupra_group
# RUN adduser --system --uid 101 --gid 101 zupra_user

# Switch to the new user
# USER zupra_user

WORKDIR /app
COPY code.py /app/code.py
COPY zupra_core.py /app/zupra_core.py
"""

    # Add requirements installation if requirements are provided
    if requirements_txt is not None:
        dockerfile_content += """
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt
"""

    if environments_txt:
        dockerfile_content += """
COPY .env /app/.env
        """

    # Final command to run the code in case we need start a server like rest o grpc
    # dockerfile_content += """
    # CMD ["python3", "/app/code.py"]
    # """

    with open(dockerfile_path, "w") as dockerfile:
        dockerfile.write(dockerfile_content)

    return temp_dir


def build_image(
        unique_id: str,
        temp_dir: str):

    image_prefix = "ztool-py"

    image_name = f"{image_prefix}-{unique_id}"

    print("🧑‍🏭 building image", image_name, temp_dir)

    try:
        image, build_logs = client.images.build(
            path=str(temp_dir), tag=image_name)

        errorDetails = {}

        # Print all build logs, including errors and warnings
        for chunk in build_logs:
            if 'stream' in chunk:
                print(chunk['stream'].strip())
            elif 'status' in chunk:
                line = chunk['status']
                if 'progress' in chunk:
                    line += f" {chunk['progress']}"
                if 'id' in chunk:
                    line = f"{chunk['id']}: {line}"
                print(line)
            elif 'errorDetail' in chunk:
                print("ErrorDetail:", chunk['errorDetail'])
                print("=======", chunk['errorDetail'].get("code"))
                if chunk['errorDetail'].get("code") == 1:
                    errorDetails["message"] = chunk['errorDetail'].get(
                        "message")

            elif 'error' in chunk:
                print("Error:", chunk['error'])
            else:
                # Print any other keys in the chunk
                print("JSON:", json.dumps(chunk, indent=2))

        if errorDetails.get("message") is not None:
            raise HTTPException(status_code=500, detail=f"Docker Build error:{errorDetails.get('message')}")

        # Get detailed image information
        # print(f"Image built successfully. ID: {image.id}")
        # image_info = client.images.get(image.id)
        # print(f"Image Tags: {image_info.tags}")
        # print(f"Image Size: {image_info.attrs['Size']} bytes")
        # print(f"Image Created: {image_info.attrs['Created']}")
        # Add any other relevant data you need from image_info.attrs

    except docker.errors.BuildError as e:
        # Print all error logs from the build process
        # print("BuildError:", str(e))
        # raise HTTPException(status_code=500, detail=f"Docker Build error:\n{data.get('errorDetail')}")
        # for log in e.build_log:
        #     try:
        #         data = json.loads(log)
        #         if data.get("errorDetail") is not None:

        #     except:
        #         pass
        raise HTTPException(
            status_code=500, detail=f"Docker Build Image Error:\n{str(e)}")

    except docker.errors.APIError as e:
        raise HTTPException(
            status_code=500, detail=f"Docker API error:\n{str(e)}")

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Unknown error:\n{str(e)}")

    finally:
        #  🟢 THIS MUST BE USED
        # Cleanup: remove the temporary directory and container after execution
        if os.path.exists(temp_dir):
            for file in temp_dir.glob("*"):
                file.unlink()
            temp_dir.rmdir()
        pass

    return {
        "image_name": image_name,
        "image_id": image.id
    }


def run_container(image_name: str, params: dict, auto_remove=False):
    try:
        params_json = json.dumps(params)

        startTime = time.time()
        # Run the Docker container with resource limits

        # Wait for the container to complete with a timeout and capture output
        try:
            params_json = params_json.replace("\'","`")
            command = "python3 /app/code.py '" + params_json + "'"
            
            container = client.containers.run(
                image=image_name,
                command=command,
                # user="zupra_user",
                read_only=True,  # Make filesystem read-only
                pids_limit=100,
                detach=True, # Run in bg mode
                # security_opt=["seccomp=default.json"],  # Use seccomp profile
                stdout=True,
                stderr=True,
                mem_reservation="50m",
                mem_limit="512m",  # Memory limit of 128MB
                cpu_period=100000,
                cpu_quota=50000,   # Limit to 50% of one CPU
                # cpus=0.5,  # see if offer better performance
                # auto_remove=True,
                volumes={
                    '/tmp/sandbox': {'bind': '/tmp', 'mode': 'rw'}
                }  # Isolated /tmp folder
                
            )

            container.wait(timeout=settings.max_container_exec_time)

            output = container.logs().decode("utf-8")
            
            success_result_regexp = r'___zupra_result_success_start\s*(.*?)\s*___zupra_result_success_end'
            success_result_match = re.search(success_result_regexp, output, re.DOTALL)

            
            error_result_regexp = r'___zupra_result_error_start\s*(.*?)\s*___zupra_result_error_start'
            error_result_match = re.search(error_result_regexp, output, re.DOTALL)
            
            outside_matches = ""
            
            is_success = True
            if success_result_match:
                important_data = success_result_match.group(1)
                execution_output = important_data.strip()
                
                pattern_split = r'___zupra_result_success_start.*?___zupra_result_success_end\s*'
                outside_parts = re.split(pattern_split, output, flags=re.DOTALL)
                outside_matches = "\n".join([part.strip() for part in outside_parts if part.strip()])
            elif error_result_match:
                is_success = False
                important_data = error_result_match.group(1)
                execution_output = important_data.strip()
                
                pattern_split = r'___zupra_result_error_start.*?___zupra_result_error_start\s*'
                outside_parts = re.split(pattern_split, output, flags=re.DOTALL)
                outside_matches = "\n".join([part.strip() for part in outside_parts if part.strip()])
            else:
                execution_output = "none_result"
            
            if settings.delete_container_after_ran != "0":
                container.remove()

            if auto_remove:
                try:
                    client.images.remove(image=image_name, force=True)
                    print(f"Image {image_name} removed")
                except docker.errors.ImageNotFound:
                    print("Error removing image")


            return {
                "output_encode": "utf-8",
                "output": execution_output,
                "output_logs": outside_matches,
                "success": is_success,
                "start_time": startTime,
                "end_time": time.time(),
                "up_time": time.time() - startTime
            }
        except docker.errors.ContainerError as e:
            print("🟥   Error running container", f"{e}")
            raise HTTPException(
                status_code=500, detail="Error executing the code in the container.")
            

    except docker.errors.BuildError as e:
        print("Error running", e)
        raise HTTPException(status_code=500, detail=f"Build running:\n{str(e)}")
