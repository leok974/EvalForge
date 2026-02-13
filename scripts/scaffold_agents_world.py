from __future__ import annotations
from pathlib import Path
import textwrap

ROOT = Path(__file__).resolve().parents[1]
QROOT = ROOT / "data" / "quests"

def w(path: Path, content: str) -> None:
  path.parent.mkdir(parents=True, exist_ok=True)
  path.write_text(content.rstrip() + "\n", encoding="utf-8")

def quest(slug: str, readme: str, starter_main: str, sol_main: str, test_py: str) -> None:
  base = QROOT / slug
  w(base / "workspace" / "README.md", readme)
  w(base / "workspace" / "main.py", starter_main)
  w(base / "grading" / "solutions" / "main.py", sol_main)
  w(base / "grading" / "public" / "test_public.py", test_py)

COMMON_TEST_HEADER = r"""
import sys
from pathlib import Path

QUEST = Path(__file__).resolve().parents[2]
WS = QUEST / "workspace"
sys.path.insert(0, str(WS))

import main  # noqa
""".lstrip()

def main() -> int:
  # 1) agents-ignition
  quest(
    "agents-ignition",
    "# Agents Ignition\n\nImplement `format_prompt(system, user)`.\n\nRules:\n- Trim `system`\n- Normalize `user` by trimming and collapsing internal whitespace to single spaces\n- Return:\n  SYSTEM: <system>\\nUSER: <user>\n",
    textwrap.dedent("""
    def format_prompt(system: str, user: str) -> str:
        raise NotImplementedError
    """),
    textwrap.dedent("""
    def _collapse_ws(s: str) -> str:
        return " ".join(s.strip().split())

    def format_prompt(system: str, user: str) -> str:
        system = system.strip()
        user = _collapse_ws(user)
        return f"SYSTEM: {system}\\nUSER: {user}"
    """),
    COMMON_TEST_HEADER + textwrap.dedent("""
    def test_format_prompt_normalizes():
        out = main.format_prompt("  You are helpful.  ", "  hello    there   ")
        assert out == "SYSTEM: You are helpful.\\nUSER: hello there"
    """)
  )

  # 2) agents-prompts-contracts
  quest(
    "agents-prompts-contracts",
    "# Prompt Contracts\n\nImplement `validate_prompt_contract(contract)` returning a list of error strings.\n\nContract must contain:\n- system: non-empty str\n- user: non-empty str\n- tools: list[str]\n- max_tokens: int > 0\nReturn [] if valid.\n",
    textwrap.dedent("""
    def validate_prompt_contract(contract: dict) -> list[str]:
        raise NotImplementedError
    """),
    textwrap.dedent("""
    def validate_prompt_contract(contract: dict) -> list[str]:
        errors: list[str] = []
        if not isinstance(contract, dict):
            return ["contract_not_dict"]

        def need_str(k: str):
            v = contract.get(k)
            if not isinstance(v, str) or not v.strip():
                errors.append(f"{k}_invalid")

        need_str("system")
        need_str("user")

        tools = contract.get("tools")
        if not isinstance(tools, list) or not all(isinstance(t, str) for t in tools):
            errors.append("tools_invalid")

        mt = contract.get("max_tokens")
        if not isinstance(mt, int) or mt <= 0:
            errors.append("max_tokens_invalid")

        return errors
    """),
    COMMON_TEST_HEADER + textwrap.dedent("""
    def test_valid_contract_ok():
        c = {"system":"s","user":"u","tools":["add"],"max_tokens":128}
        assert main.validate_prompt_contract(c) == []

    def test_invalid_contract_errors():
        c = {"system":"", "user": 123, "tools":"x", "max_tokens":0}
        errs = main.validate_prompt_contract(c)
        assert "system_invalid" in errs
        assert "user_invalid" in errs
        assert "tools_invalid" in errs
        assert "max_tokens_invalid" in errs
    """)
  )

  # 3) agents-tools-basics
  quest(
    "agents-tools-basics",
    "# Tools Basics\n\nImplement ToolContract + ToolRegistry.\n\n- ToolContract(name, input_keys, fn)\n- ToolRegistry.register(tool)\n- ToolRegistry.call(name, **kwargs)\n  - validates name exists\n  - validates kwargs keys match tool.input_keys exactly\n",
    textwrap.dedent("""
    from dataclasses import dataclass
    from typing import Callable

    @dataclass(frozen=True)
    class ToolContract:
        name: str
        input_keys: tuple[str, ...]
        fn: Callable[..., object]

    class ToolRegistry:
        def __init__(self):
            raise NotImplementedError

        def register(self, tool: ToolContract) -> None:
            raise NotImplementedError

        def call(self, name: str, **kwargs):
            raise NotImplementedError
    """),
    textwrap.dedent("""
    from dataclasses import dataclass
    from typing import Callable, Dict

    @dataclass(frozen=True)
    class ToolContract:
        name: str
        input_keys: tuple[str, ...]
        fn: Callable[..., object]

    class ToolRegistry:
        def __init__(self):
            self._tools: Dict[str, ToolContract] = {}

        def register(self, tool: ToolContract) -> None:
            self._tools[tool.name] = tool

        def call(self, name: str, **kwargs):
            if name not in self._tools:
                raise KeyError(name)
            tool = self._tools[name]
            if set(kwargs.keys()) != set(tool.input_keys):
                raise ValueError("BAD_ARGS")
            return tool.fn(**kwargs)
    """),
    COMMON_TEST_HEADER + textwrap.dedent("""
    def test_registry_call_and_arg_validation():
        reg = main.ToolRegistry()
        reg.register(main.ToolContract("add", ("a","b"), lambda a,b: a+b))
        assert reg.call("add", a=2, b=3) == 5

        try:
            reg.call("add", a=2)
            assert False, "expected ValueError"
        except ValueError as e:
            assert str(e) == "BAD_ARGS"

        try:
            reg.call("missing", x=1)
            assert False, "expected KeyError"
        except KeyError:
            pass
    """)
  )

  # 4) agents-planner
  quest(
    "agents-planner",
    "# Planner\n\nImplement `plan(request, tool_names)`.\n\nSupported request forms:\n- \"add <a> <b>\" -> tool \"add\" args {a:int,b:int}\n- \"echo <text...>\" -> tool \"echo\" args {text:str}\nRaises ValueError(\"NO_TOOL\") if required tool missing.\n",
    textwrap.dedent("""
    def plan(request: str, tool_names: list[str]) -> list[dict]:
        raise NotImplementedError
    """),
    textwrap.dedent("""
    def plan(request: str, tool_names: list[str]) -> list[dict]:
        parts = request.strip().split()
        if not parts:
            return []
        cmd = parts[0].lower()

        if cmd == "add":
            if "add" not in tool_names:
                raise ValueError("NO_TOOL")
            a = int(parts[1]); b = int(parts[2])
            return [{"tool":"add", "args":{"a":a, "b":b}}]

        if cmd == "echo":
            if "echo" not in tool_names:
                raise ValueError("NO_TOOL")
            text = " ".join(parts[1:])
            return [{"tool":"echo", "args":{"text":text}}]

        return []
    """),
    COMMON_TEST_HEADER + textwrap.dedent("""
    def test_plan_add():
        p = main.plan("add 2 3", ["add", "echo"])
        assert p == [{"tool":"add","args":{"a":2,"b":3}}]

    def test_plan_missing_tool():
        try:
            main.plan("add 1 2", ["echo"])
            assert False
        except ValueError as e:
            assert str(e) == "NO_TOOL"
    """)
  )

  # 5) agents-executor
  quest(
    "agents-executor",
    "# Executor\n\nImplement `execute(plan, registry)`.\n\n- Executes steps in order\n- Returns {\"results\": [ {\"tool\":name, \"output\": value}, ... ] }\n",
    textwrap.dedent("""
    def execute(plan: list[dict], registry) -> dict:
        raise NotImplementedError
    """),
    textwrap.dedent("""
    def execute(plan: list[dict], registry) -> dict:
        results = []
        for step in plan:
            name = step["tool"]
            args = step.get("args", {})
            out = registry.call(name, **args)
            results.append({"tool": name, "output": out})
        return {"results": results}
    """),
    COMMON_TEST_HEADER + textwrap.dedent("""
    def test_execute_runs_steps():
        # Minimal mock for ToolRegistry
        class ToolContract:
            def __init__(self, name, input_keys, fn):
                self.name = name
                self.input_keys = input_keys
                self.fn = fn
        
        class ToolRegistry:
            def __init__(self):
                self._tools = {}
            def register(self, tool):
                self._tools[tool.name] = tool
            def call(self, name, **kwargs):
                return self._tools[name].fn(**kwargs)

        reg = ToolRegistry()
        reg.register(ToolContract("add", ("a","b"), lambda a,b: a+b))
        plan = [{"tool":"add","args":{"a":2,"b":3}}, {"tool":"add","args":{"a":3,"b":4}}]
        out = main.execute(plan, reg)
        assert out["results"][0]["output"] == 5
        assert out["results"][1]["output"] == 7
    """)
  )

  # 6) agents-verifier
  quest(
    "agents-verifier",
    "# Verifier\n\nImplement `verify_output(output, required_keys)`.\n\nReturns {ok: bool, missing: list[str]}.\n",
    textwrap.dedent("""
    def verify_output(output: dict, required_keys: list[str]) -> dict:
        raise NotImplementedError
    """),
    textwrap.dedent("""
    def verify_output(output: dict, required_keys: list[str]) -> dict:
        missing = [k for k in required_keys if k not in output]
        return {"ok": len(missing) == 0, "missing": missing}
    """),
    COMMON_TEST_HEADER + textwrap.dedent("""
    def test_verify_output():
        out = main.verify_output({"a":1}, ["a","b"])
        assert out["ok"] is False
        assert out["missing"] == ["b"]

        out2 = main.verify_output({"a":1,"b":2}, ["a","b"])
        assert out2["ok"] is True
        assert out2["missing"] == []
    """)
  )

  # 7) agents-approvals-diffs
  quest(
    "agents-approvals-diffs",
    "# Approvals + Diffs\n\nImplement `apply_diff(base, diff, approved)`.\n\nDiff is a list of edits: {start:int, end:int, text:str}\n- start/end are indices into base (end exclusive)\n- apply edits in order\n- if approved is False: raise PermissionError\n",
    textwrap.dedent("""
    def apply_diff(base: str, diff: list[dict], approved: bool) -> str:
        raise NotImplementedError
    """),
    textwrap.dedent("""
    def apply_diff(base: str, diff: list[dict], approved: bool) -> str:
        if not approved:
            raise PermissionError("NOT_APPROVED")
        s = base
        offset = 0
        for e in diff:
            start = int(e["start"]) + offset
            end = int(e["end"]) + offset
            text = str(e["text"])
            s = s[:start] + text + s[end:]
            offset += len(text) - (end - start)
        return s
    """),
    COMMON_TEST_HEADER + textwrap.dedent("""
    def test_apply_diff_requires_approval():
        try:
            main.apply_diff("hello", [{"start":0,"end":5,"text":"hi"}], approved=False)
            assert False
        except PermissionError as e:
            assert str(e) == "NOT_APPROVED"

    def test_apply_diff_replaces_range():
        out = main.apply_diff("hello world", [{"start":6,"end":11,"text":"agent"}], approved=True)
        assert out == "hello agent"
    """)
  )

  # 8) agents-memory
  quest(
    "agents-memory",
    "# Memory\n\nImplement WorkingMemory with:\n- remember(key,value)\n- recall(key, default=None)\n- forget(key)\n- keys(prefix='') -> sorted list\n",
    textwrap.dedent("""
    class WorkingMemory:
        def __init__(self):
            raise NotImplementedError

        def remember(self, key: str, value: str) -> None:
            raise NotImplementedError

        def recall(self, key: str, default=None):
            raise NotImplementedError

        def forget(self, key: str) -> None:
            raise NotImplementedError

        def keys(self, prefix: str = "") -> list[str]:
            raise NotImplementedError
    """),
    textwrap.dedent("""
    class WorkingMemory:
        def __init__(self):
            self._m: dict[str, str] = {}

        def remember(self, key: str, value: str) -> None:
            self._m[key] = value

        def recall(self, key: str, default=None):
            return self._m.get(key, default)

        def forget(self, key: str) -> None:
            self._m.pop(key, None)

        def keys(self, prefix: str = "") -> list[str]:
            out = [k for k in self._m.keys() if k.startswith(prefix)]
            return sorted(out)
    """),
    COMMON_TEST_HEADER + textwrap.dedent("""
    def test_working_memory():
        mem = main.WorkingMemory()
        mem.remember("user:name", "leo")
        mem.remember("user:role", "mle")
        assert mem.recall("user:name") == "leo"
        assert mem.keys("user:") == ["user:name", "user:role"]
        mem.forget("user:role")
        assert mem.recall("user:role", "none") == "none"
    """)
  )

  # 9) agents-budgets
  quest(
    "agents-budgets",
    "# Budgets\n\nImplement BudgetGuardrail(max_tool_calls, max_cost).\n\n- charge_tool(cost): increments tool_calls and cost\n- raises BudgetExceeded when either limit exceeded\n",
    textwrap.dedent("""
    class BudgetExceeded(Exception):
        pass

    class BudgetGuardrail:
        def __init__(self, max_tool_calls: int, max_cost: int):
            raise NotImplementedError

        def charge_tool(self, cost: int) -> None:
            raise NotImplementedError

        @property
        def tool_calls(self) -> int:
            raise NotImplementedError

        @property
        def cost(self) -> int:
            raise NotImplementedError
    """),
    textwrap.dedent("""
    class BudgetExceeded(Exception):
        pass

    class BudgetGuardrail:
        def __init__(self, max_tool_calls: int, max_cost: int):
            self._max_calls = int(max_tool_calls)
            self._max_cost = int(max_cost)
            self._calls = 0
            self._cost = 0

        def charge_tool(self, cost: int) -> None:
            self._calls += 1
            self._cost += int(cost)
            if self._calls > self._max_calls or self._cost > self._max_cost:
                raise BudgetExceeded("BUDGET_EXCEEDED")

        @property
        def tool_calls(self) -> int:
            return self._calls

        @property
        def cost(self) -> int:
            return self._cost
    """),
    COMMON_TEST_HEADER + textwrap.dedent("""
    def test_budget_guardrail_limits():
        b = main.BudgetGuardrail(max_tool_calls=2, max_cost=5)
        b.charge_tool(3)
        assert b.tool_calls == 1 and b.cost == 3

        try:
            b.charge_tool(3)  # cost becomes 6 -> exceeds
            assert False
        except main.BudgetExceeded as e:
            assert str(e) == "BUDGET_EXCEEDED"
    """)
  )

  # 10) agents-observability
  quest(
    "agents-observability",
    "# Observability\n\nImplement AuditLog.\n\n- event(name, **fields) appends {name, ...fields, seq}\n- span(name) context manager emits span_start / span_end with same span_id\n- to_json() returns the list\nNo real time; use a deterministic sequence counter.\n",
    textwrap.dedent("""
    class AuditLog:
        def __init__(self):
            raise NotImplementedError

        def event(self, name: str, **fields) -> None:
            raise NotImplementedError

        def span(self, name: str):
            raise NotImplementedError

        def to_json(self) -> list[dict]:
            raise NotImplementedError
    """),
    textwrap.dedent("""
    import contextlib

    class AuditLog:
        def __init__(self):
            self._events: list[dict] = []
            self._seq = 0
            self._span_seq = 0

        def event(self, name: str, **fields) -> None:
            self._seq += 1
            e = {"name": name, "seq": self._seq}
            e.update(fields)
            self._events.append(e)

        @contextlib.contextmanager
        def span(self, name: str):
            self._span_seq += 1
            span_id = f"sp{self._span_seq}"
            self.event("span_start", span=name, span_id=span_id)
            try:
                yield span_id
            finally:
                self.event("span_end", span=name, span_id=span_id)

        def to_json(self) -> list[dict]:
            return list(self._events)
    """),
    COMMON_TEST_HEADER + textwrap.dedent("""
    def test_auditlog_span_order_and_id():
        log = main.AuditLog()
        with log.span("exec") as sid:
            log.event("tool_call", tool="add")

        events = log.to_json()
        assert events[0]["name"] == "span_start"
        assert events[1]["name"] == "tool_call"
        assert events[2]["name"] == "span_end"
        assert events[0]["span_id"] == sid
        assert events[2]["span_id"] == sid
    """)
  )

  print("[OK] scaffolded agents world (10 quests)")
  return 0

if __name__ == "__main__":
  raise SystemExit(main())
