import sys
sys.path.append("src")

from netprobe import diagnostics


def test_dns_lookup_google():
    result = diagnostics.dns_lookup("google.com")
    assert "ip" in result


def test_ping_localhost():
    result = diagnostics.ping_host("127.0.0.1")
    assert "status" in result


def test_tcp_check_closed_port():
    result = diagnostics.tcp_check("127.0.0.1", 65000)
    assert result["status"] in ["open", "closed"]
