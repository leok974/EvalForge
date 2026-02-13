import pytest
from workspace.task import ignite

def test_ignition():
    assert ignite() == "READY", "Ignition failed: expected 'READY'"