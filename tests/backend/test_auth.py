import os
from arcade_app import auth_helper

def test_mock_auth_default():
    # Ensure default is mock
    os.environ["EVALFORGE_AUTH_MODE"] = "mock"
    user = auth_helper.get_current_user()
    assert user["id"] == "leo"
    assert user["auth_mode"] == "mock"

def test_real_auth_empty():
    # Ensure non-mock returns empty dict (simulating logged out)
    os.environ["EVALFORGE_AUTH_MODE"] = "github"
    user = auth_helper.get_current_user()
    assert user == {}
    # Reset for other tests
    os.environ["EVALFORGE_AUTH_MODE"] = "mock"
