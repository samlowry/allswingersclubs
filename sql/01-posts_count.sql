START TRANSACTION;

ALTER TABLE groups ADD COLUMN posts_count INT NULL;


UPDATE groups g
JOIN (
    SELECT g.group_id, COUNT(gp.topic_id) as posts_count
    FROM groups g
    JOIN group_posts gp ON gp.src_group_id = g.src_group_id
--  WHERE g.group_id IN (
--      7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21,
--      22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37
--  )
    GROUP BY g.group_id
    ORDER BY posts_count DESC
) x
ON g.group_id = x.group_id
SET g.posts_count = x.posts_count;

/*
    -- Test SELECT to calculate posts count across specified groups
    -- Remove "WHERE" clause to camculate over entire groups set
    SELECT
        g.group_id,
        g.src_group_id,
        g.group_name,
        COUNT(gp.topic_id) as posts_count
    FROM groups g
    JOIN group_posts gp ON gp.src_group_id = g.src_group_id
    WHERE g.group_id IN (
        7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21,
        22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37
    )
    GROUP BY g.group_id
    ORDER BY posts_count DESC;

    -- Check after update posts count statement
    SELECT
        group_id,
        src_group_id,
        group_name,
        posts_count
    FROM groups WHERE posts_count IS NOT NULL ORDER BY posts_count DESC;
*/

COMMIT;
