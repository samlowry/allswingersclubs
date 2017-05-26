-- Add column to mark processed items and pre-mark incorrect posts (dropped from processing)

ALTER TABLE group_posts
    ADD COLUMN processed BIT NULL
    ADD COLUMN unprocessable BIT NULL;

UPDATE group_posts SET unprocessable WHERE time IS NULL;
