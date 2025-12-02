ALTER TABLE "user" ADD COLUMN IF NOT EXISTS current_avatar_id VARCHAR DEFAULT 'default_user';
