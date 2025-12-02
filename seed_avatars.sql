INSERT INTO avatardefinition (id, name, description, required_level, rarity, visual_type, visual_data, is_active) VALUES
('default_user', 'Initiate', 'Baseline identity. No augmentations installed.', 1, 'common', 'icon', 'user', true),
('coder_green', 'Script Kiddie', 'Emerald terminal glow.', 2, 'common', 'icon', 'terminal', true),
('python_gold', 'Snake Eye', 'Golden code sigil.', 5, 'rare', 'icon', 'code', true),
('neon_ghost', 'Netrunner', 'Glowing cyan silhouette. Pulses with traffic.', 10, 'epic', 'css', 'neon-pulse', true),
('glitch_king', 'Root User', 'Red/black avatar that glitches reality.', 20, 'epic', 'css', 'glitch', true),
('void_walker', 'Architect', 'Animated starfield masked into a circle.', 50, 'legendary', 'css', 'cosmic', true)
ON CONFLICT (id) DO NOTHING;
