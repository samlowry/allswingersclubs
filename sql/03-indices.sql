CREATE INDEX ix_groups__group_id ON groups (group_id);
CREATE INDEX ix_group_posts__group_id ON group_posts (group_id);
CREATE INDEX ix_group_posts__author_id ON group_posts (author_id);
CREATE INDEX ix_users__user_id ON users (user_id);
CREATE INDEX ix_group_posts__time ON group_posts (time);
