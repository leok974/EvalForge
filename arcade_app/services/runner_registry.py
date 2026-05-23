
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
                # Use evalforge-backend image (has pytest pre-installed)
                return RunnerSpec(
                    docker_image="evalforge-backend:latest",
                    file_name=entrypoint,
                    command=["python", "-u", "-I", "-B", "/workspace/.evalforge/run_unittest_json.py"]
                )
            
            return RunnerSpec(
                docker_image="python:3.12-slim",
                file_name=entrypoint,
                command=["python", "-u", "-I", "-B", entry_path]
            )
            
        elif language == "sql":
            if mode == "tests":
                return RunnerSpec(
                    docker_image="python:3.12-slim",
                    file_name="task.sql",
                    command=["python", "-u", "-I", "-B", "/workspace/.evalforge/run_unittest_json.py"]
                )
            
            # Phase 9.3: Tier 3 Postgres Support
            # Note: code_runner_docker will decide which .evalforge script to use
            return RunnerSpec(
                docker_image="evalforge-backend:latest",
                file_name="task.sql",
                command=["python", "-u", "-I", "-B", "/workspace/.evalforge/sql_preview.py"]
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

        elif language == "javascript":
            return RunnerSpec(
                docker_image="node:20-slim",
                command=["node", entry_path],
                file_name="main.js",
            )

        elif language == "docker":
            # Grade-by-inspection: no subprocess execution. RunnerSpec is a
            # no-op entry used by CI sweep scripts that enumerate languages.
            return RunnerSpec(
                docker_image="",           # no container needed
                command=[],                # no command — runner is run_docker_local()
                file_name="Dockerfile",
            )

        raise ValueError(f"Unsupported language: {language}")
