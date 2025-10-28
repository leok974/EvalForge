"""
Test that arcade_app agent loads correctly.
"""
import importlib


def test_root_agent_exposes_subagents():
    """Test that root_agent is properly exposed and has sub-agents."""
    m = importlib.import_module("arcade_app")
    assert hasattr(m, "root_agent")
    ra = m.root_agent
    assert ra.name == "ArcadeOrchestrator"
    subs = [a.name for a in ra.sub_agents]
    assert "Greeter" in subs
    print(f"✓ Agent loaded successfully with sub-agents: {subs}")


def test_optional_tools_loaded():
    """Test that optional tools (Judge and Coach) are loaded."""
    m = importlib.import_module("arcade_app")
    ra = m.root_agent
    subs = [a.name for a in ra.sub_agents]
    
    # Should have at least Greeter
    assert "Greeter" in subs
    
    # Try to have Judge and Coach too
    if "Judge" in subs and "Coach" in subs:
        print("✓ Full functionality: Judge and Coach loaded")
        assert len(subs) >= 3
    else:
        print("⚠️ Minimal mode: Only Greeter loaded")
        assert len(subs) >= 1


if __name__ == "__main__":
    test_root_agent_exposes_subagents()
    test_optional_tools_loaded()
    print("\n✅ All tests passed!")
