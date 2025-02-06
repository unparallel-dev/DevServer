import docker
import socket
import random
from uuid import uuid4



client = docker.from_env()
image_name = "lscr.io/linuxserver/code-server:latest"
client.images.pull(image_name)


def findRandomAvailablePort() -> int:
    available_ports = []
    for port in range(1024, 65535):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            if sock.connect_ex(("localhost", port)) != 0:
                available_ports.append(port)
    if not available_ports:
        raise ValueError("No available ports found")
    return random.choice(available_ports)


def SpinContainer(host_port: int):
    name = uuid4().hex
    container_port = 8443
    client.containers.run(
        image_name,
        name=name,
        environment={
            "PUID": "1000",
            "PGID": "1000",
            "TZ": "Etc/UTC",
        },
        ports={f"{container_port}/tcp": host_port},
        volumes={
            "/path/to/appdata/config": {
                "bind": "/config",
                "mode": "rw",
            }
        },
        restart_policy={"Name": "unless-stopped"},
        detach=True,
    )
    return [host_port,name]

def SpinDownContainer(containerId):
    try:
        client.containers.get(containerId).stop()
        return f"Container {containerId} stopped successfully."
    except docker.errors.NotFound:
        return f"Container {containerId} not found."
    except docker.errors.APIError as e:
        return f"Error stopping container {containerId}: {e}"

def PruneContainer(containerId):
    try:
        client.containers.get(containerId).remove()
        return f"Container {containerId} removed successfully."
    except docker.errors.NotFound:
        return f"Container {containerId} not found."
    except docker.errors.APIError as e:
        return f"Error removing container {containerId}: {e}"
    
def ForcePruneContainer(containerId):
        try:
            client.containers.get(containerId).remove(force=True)
            return f"Container {containerId} removed successfully."
        except docker.errors.NotFound:
            return f"Container {containerId} not found."
        except docker.errors.APIError as e:
            return f"Error removing container {containerId}: {e}"