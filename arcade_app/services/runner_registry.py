
from dataclasses import dataclass, field
from typing import Dict, List, Optional

@dataclass
class RunnerSpec:
    docker_image: str
    command: List[str]
    file_name: str
    env: Dict[str, str] = field(default_factory=dict)

class RunnerRegistry:
    @staticmethod
    def get_runner(language: str, mode: str = "run", entrypoint: str = "main.py") -> RunnerSpec:
        
        # Determine paths
        entry_path = f"/workspace/{entrypoint}"
        
        if language == "python":
            if mode == "tests":
                # We expect the runner to inject run_unittest_json.py
                return RunnerSpec(
                    docker_image="python:3.12-slim",
                    file_name=entrypoint,
                    command=["python", "-u", "-I", "-B", "/workspace/.evalforge/run_unittest_json.py"]
                )
            
            return RunnerSpec(
                docker_image="python:3.12-slim",
                file_name=entrypoint,
                command=["python", "-u", "-I", "-B", entry_path]
            )
            
        elif language == "typescript":
            if mode == "tests":
                return RunnerSpec(
                    docker_image="oven/bun:1",
                    file_name="main.ts", # Not strictly used for test cmd
                    command=["bun", "test"]
                )

            return RunnerSpec(
                docker_image="oven/bun:1",
                file_name=entrypoint,
                command=["bun", "run", entry_path]
            )
            
        raise ValueError(f"Unsupported language: {language}")
