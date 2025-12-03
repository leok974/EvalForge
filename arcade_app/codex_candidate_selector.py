"""
CandidateSelector: Stage 2 of Smart Project Sync pipeline.

Selects relevant files and snippets to feed into LLM for each doc_type.
"""

from pathlib import Path
from typing import Dict, List
import re

class CandidateSelector:
    """Selects file candidates for each Project Codex doc_type."""
    
    # Map doc_type to file patterns
    DOC_TYPE_PATTERNS = {
        "overview": [
            "README.md", "README.rst", "README.txt",
            ".github/README.md"
        ],
        "architecture": [
            "ARCHITECTURE.md", "SYSTEM_DESIGN.md", "DESIGN.md",
            "docs/architecture.md", "docs/architecture/*.md",
            "docs/system-design.md",
            "docker-compose.yml", "docker-compose.prod.yml",
            "docs/overview.md"
        ],
        "data_model": [
            "schema.sql", "prisma/schema.prisma",
            "models.py", "models/**/*.py",
            "migrations/**/*.sql", "alembic/versions/*.py",
            "docs/data-model.md", "docs/database.md", "docs/schema.md"
        ],
        "infra": [
            "Dockerfile", "Dockerfile.*",
            "docker-compose.yml", "docker-compose.*.yml",
            "k8s/**/*.yaml", "kubernetes/**/*.yaml",
            "terraform/**/*.tf",
            ".github/workflows/*.yml",
            "docs/deployment.md", "docs/infra.md", "DEPLOYMENT.md"
        ],
        "observability": [
            "docs/monitoring.md", "docs/observability.md",
            "docs/logging.md", "docs/metrics.md",
            "prometheus.yml", "grafana/**/*.json"
        ],
        "agents": [
            "AGENTS.md", "docs/agents.md",
            "agents/**/*.py", "tools/**/*.py",
            "prompts/**/*",
            "*_agent.py", "*_tool.py"
        ],
        "quest_hooks": [
            "TODO.md", "TODO", "ROADMAP.md",
            "CONTRIBUTING.md",
            ".github/ISSUE_TEMPLATE/*.md",
            "docs/roadmap.md"
        ]
    }
    
    def select_candidates(self, repo_path: str, doc_type: str, scan_results: Dict) -> List[Dict]:
        """
        Select file candidates for a specific doc_type.
        
        Args:
            repo_path: Path to repository
            doc_type: Type of doc to generate (overview, architecture, etc.)
            scan_results: Results from RepoScanner.scan()
            
        Returns:
            List of dicts with 'path', 'snippet', 'relevance_score'
        """
        repo_root = Path(repo_path)
        candidates = []
        
        # Get patterns for this doc_type
        patterns = self.DOC_TYPE_PATTERNS.get(doc_type, [])
        
        for pattern in patterns:
            files = self._find_files(repo_root, pattern)
            for file_path in files:
                snippet = self._extract_snippet(file_path, doc_type)
                if snippet:
                    candidates.append({
                        "path": str(file_path.relative_to(repo_root)),
                        "snippet": snippet,
                        "relevance_score": self._calculate_relevance(file_path, doc_type, scan_results)
                    })
        
        # Sort by relevance and return top candidates
        candidates.sort(key=lambda x: x["relevance_score"], reverse=True)
        
        # Limit to top 5 most relevant files to avoid token limits
        return candidates[:5]
    
    def _find_files(self, repo_root: Path, pattern: str) -> List[Path]:
        """Find files matching a pattern."""
        if "*" in pattern:
            return list(repo_root.glob(pattern))
        else:
            file_path = repo_root / pattern
            return [file_path] if file_path.exists() else []
    
    def _extract_snippet(self, file_path: Path, doc_type: str, max_lines: int = 200) -> str:
        """
        Extract relevant snippet from a file.
        
        For most files, return the first N lines.
        For code files, apply smarter extraction.
        """
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            lines = content.split('\n')
            
            # For markdown/text files, take more content
            if file_path.suffix in ['.md', '.txt', '.rst']:
                return '\n'.join(lines[:max_lines])
            
            # For YAML/JSON config files
            elif file_path.suffix in ['.yml', '.yaml', '.json']:
                return '\n'.join(lines[:100])  # Configs are usually structured
            
            # For SQL files
            elif file_path.suffix == '.sql':
                return '\n'.join(lines[:150])
            
            # For Python/TS code files - extract docstrings and class/function signatures
            elif file_path.suffix in ['.py', '.ts', '.js']:
                return self._extract_code_structure(content, file_path.suffix)
            
            else:
                return '\n'.join(lines[:100])
                
        except Exception as e:
            print(f"Failed to extract snippet from {file_path}: {e}")
            return ""
    
    def _extract_code_structure(self, content: str, extension: str) -> str:
        """Extract high-level structure from code files (classes, functions, docstrings)."""
        lines = content.split('\n')
        
        if extension == '.py':
            # Extract classes, functions, and their docstrings
            structure_lines = []
            in_docstring = False
            indent_level = 0
            
            for line in lines[:300]:  # Limit to first 300 lines
                stripped = line.strip()
                
                # Class or function definition
                if stripped.startswith('class ') or stripped.startswith('def ') or stripped.startswith('async def '):
                    structure_lines.append(line)
                    indent_level = len(line) - len(line.lstrip())
                
                # Docstring
                elif '"""' in stripped or "'''" in stripped:
                    if not in_docstring:
                        in_docstring = True
                        structure_lines.append(line)
                    else:
                        structure_lines.append(line)
                        in_docstring = False
                elif in_docstring:
                    structure_lines.append(line)
            
            return '\n'.join(structure_lines) if structure_lines else '\n'.join(lines[:100])
        
        else:
            # For TS/JS, just return first portion
            return '\n'.join(lines[:100])
    
    def _calculate_relevance(self, file_path: Path, doc_type: str, scan_results: Dict) -> float:
        """
        Calculate relevance score for a file based on doc_type.
        
        Higher score = more relevant.
        """
        score = 0.0
        filename = file_path.name.lower()
        
        # Base scores by file type
        if doc_type in filename:
            score += 10.0  # E.g., architecture.md for doc_type=architecture
        
        if filename.startswith("readme"):
            score += 8.0 if doc_type == "overview" else 2.0
        
        if "architecture" in filename or "design" in filename:
            score += 8.0 if doc_type == "architecture" else 1.0
        
        if "docker-compose" in filename:
            score += 7.0 if doc_type in ["architecture", "infra"] else 1.0
        
        if "schema" in filename or "model" in filename:
            score += 7.0 if doc_type == "data_model" else 1.0
        
        if "agent" in filename or "tool" in filename:
            score += 7.0 if doc_type == "agents" else 0.5
        
        # Markdown files are generally more valuable for LLM input
        if file_path.suffix == '.md':
            score += 3.0
        
        # Penalize very large files (likely to be noisy)
        try:
            size_kb = file_path.stat().st_size / 1024
            if size_kb > 100:
                score -= 2.0
            if size_kb > 500:
                score -= 5.0
        except:
            pass
        
        return max(score, 0.0)
