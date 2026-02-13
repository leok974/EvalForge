import pytest
import importlib.util

def test_variable_energy():
    spec = importlib.util.spec_from_file_location("main", "main.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    
    assert hasattr(module, "energy"), "Variable 'energy' not found"
    assert module.energy == 100, f"Expected energy to be 100, but got {module.energy}"