import socket
import subprocess
from typing import Dict
import dns.resolver


def ping_host(host: str) -> Dict[str, str | float]:
    """Ping a host once and return latency (ms) or error."""
    try:
        result = subprocess.run(
            ["ping", "-c", "1", host],
            capture_output=True,
            text=True,
            check=True,
        )
        for line in result.stdout.split("\n"):
            if "time=" in line:
                latency = float(line.split("time=")[1].split()[0])
                return {"host": host, "status": "reachable", "latency_ms": latency}
        return {"host": host, "status": "unknown"}
    except Exception as e:
        return {"host": host, "status": "unreachable", "error": str(e)}


def dns_lookup(host: str) -> Dict[str, str]:
    """Resolve DNS for a hostname."""
    try:
        answers = dns.resolver.resolve(host, "A")
        return {"host": host, "ip": answers[0].to_text()}
    except Exception as e:
        return {"host": host, "error": str(e)}


def tcp_check(host: str, port: int, timeout: int = 3) -> Dict[str, str | int]:
    """Check TCP connectivity."""
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return {"host": host, "port": port, "status": "open"}
    except Exception as e:
        return {"host": host, "port": port, "status": "closed", "error": str(e)}

