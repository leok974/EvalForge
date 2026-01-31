
import json, glob, os
# Determine root dir (parent of scripts/)
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

paths = sorted(set(
  glob.glob(os.path.join(root_dir, 'data/questpacks/*.json')) +
  glob.glob(os.path.join(root_dir, 'seed/quests/*.json')) +
  glob.glob(os.path.join(root_dir, 'seed/**/*.json'), recursive=True)
))
packs=0; quests=0; bosses=0; tracks=0; worlds=0
for p in paths:
  try:
    obj=json.load(open(p,'r',encoding='utf-8'))
  except Exception:
    continue
  packs += 1
  # tolerate both single-pack and multi-pack layouts
  items = []
  if isinstance(obj, list):
      items = obj
  elif isinstance(obj, dict):
      if 'packs' in obj: items = obj['packs']
      elif 'quests' in obj: items = obj['quests'] # or should we treat the dict as one item if it's a quest?
      elif 'slug' in obj: items = [obj]
      # Also handle snapshot format (worlds key)
      if 'worlds' in obj:
          items.extend(obj['worlds'])
  
  for it in items:
    if not isinstance(it,dict): continue
    
    # Check if it's a world snapshot (contains tracks/bosses)
    if 'world_slug' in it and 'tracks' in it:
         worlds += 1
         tracks += len(it.get('tracks', []))
         
         # Count embedded quests in tracks
         for t in it.get('tracks', []):
             quests += len(t.get('quests', []))
             bosses += len(t.get('bosses', []))
         
         bosses += len(it.get('bosses', []))
    else:
        # Regular quest item?
        # A quest item doesn't usually contain other quests.
        # But if it's a list of quests, we are iterating them.
        # Does a quest have "quests"? No.
        # Does a quest have "bosses"? No.
        # Does a quest have "tracks"? No.
        # Does a quest have "worlds"? No.
        # So we just count it as a quest if it has a slug?
        if 'slug' in it:
             quests += 1

print('packs', packs)
print('quests', quests)
print('bosses', bosses)
print('tracks', tracks)
print('worlds', worlds)
