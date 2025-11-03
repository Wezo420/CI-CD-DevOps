import pytest
from scanner.gitleaks_scanner import GitLeaksScanner
from scanner.checkov_scanner import CheckovScanner
from scanner.trivy_scanner import TrivyScanner

@pytest.mark.asyncio
async def test_gitleaks_scan():
    """Test Gitleaks scanner"""
    scanner = GitLeaksScanner()
    result = await scanner.scan(".")
    assert result["status"] in ["completed", "failed"]
    assert "findings" in result

@pytest.mark.asyncio
async def test_checkov_scan():
    """Test Checkov scanner"""
    scanner = CheckovScanner()
    result = await scanner.scan(".")
    assert result["status"] in ["completed", "failed"]
    assert "findings" in result

@pytest.mark.asyncio
async def test_trivy_filesystem_scan():
    """Test Trivy filesystem scanner"""
    scanner = TrivyScanner()
    result = await scanner.scan_filesystem(".")
    assert result["status"] in ["completed", "failed"]
    assert "findings" in result
