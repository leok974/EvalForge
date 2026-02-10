#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

RE_PLACEHOLDER = re.compile(
    r"\b(TODO|TBD|PLACEHOLDER|LOREM IPSUM|COMING SOON|FILL THIS IN)\b",
    re.IGNORECASE,
)

# Common Codex link patterns (extend as needed)
RE_CODEX_TERM = re.compile(
    r"""
    (?:\[\[codex:(?P<t1>[a-z0-9/_\-]+)\]\])|
    (?:codex://(?P<t2>[a-z0-9/_\-]+))|
    (?:[?&]term=(?P<t3>[a-z0-9/_\-]+))
    """,
    re.IGNORECASE | re.VERBOSE,
)

RE_HEADING = re.compile(r"^\s*(#{1,6})\s+(.+?)\s*$", re.MULTILINE)

DEFAULT_DOCS_DIR = Path("docs/quests")
DEFAULT_CODEX_DIR = Path("docs/codex")
DEFAULT_QUESTPACK_DIR = Path("data/questpacks")


@dataclass
class DocCheck:
    path: str
    required: bool
    exists: bool
    errors: List[str]
    warnings: List[str]
    codex_terms_found: List[str]
    codex_terms_missing: List[str]


@dataclass
class QuestCheck:
    slug: str
    world: Optional[str]
    tutorial_tier: int
    docs: Dict[str, DocCheck]
    errors: List[str]
    warnings: List[str]


def _read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _safe_get_tutorial_tier(q: Dict[str, Any]) -> int:
    for k in ("tutorial_tier", "tier", "tutorialTier"):
        if k in q and isinstance(q[k], int):
            return q[k]
    meta = q.get("meta") or {}
    if isinstance(meta, dict):
        for k in ("tutorial_tier", "tier"):
            if k in meta and isinstance(meta[k], int):
                return meta[k]
    return 0


def _quest_slug(q: Dict[str, Any]) -> Optional[str]:
    for k in ("slug", "id", "quest_id"):
        v = q.get(k)
        if isinstance(v, str) and v.strip():
            return v.strip()
    return None


def _load_codex_terms_disk(codex_dir: Path) -> Set[str]:
    if not codex_dir.exists():
        return set()

    terms: Set[str] = set()
    for p in codex_dir.rglob("*.md"):
        if p.name.lower() == "readme.md":
            continue
        rel = p.relative_to(codex_dir).with_suffix("")
        term = str(rel).replace("\\", "/")
        terms.add(term.lower())
    return terms


def _extract_codex_terms(md: str) -> List[str]:
    found: List[str] = []
    for m in RE_CODEX_TERM.finditer(md):
        t = m.group("t1") or m.group("t2") or m.group("t3")
        if t:
            found.append(t.strip().lower())
    return sorted(set(found))


def _headings(md: str) -> List[str]:
    return [m.group(2).strip().lower() for m in RE_HEADING.finditer(md)]


def _check_placeholders(md: str) -> Optional[str]:
    m = RE_PLACEHOLDER.search(md)
    if not m:
        return None
    return f"Contains placeholder token '{m.group(1)}'."


def _check_min_structure(kind: str, md: str) -> Tuple[List[str], List[str]]:
    errs: List[str] = []
    warns: List[str] = []

    hs = _headings(md)

    if len(md.strip()) < 200:
        warns.append("Very short content (<200 chars).")

    if not hs:
        warns.append("No markdown headings found.")

    if kind == "briefing":
        must = {"objective", "context", "where you’ll work", "requirements", "constraints", "success criteria", "how to verify", "spec and codex references"}
        found = set(hs)
        missing = must - found
        
        # Checking for >= 5/8 match to allow some flexibility, but core sections must exist
        # Or better: check critical ones strictly
        critical = {"objective", "requirements", "success criteria", "how to verify"}
        missing_critical = critical - found
        
        if missing_critical:
            warns.append(f"Briefing missing critical sections: {missing_critical}")
        
        # Looser check for others to avoid breaking on typos
        if len(found.intersection(must)) < 5:
             warns.append(f"Briefing structure weak. Expected sections: {must}")

    if kind == "tutorial":
        must_any = {"what you’ll learn", "approach", "implementation plan", "testing", "pitfalls", "if you’re stuck"}
        found = set(hs)
        
        if len(found.intersection(must_any)) < 3:
            warns.append(f"Tutorial missing key sections (expected 3+ of: {must_any}). Found: {found}")

    if kind == "hints":
        # Check for Hint 1, Hint 2, Hint 3
        hint_headings = [h for h in hs if h.startswith("hint")]
        if len(hint_headings) < 3:
            warns.append(f"Hints must have at least 3 levels (Hint 1, Hint 2, Hint 3). Found: {len(hint_headings)}")

    if kind == "lore":
        if len(md.strip()) < 300:
            warns.append("Lore is short (<300 chars).")

    return errs, warns


def _check_doc(
    kind: str,
    path: Path,
    required: bool,
    codex_terms: Set[str],
    strict_codex: bool,
) -> DocCheck:
    errors: List[str] = []
    warnings: List[str] = []
    exists = path.exists()

    if not exists:
        if required:
            errors.append("Missing required file.")
        else:
            warnings.append("Missing optional file.")
        return DocCheck(
            path=str(path),
            required=required,
            exists=exists,
            errors=errors,
            warnings=warnings,
            codex_terms_found=[],
            codex_terms_missing=[],
        )

    md = path.read_text(encoding="utf-8").strip()
    if not md:
        errors.append("File exists but is empty.")
        return DocCheck(
            path=str(path),
            required=required,
            exists=exists,
            errors=errors,
            warnings=warnings,
            codex_terms_found=[],
            codex_terms_missing=[],
        )

    ph = _check_placeholders(md)
    if ph:
        errors.append(ph)

    se, sw = _check_min_structure(kind, md)
    errors.extend(se)
    warnings.extend(sw)

    terms_found = _extract_codex_terms(md)
    terms_missing: List[str] = []
    if terms_found and codex_terms:
        missing = [t for t in terms_found if t not in codex_terms]
        terms_missing = missing
        if missing:
            msg = f"Codex terms not found on disk: {missing}"
            if strict_codex:
                errors.append(msg)
            else:
                warnings.append(msg)

    return DocCheck(
        path=str(path),
        required=required,
        exists=exists,
        errors=errors,
        warnings=warnings,
        codex_terms_found=terms_found,
        codex_terms_missing=terms_missing,
    )


def _iter_questpacks(paths: List[Path]) -> List[Tuple[Path, Dict[str, Any]]]:
    out: List[Tuple[Path, Dict[str, Any]]] = []
    for p in paths:
        try:
            out.append((p, _read_json(p)))
        except Exception as e:
            out.append((p, {"__parse_error__": str(e)}))
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--questpack", action="append", default=[], help="Path to a questpack JSON (repeatable).")
    ap.add_argument("--world", default=None, help="Filter by world id (e.g., world-react).")
    ap.add_argument("--only-slug", default=None, help="Check a single quest slug.")
    ap.add_argument("--tier", type=int, default=None, help="Only check quests with tutorial_tier >= N.")
    ap.add_argument("--fail-on-warn", action="store_true", help="Warnings become fatal (non-zero exit).")
    ap.add_argument("--strict-codex", action="store_true", help="Missing Codex terms become errors.")
    ap.add_argument("--require-lore", action="store_true", help="Require lore.md for checked quests.")
    ap.add_argument("--format", choices=["text", "json"], default="text")
    args = ap.parse_args()

    questpacks: List[Path] = [Path(p) for p in args.questpack]
    if not questpacks:
        questpacks = sorted(DEFAULT_QUESTPACK_DIR.glob("*.json"))

    codex_terms = _load_codex_terms_disk(DEFAULT_CODEX_DIR)

    checks: List[QuestCheck] = []
    pack_items = _iter_questpacks(questpacks)

    for pack_path, pack in pack_items:
        if "__parse_error__" in pack:
            checks.append(
                QuestCheck(
                    slug=f"(questpack parse error) {pack_path}",
                    world=None,
                    tutorial_tier=0,
                    docs={},
                    errors=[pack["__parse_error__"]],
                    warnings=[],
                )
            )
            continue

        # Handle list-based questpacks (legacy or flat structure)
        if isinstance(pack, list):
            world = None
            quests = pack
        else:
            world = pack.get("world") or pack.get("world_id") or pack.get("id")
            quests = pack.get("quests") or []

        if args.world and world != args.world:
            continue

        if not isinstance(quests, list):
            continue

        for q in quests:
            if not isinstance(q, dict):
                continue

            slug = _quest_slug(q)
            if not slug:
                continue
            if args.only_slug and slug != args.only_slug:
                continue

            tutorial_tier = _safe_get_tutorial_tier(q)
            if args.tier is not None and tutorial_tier < args.tier:
                continue

            # Tier-1+ contract
            briefing_required = tutorial_tier >= 1
            tutorial_required = tutorial_tier >= 1
            hints_required = tutorial_tier >= 1
            lore_required = args.require_lore

            quest_dir = DEFAULT_DOCS_DIR / slug
            docs = {
                "briefing": _check_doc("briefing", quest_dir / "briefing.md", briefing_required, codex_terms, args.strict_codex),
                "tutorial": _check_doc("tutorial", quest_dir / "tutorial.md", tutorial_required, codex_terms, args.strict_codex),
                "hints": _check_doc("hints", quest_dir / "hints.md", hints_required, codex_terms, args.strict_codex),
                "lore": _check_doc("lore", quest_dir / "lore.md", lore_required, codex_terms, args.strict_codex),
            }

            q_errors: List[str] = []
            q_warnings: List[str] = []
            for d in docs.values():
                q_errors.extend(d.errors)
                q_warnings.extend(d.warnings)

            checks.append(
                QuestCheck(
                    slug=slug,
                    world=world if isinstance(world, str) else None,
                    tutorial_tier=tutorial_tier,
                    docs=docs,
                    errors=q_errors,
                    warnings=q_warnings,
                )
            )

    total_errors = sum(len(c.errors) for c in checks)
    total_warnings = sum(len(c.warnings) for c in checks)

    if args.format == "json":
        payload = {
            "summary": {
                "quests_checked": len(checks),
                "errors": total_errors,
                "warnings": total_warnings,
                "fail_on_warn": args.fail_on_warn,
                "strict_codex": args.strict_codex,
                "require_lore": args.require_lore
            },
            "quests": [asdict(c) for c in checks],
        }
        print(json.dumps(payload, indent=2))
    else:
        print(f"[audit_quest_content] quests={len(checks)} errors={total_errors} warnings={total_warnings}")
        for c in checks:
            if not c.errors and not c.warnings:
                continue
            print(f"\n- {c.slug} (world={c.world}, tier={c.tutorial_tier})")
            for k, d in c.docs.items():
                if not d.errors and not d.warnings:
                    continue
                status = "OK" if d.exists else "MISSING"
                req = "REQ" if d.required else "OPT"
                print(f"  * {k}: {status} ({req}) -> {d.path}")
                for e in d.errors:
                    print(f"      ERROR: {e}")
                for w in d.warnings:
                    print(f"      WARN:  {w}")

    if total_errors > 0:
        return 1
    if args.fail_on_warn and total_warnings > 0:
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
