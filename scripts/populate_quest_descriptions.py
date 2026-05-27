"""
Sprint 23: Populate short_description for quests that are missing it.

Strategy (Option B — briefing auto-extract):
  Priority order for each missing quest:
    1. If 'description' field is non-empty → copy it to short_description
    2. If 'briefing_md' field is non-empty → extract first meaningful sentence
    3. If data/quests/<slug>/docs/briefing.md exists → extract first meaningful sentence
    4. Log warning and skip (don't write blank)

Extraction rules:
  - Strip markdown headings (lines starting with #)
  - Strip bold/italic markers (**..**, *..*, __..__, _.._ )
  - Strip inline code backticks (`...`)
  - Strip link syntax [text](url) → text
  - Take first period-terminated sentence OR first 150 chars, whichever is shorter
  - Collapse whitespace

Run:
  python scripts/populate_quest_descriptions.py
  python scripts/populate_quest_descriptions.py --dry-run
"""

import argparse
import json
import pathlib
import re
import sys

BASE = pathlib.Path(__file__).parent.parent  # repo root

ACTIVE_QUESTPACKS = [
    "data/questpacks/python_systems.json",
    "data/questpacks/_tier2/python_tier2.json",
    "data/questpacks/foundry_python.json",
    "data/questpacks/python_selenium.json",
    "data/questpacks/web_html_core.json",
    "data/questpacks/web_css_core.json",
    "data/questpacks/sql_core.json",
    "data/questpacks/javascript_core.json",
    "data/questpacks/typescript_core.json",
    "data/questpacks/git_core.json",
    "data/questpacks/docker_ignition.json",
    "data/questpacks/docker_systems.json",
]


def strip_markdown(text: str) -> str:
    """Remove common markdown formatting from a text block."""
    # Remove headings
    text = re.sub(r'^#+\s+', '', text, flags=re.MULTILINE)
    # Remove bold/italic: **text**, __text__, *text*, _text_
    text = re.sub(r'\*\*(.+?)\*\*', r'\1', text)
    text = re.sub(r'__(.+?)__', r'\1', text)
    text = re.sub(r'\*(.+?)\*', r'\1', text)
    text = re.sub(r'_(.+?)_', r'\1', text)
    # Remove inline code
    text = re.sub(r'`(.+?)`', r'\1', text)
    # Remove links: [text](url) → text
    text = re.sub(r'\[(.+?)\]\(.+?\)', r'\1', text)
    # Remove images: ![alt](url) → ''
    text = re.sub(r'!\[.*?\]\(.+?\)', '', text)
    # Remove HTML tags
    text = re.sub(r'<[^>]+>', '', text)
    # Collapse whitespace / newlines to single space
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def extract_first_sentence(raw: str, max_chars: int = 150) -> str:
    """
    From a markdown string, extract the first meaningful sentence
    (≤ max_chars characters).
    Returns empty string if nothing usable is found.
    """
    # Split into lines, skip blank lines and heading lines
    lines = raw.splitlines()
    candidate_lines = []
    # Boilerplate patterns that appear in auto-generated briefings
    SKIP_PATTERNS = [
        r'^\*\*World:\*\*',
        r'^\*\*Objective:\*\*',
        r'^You need to implement',
        r'^Focus on meeting',
        r'^Edit `',
        r'^Requirements:',
        r'^\d+\)',           # numbered list items
        r'^-\s',             # bullet list items
    ]

    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.startswith('#'):
            continue
        # Skip lines that are just separators or metadata
        if re.match(r'^[-=*_]{3,}$', stripped):
            continue
        if any(re.match(p, stripped) for p in SKIP_PATTERNS):
            continue
        candidate_lines.append(stripped)

    if not candidate_lines:
        return ''

    # Join candidate lines (stop at first blank paragraph boundary)
    body = ' '.join(candidate_lines)
    body = strip_markdown(body)

    if not body:
        return ''

    # Try to find first sentence (ends with . ! ?)
    sentence_end = re.search(r'[.!?](?:\s|$)', body)
    if sentence_end:
        sentence = body[:sentence_end.start() + 1].strip()
        if len(sentence) > max_chars:
            # Truncate at word boundary
            sentence = sentence[:max_chars].rsplit(' ', 1)[0].rstrip('.,;:') + '…'
        return sentence

    # No sentence terminator: take first max_chars chars at word boundary
    if len(body) <= max_chars:
        return body
    return body[:max_chars].rsplit(' ', 1)[0].rstrip('.,;:') + '…'


def find_briefing_md(slug: str) -> str:
    """Try to find briefing.md content for a quest slug. Returns '' if not found."""
    # Standard location: data/quests/<slug>/docs/briefing.md
    path = BASE / 'data' / 'quests' / slug / 'docs' / 'briefing.md'
    if path.exists():
        return path.read_text(encoding='utf-8')
    # Alternate: data/quests/<slug>/workspace/README.md
    path2 = BASE / 'data' / 'quests' / slug / 'workspace' / 'README.md'
    if path2.exists():
        return path2.read_text(encoding='utf-8')
    return ''


def title_fallback(quest: dict) -> str | None:
    """Generate a short_description from the quest title as last resort."""
    title = quest.get('title', '').strip()
    if not title:
        return None
    # Use the title as the description (it's informative enough for browsing)
    return title if title.endswith('.') else title + '.'


def derive_short_description(quest: dict) -> str | None:
    """
    Try to derive a short_description for a quest.
    Returns the string to use, or None if no source was found.
    """
    slug = quest.get('slug', '')

    # Priority 1: existing 'description' field
    desc = quest.get('description', '').strip()
    if desc:
        cleaned = strip_markdown(desc)
        if cleaned:
            # Trim to 150 chars
            if len(cleaned) > 150:
                cleaned = cleaned[:150].rsplit(' ', 1)[0].rstrip('.,;:') + '…'
            return cleaned

    # Priority 2: inline 'briefing_md' field
    bmd = quest.get('briefing_md', '').strip()
    if bmd:
        result = extract_first_sentence(bmd)
        if result:
            return result

    # Priority 3: file-based briefing.md
    if slug:
        file_content = find_briefing_md(slug)
        if file_content:
            result = extract_first_sentence(file_content)
            if result:
                return result

    # Priority 4: title-based fallback
    fallback = title_fallback(quest)
    if fallback:
        return fallback

    return None


def process_pack(pack_path: pathlib.Path, dry_run: bool) -> dict:
    """Process one questpack JSON file. Returns stats dict."""
    data = json.loads(pack_path.read_text(encoding='utf-8'))

    # Determine if quests are top-level array or nested under 'quests' key
    is_list = isinstance(data, list)
    quests = data if is_list else data.get('quests', [])

    # For packs with pack-level world_id/track_id (SQL, HTML, CSS, Docker format)
    pack_world_id = None if is_list else data.get('world_id')
    pack_track_id = None if is_list else data.get('track_id')

    updated = 0
    skipped = 0
    already_ok = 0
    warnings = []

    for quest in quests:
        existing_sd = quest.get('short_description', '').strip()
        if existing_sd:
            already_ok += 1
            continue

        derived = derive_short_description(quest)
        if derived:
            if not dry_run:
                quest['short_description'] = derived
            updated += 1
        else:
            slug = quest.get('slug', '??')
            warnings.append(f"  WARNING: no source found for {slug}")
            skipped += 1

    if updated > 0 and not dry_run:
        # Write back (preserve formatting as best we can with indent=4)
        pack_path.write_text(
            json.dumps(data, indent=4, ensure_ascii=False) + '\n',
            encoding='utf-8'
        )

    return {
        'updated': updated,
        'skipped': skipped,
        'already_ok': already_ok,
        'warnings': warnings,
    }


def main():
    parser = argparse.ArgumentParser(description='Populate quest short_descriptions from briefing content.')
    parser.add_argument('--dry-run', action='store_true', help='Show what would change without writing files')
    args = parser.parse_args()

    if args.dry_run:
        print('DRY RUN — no files will be modified\n')

    total_updated = 0
    total_skipped = 0
    total_ok = 0

    for rel in ACTIVE_QUESTPACKS:
        pack_path = BASE / rel
        if not pack_path.exists():
            print(f'SKIP (not found): {rel}')
            continue

        stats = process_pack(pack_path, dry_run=args.dry_run)
        total_updated += stats['updated']
        total_skipped += stats['skipped']
        total_ok += stats['already_ok']

        status = 'DRY' if args.dry_run else 'WROTE'
        if stats['updated'] > 0:
            print(f'[{status}] {pack_path.name}: +{stats["updated"]} descriptions  ({stats["already_ok"]} already had one)')
        else:
            print(f'[OK]   {pack_path.name}: all {stats["already_ok"]} already had short_description')

        for w in stats['warnings']:
            print(w)

    print(f'\nSummary: {total_updated} populated, {total_ok} already OK, {total_skipped} no source found')
    if total_skipped > 0:
        print('  → Quests with no source need manual short_description in the questpack JSON')

    return 0 if total_skipped == 0 else 1


if __name__ == '__main__':
    sys.exit(main())
