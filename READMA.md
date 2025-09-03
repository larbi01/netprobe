# NetProbe 🛰️

A simple yet practical **network diagnostic tool** written in **Python**.  
It demonstrates **networking fundamentals** (ping, DNS, TCP connectivity) and good software practices (tests, CI, documentation).  

---

## 🌍 Features
- ✅ **Ping hosts** and measure latency (ICMP)
- ✅ **DNS lookups** (resolve hostnames to IPs)
- ✅ **TCP connectivity checks** (open/closed ports)
- ✅ Configurable targets in `targets.yaml`
- ✅ CLI interface with `typer`
- ✅ Tests + GitHub Actions CI

---

## ⚡ Quick Start (English)

### Clone the repo
git clone git@github.com:larbi01/netprobe.git
cd netprobe

### Setup environment

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

### Run diagnostics

python -m netprobe.diagnostics

### Or run tests:

pytest -v

### Example targets (targets.yaml)

hosts:
  - name: Localhost
    host: 127.0.0.1
    tcp_ports: [22, 8000]
  - name: Google
    host: google.com
    tcp_ports: [80, 443]

## 🧪 Tech Stack

Python 3.10+
Typer -> CLI
dnspython -> DNS lookups
ping3 -> ICMP
pytest -> Tests

## 👤 Author

Larbi Ouadeih
