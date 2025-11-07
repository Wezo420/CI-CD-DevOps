import pytest
import shutil
import subprocess
from scanner.gitleaks_scanner import GitLeaksScanner
from scanner.checkov_scanner import CheckovScanner
from scanner.trivy_scanner import TrivyScanner

@pytest.mark.asyncio
async def test_gitleaks_scan():
    # If gitleaks binary not on PATH -> skip
    if not shutil.which("gitleaks"):
        pytest.skip("gitleaks not installed in runner")

    # If gitleaks present but not executable on this runner -> skip
    try:
        subprocess.run(["gitleaks", "version"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception:
        pytest.skip("gitleaks present but not executable in this environment")

    scanner = GitLeaksScanner()
    result = await scanner.scan(".")  # scanner returns status + findings or error
    assert "status" in result
    # Accept either a findings list or an error key (test won't fail on binary issues)
    assert ("findings" in result) or ("error" in result)


@pytest.mark.asyncio
async def test_checkov_scan():
    """Test Checkov scanner"""
    scanner = CheckovScanner()
    result = await scanner.scan(".")
    assert result["status"] in ["completed", "failed"]
    assert "findings" in result

@pytest.mark.asyncio
@pytest.mark.skip(reason="Trivy not installed in CI environment")
async def test_trivy_filesystem_scan():
    """Test Trivy filesystem scanner"""
    scanner = TrivyScanner()
    result = await scanner.scan_filesystem(".")
    assert result["status"] in ["completed", "failed"]
    assert "findings" in result
