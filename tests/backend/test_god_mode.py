import os
import pytest
from arcade_app import config

def test_dev_unlock_all_enabled(monkeypatch):
    # Case 1: Dev env, Flag True -> True
    monkeypatch.setenv("EVALFORGE_ENVIRONMENT", "dev")
    monkeypatch.setenv("EVALFORGE_DEV_UNLOCK_ALL_FEATURES", "true")
    # Reload config to pick up env vars
    from importlib import reload
    reload(config)
    assert config.dev_unlock_all_enabled() is True

    # Case 2: Prod env, Flag True -> False (Safety Rail)
    monkeypatch.setenv("EVALFORGE_ENVIRONMENT", "prod")
    monkeypatch.setenv("EVALFORGE_DEV_UNLOCK_ALL_FEATURES", "true")
    reload(config)
    assert config.dev_unlock_all_enabled() is False

    # Case 3: Dev env, Flag False -> False
    monkeypatch.setenv("EVALFORGE_ENVIRONMENT", "dev")
    monkeypatch.setenv("EVALFORGE_DEV_UNLOCK_ALL_FEATURES", "false")
    reload(config)
    assert config.dev_unlock_all_enabled() is False
