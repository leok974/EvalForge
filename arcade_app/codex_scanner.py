"""
RepoScanner: Stage 1 of Smart Project Sync pipeline.

Scans a repository to detect:
- Core documentation files (README, ARCHITECTURE, docs/)
- Stack signals (config files indicating frameworks/tools)
- Languages (by file extensions)
- Services (from docker-compose, etc.)
- EvalForge worlds mapping
"""

from pathlib import Path
from typing import Dict, List, Set
import json

class RepoScanner:
    """Scans repository structure and content to extract metadata."""
    
    # Documentation files we look for
    CORE_DOCS = [
        "README.md", "README.rst", "README.txt",
        "ARCHITECTURE.md", "SYSTEM_DESIGN.md", "DESIGN.md",
        "docs/overview.md", "docs/architecture.md", "docs/architecture/*.md",
        "docs/api.md", "docs/infra.md", "docs/data-model.md",
        "AGENTS.md", "docs/agents.md"
    ]
    
    # File patterns that signal specific technologies
    STACK_SIGNALS = {
        "python": [
            "pyproject.toml", "requirements.txt", "requirements/*.txt",
            "setup.py", "setup.cfg", "Pipfile", "poetry.lock"
        ],
        "javascript": [
            "package.json", "package-lock.json", "yarn.lock",
            "tsconfig.json", "vite.config.ts", "vite.config.js",
            "webpack.config.js", "next.config.js"
        ],
        "frontend": [
            "package.json",  # Usually indicates frontend if has deps like react/vue
            ".eslintrc*", ".prettierrc*"
        ],
        "infra": [
            "Dockerfile", "Dockerfile.*",
            "docker-compose.yml", "docker-compose.*.yml",
            "k8s/**/*.yaml", "kubernetes/**/*.yaml",
            "terraform/**/*.tf", ".github/workflows/*.yml"
        ],
        "database": [
            "alembic.ini", "migrations/**", "prisma/schema.prisma",
            "schema.sql", "models.py", "models/**/*.py"
        ],
        "agents": [
            "agents/**", "tools/**", "prompts/**",
            "*langgraph*", "mcp_*.py", "*_agent.py"
        ]
    }
    
    # Map tech indicators to EvalForge worlds
    WORLD_MAPPING = {
        "python": "world-python",
        "javascript": "world-js",
        "typescript": "world-js",
        "database": "world-sql",
        "infra": "world-infra",
        "agents": "world-agents",
        "git": "world-git"
    }
    
    def scan(self, repo_path: str) -> Dict:
        """
        Scan repository and return comprehensive metadata.
        
        Args:
            repo_path: Absolute path to cloned repository
            
        Returns:
            Dict with keys: core_docs, stack, languages, services, worlds, frameworks
        """
        repo_root = Path(repo_path)
        
        if not repo_root.exists():
            raise ValueError(f"Repository path does not exist: {repo_path}")
        
        return {
            "core_docs": self._find_core_docs(repo_root),
            "stack": self._detect_stack(repo_root),
            "languages": self._detect_languages(repo_root),
            "services": self._detect_services(repo_root),
            "frameworks": self._detect_frameworks(repo_root),
            "worlds": self._map_to_worlds(repo_root),
        }
    
    def _find_core_docs(self, repo_root: Path) -> Dict[str, Path]:
        """Find README, ARCHITECTURE, and other documentation files."""
        found = {}
        
        for pattern in self.CORE_DOCS:
            # Handle glob patterns
            if "*" in pattern:
                matches = list(repo_root.glob(pattern))
                if matches:
                    # Take the first match
                    found[pattern] = matches[0]
            else:
                file_path = repo_root / pattern
                if file_path.exists():
                    found[pattern] = file_path
        
        return found
    
    def _detect_stack(self, repo_root: Path) -> List[str]:
        """Detect frameworks and technologies from config files."""
        stack = []
        
        for tech, patterns in self.STACK_SIGNALS.items():
            tech_detected = False
            for pattern in patterns:
                if "*" in pattern:
                    if list(repo_root.glob(pattern)):
                        tech_detected = True
                        break
                else:
                    if (repo_root / pattern).exists():
                        tech_detected = True
                        break
            
            if tech_detected:
                stack.append(tech)
        
        return stack
    
    def _detect_languages(self, repo_root: Path) -> Dict[str, int]:
        """
        Count lines of code by language.
        
        Returns:
            Dict mapping language to approximate line count
        """
        ext_map = {
            ".py": "python",
            ".ts": "typescript",
            ".tsx": "typescript",
            ".js": "javascript",
            ".jsx": "javascript",
            ".go": "go",
            ".rs": "rust",
            ".java": "java",
            ".rb": "ruby",
            ".php": "php"
        }
        
        language_lines = {}
        
        # Skip common non-code directories
        skip_dirs = {".git", "node_modules", "__pycache__", "venv", ".venv", "dist", "build"}
        
        for ext, lang in ext_map.items():
            total_lines = 0
            for file_path in repo_root.rglob(f"*{ext}"):
                # Skip if in excluded directory
                if any(skip in file_path.parts for skip in skip_dirs):
                    continue
                
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        total_lines += sum(1 for _ in f)
                except Exception:
                    # Skip files that can't be read
                    continue
            
            if total_lines > 0:
                language_lines[lang] = total_lines
        
        return language_lines
    
    def _detect_services(self, repo_root: Path) -> List[Dict[str, str]]:
        """
        Detect services from docker-compose files.
        
        Returns:
            List of dicts with service name and type
        """
        services = []
        
        # Look for docker-compose files
        compose_files = list(repo_root.glob("docker-compose*.yml")) + \
                       list(repo_root.glob("docker-compose*.yaml"))
        
        for compose_file in compose_files:
            try:
                import yaml
                with open(compose_file, 'r') as f:
                    compose_data = yaml.safe_load(f)
                
                if compose_data and "services" in compose_data:
                    for service_name, service_config in compose_data["services"].items():
                        service_type = self._infer_service_type(service_name, service_config)
                        services.append({
                            "name": service_name,
                            "type": service_type
                        })
            except Exception as e:
                # Skip files that can't be parsed
                print(f"Could not parse {compose_file}: {e}")
                continue
        
        return services
    
    def _infer_service_type(self, name: str, config: Dict) -> str:
        """Infer service type from name and configuration."""
        name_lower = name.lower()
        
        # Check image name
        image = config.get("image", "").lower()
        
        if "postgres" in image or "postgres" in name_lower:
            return "database"
        elif "redis" in image or "redis" in name_lower:
            return "cache"
        elif "nginx" in image or "nginx" in name_lower:
            return "proxy"
        elif "elasticsearch" in image or "elastic" in name_lower:
            return "search"
        elif any(word in name_lower for word in ["api", "backend", "server"]):
            return "backend"
        elif any(word in name_lower for word in ["web", "frontend", "ui"]):
            return "frontend"
        elif "worker" in name_lower or "celery" in name_lower:
            return "worker"
        else:
            return "service"
    
    def _detect_frameworks(self, repo_root: Path) -> Dict[str, List[str]]:
        """Detect specific frameworks from package files."""
        frameworks = {
            "backend": [],
            "frontend": [],
            "infra": [],
            "testing": []
        }
        
        # Check Python frameworks
        if (repo_root / "pyproject.toml").exists():
            try:
                # Try Python 3.11+ tomllib first, fallback to tomli
                try:
                    import tomllib
                except ImportError:
                    try:
                        import tomli as tomllib
                    except ImportError:
                        tomllib = None
                
                if tomllib:
                    with open(repo_root / "pyproject.toml", "rb") as f:
                        pyproject = tomllib.load(f)
                    
                    deps = []
                    if "project" in pyproject and "dependencies" in pyproject["project"]:
                        deps.extend(pyproject["project"]["dependencies"])
                    if "tool" in pyproject and "poetry" in pyproject["tool"]:
                        if "dependencies" in pyproject["tool"]["poetry"]:
                            deps.extend(pyproject["tool"]["poetry"]["dependencies"].keys())
                    
                    for dep in deps:
                        dep_lower = str(dep).lower()
                        if "fastapi" in dep_lower:
                            frameworks["backend"].append("FastAPI")
                        elif "flask" in dep_lower:
                            frameworks["backend"].append("Flask")
                        elif "django" in dep_lower:
                            frameworks["backend"].append("Django")
                        elif "sqlalchemy" in dep_lower or "sqlmodel" in dep_lower:
                            frameworks["backend"].append("SQLAlchemy")
            except Exception:
                pass
        
        # Check Node.js frameworks
        if (repo_root / "package.json").exists():
            try:
                with open(repo_root / "package.json", "r") as f:
                    package = json.load(f)
                
                deps = {**(package.get("dependencies", {})), **(package.get("devDependencies", {}))}
                
                if "react" in deps:
                    frameworks["frontend"].append("React")
                if "vue" in deps:
                    frameworks["frontend"].append("Vue")
                if "next" in deps:
                    frameworks["frontend"].append("Next.js")
                if "vite" in deps:
                    frameworks["frontend"].append("Vite")
                if "tailwindcss" in deps:
                    frameworks["frontend"].append("Tailwind")
            except Exception:
                pass
        
        return {k: v for k, v in frameworks.items() if v}
    
    def _map_to_worlds(self, repo_root: Path) -> List[str]:
        """Map detected stack to EvalForge worlds."""
        stack = self._detect_stack(repo_root)
        languages = self._detect_languages(repo_root)
        
        worlds = set()
        
        # Add worlds based on stack
        for tech in stack:
            if tech in self.WORLD_MAPPING:
                worlds.add(self.WORLD_MAPPING[tech])
        
        # Add worlds based on primary languages
        for lang in languages.keys():
            if lang in self.WORLD_MAPPING:
                worlds.add(self.WORLD_MAPPING[lang])
        
        # Always add git world for any repo
        worlds.add("world-git")
        
        return sorted(list(worlds))
