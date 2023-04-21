# tests/unit/test_axe_scan.py
import pytest
from app.main import axe_scan


def test_axe_scan():
    # Test a URL with known accessibility issues
    url = 'https://example.com/accessibility-issues'
    results = axe_scan(url)
    assert 'violations' in results
    assert len(results['violations']) > 0

    # Test a URL with no accessibility issues
    url = 'https://example.com/no-accessibility-issues'
    results = axe_scan(url)
    assert 'violations' not in results