import socket
import subprocess
from typing import Dict
import dns.resolver
import yaml
from pathlib import Path
from rich.console import Console
from rich.table import Table


def ping_host(host: str) -> Dict[str, str | float]:
    """Ping a host once and return latency (ms) or error."""
    try:
        result = subprocess.run( ["ping", "-c", "1", host],
            capture_output=True, text=True, check=True,
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


def run_diagnostics():
    """Run diagnostics for all hosts in targets.yaml and print results."""
    console = Console()
    config_file = Path(__file__).parent.parent.parent / "targets.yaml"

    if not config_file.exists():
        console.print("[red]targets.yaml not found[/red]")
        return

    with open(config_file, "r") as f:
        targets = yaml.safe_load(f)

    for target in targets.get("hosts", []):
        name = target["name"]
        host = target["host"]
        console.print(f"\n[bold cyan]Diagnostics for {name} ({host})[/bold cyan]")

        # DNS lookup
        dns_result = dns_lookup(host)
        console.print(f"  [yellow]DNS:[/yellow] {dns_result}")

        # Ping
        ping_result = ping_host(host)
        console.print(f"  [yellow]Ping:[/yellow] {ping_result}")

        # TCP ports
        for port in target.get("tcp_ports", []):
            tcp_result = tcp_check(host, port)
            console.print(f"  [yellow]TCP:{port}[/yellow] {tcp_result}")


if __name__ == "__main__":
    run_diagnostics()

