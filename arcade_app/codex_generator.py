"""
CodexDocGenerator: Stage 3 of Smart Project Sync pipeline.

Uses LLM (Vertex AI) to generate structured Project Codex documentation
from repository file snippets and metadata.
"""

import os
import yaml
from typing import Dict, Optional
from arcade_app.codex_prompts import SYSTEM_PROMPT, get_prompt_for_doc_type

class CodexDocGenerator:
    """Generates Project Codex documentation using LLM."""
    
    def __init__(self):
        """Initialize with Vertex AI configuration."""
        self.project_id = os.getenv("GOOGLE_CLOUD_PROJECT", "")
        self.location = os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1")
        self.model_version = os.getenv("EVALFORGE_MODEL_VERSION", "gemini-1.5-flash")
        
        # Lazy import to avoid dependency issues
        self._model = None
    
    def _get_model(self):
        """Lazy load Vertex AI model."""
        if self._model is None:
            try:
                import vertexai
                from vertexai.generative_models import GenerativeModel
                
                vertexai.init(project=self.project_id, location=self.location)
                self._model = GenerativeModel(self.model_version)
            except Exception as e:
                print(f"Warning: Could not initialize Vertex AI: {e}")
                self._model = None
        
        return self._model
    
    async def generate_doc(
        self,
        project_slug: str,
        doc_type: str,
        file_snippets: list[Dict],
        scan_meta: Dict
    ) -> Dict:
        """
        Generate a complete Project Codex document.
        
        Args:
            project_slug: Project identifier (e.g., "applylens")
            doc_type: Type of doc (overview, architecture, etc.)
            file_snippets: List of dicts from CandidateSelector with 'path' and 'snippet'
            scan_meta: Metadata from RepoScanner
            
        Returns:
            Dict with keys:
                - title: str
                - summary: str  
                - body_md: str (full markdown with frontmatter)
                - world_ids: list[str]
                - level: int
                - tags: list[str]
                - metadata_json: dict
        """
        # Combine snippets into context
        snippets_text = self._format_snippets(file_snippets)
        
        # Get prompt for this doc_type
        user_prompt = get_prompt_for_doc_type(
            doc_type=doc_type,
            project_slug=project_slug,
            snippets=snippets_text,
            scan_meta=scan_meta
        )
        
        # Format system prompt with project context
        system_prompt = SYSTEM_PROMPT.format(
            project_slug=project_slug,
            doc_type=doc_type
        )
        
        # Generate with LLM
        generated_markdown = await self._call_llm(system_prompt, user_prompt)
        
        # Parse frontmatter and extract metadata
        return self._parse_generated_doc(generated_markdown, project_slug, doc_type, scan_meta)
    
    def _format_snippets(self, file_snippets: list[Dict]) -> str:
        """Format file snippets into readable context for LLM."""
        if not file_snippets:
            return "(No relevant files found in repository)"
        
        formatted = []
        for snippet_data in file_snippets:
            path = snippet_data.get("path", "unknown")
            snippet = snippet_data.get("snippet", "")
            
            formatted.append(f"**File: {path}**\n```\n{snippet}\n```\n")
        
        return "\n".join(formatted)
    
    async def _call_llm(self, system_prompt: str, user_prompt: str) -> str:
        """Call Vertex AI to generate documentation."""
        model = self._get_model()
        
        if model is None:
            # Fallback for testing without Vertex AI
            return self._generate_fallback_doc(user_prompt)
        
        try:
            # Combine system and user prompts
            full_prompt = f"{system_prompt}\n\n{user_prompt}"
            
            response = model.generate_content(
                full_prompt,
                generation_config={
                    "temperature": 0.3,  # Lower temperature for consistent, factual output
                    "max_output_tokens": 2048,
                    "top_p": 0.8,
                }
            )
            
            return response.text
        except Exception as e:
            print(f"LLM generation failed: {e}")
            return self._generate_fallback_doc(user_prompt)
    
    def _generate_fallback_doc(self, prompt: str) -> str:
        """Generate a minimal fallback doc when LLM is unavailable."""
        return """---
project: unknown
doc_type: overview
worlds: [world-python]
level: 2
stack:
  backend: Unknown
tags: []
---

# Project Overview

*This documentation could not be auto-generated.*

Please manually add documentation for this project.
"""
    
    def _parse_generated_doc(
        self,
        markdown: str,
        project_slug: str,
        doc_type: str,
        scan_meta: Dict
    ) -> Dict:
        """
        Parse generated markdown to extract frontmatter and content.
        
        Returns structured data for ProjectCodexDoc model.
        """
        # Split frontmatter from body
        parts = markdown.split("---", 2)
        
        if len(parts) >= 3:
            # Has frontmatter
            try:
                frontmatter = yaml.safe_load(parts[1])
                body_md = markdown  # Keep full markdown including frontmatter
            except yaml.YAMLError:
                # Malformed frontmatter, treat entire content as body
                frontmatter = {}
                body_md = markdown
        else:
            # No frontmatter found, add default
            frontmatter = {
                "project": project_slug,
                "doc_type": doc_type,
                "worlds": scan_meta.get("worlds", []),
                "level": 2,
                "tags": []
            }
            # Prepend frontmatter to markdown
            frontmatter_yaml = yaml.dump(frontmatter, default_flow_style=False)
            body_md = f"---\n{frontmatter_yaml}---\n\n{markdown}"
        
        # Extract title from first heading or generate default
        title = self._extract_title(markdown, project_slug, doc_type)
        
        # Extract summary from first paragraph after heading
        summary = self._extract_summary(markdown)
        
        # Extract metadata fields
        world_ids = frontmatter.get("worlds", scan_meta.get("worlds", []))
        level = frontmatter.get("level", 2)
        tags = frontmatter.get("tags", [])
        
        # Store full stack/domains in metadata_json
        metadata_json = {
            "stack": frontmatter.get("stack", scan_meta.get("stack", [])),
            "domains": frontmatter.get("domains", []),
            "frameworks": scan_meta.get("frameworks", {}),
            "languages": list(scan_meta.get("languages", {}).keys()),
        }
        
        return {
            "title": title,
            "summary": summary,
            "body_md": body_md,
            "world_ids": world_ids if isinstance(world_ids, list) else [world_ids],
            "level": level,
            "tags": tags if isinstance(tags, list) else [],
            "metadata_json": metadata_json
        }
    
    def _extract_title(self, markdown: str, project_slug: str, doc_type: str) -> str:
        """Extract title from first # heading or generate default."""
        for line in markdown.split('\n'):
            if line.startswith('# '):
                return line[2:].strip()
        
        # Default title
        return f"{project_slug.capitalize()}: {doc_type.replace('_', ' ').title()}"
    
    def _extract_summary(self, markdown: str) -> str:
        """Extract summary from first paragraph after frontmatter."""
        # Remove frontmatter
        content = markdown
        if content.startswith('---'):
            parts = content.split('---', 2)
            if len(parts) >= 3:
                content = parts[2]
        
        # Find first substantial paragraph (not heading)
        lines = content.strip().split('\n')
        summary_lines = []
        
        for line in lines:
            stripped = line.strip()
            if not stripped or stripped.startswith('#'):
                continue
            if len(stripped) > 20:  # Substantial content
                summary_lines.append(stripped)
                if len(' '.join(summary_lines)) > 100:  # Got enough
                    break
        
        summary = ' '.join(summary_lines)[:200]  # Max 200 chars
        return summary if summary else "Documentation for this project."
