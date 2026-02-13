
def execute(plan: list[dict], registry) -> dict:
    results = []
    for step in plan:
        name = step["tool"]
        args = step.get("args", {})
        out = registry.call(name, **args)
        results.append({"tool": name, "output": out})
    return {"results": results}
