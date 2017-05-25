START TRANSACTION;

CREATE TABLE group_categories (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL
);

INSERT INTO group_categories VALUES
(1, 'sextourism'), (2, 'swing'), (3, 'gay'), (4, 'fetish/bdsm');

ALTER TABLE groups ADD COLUMN category_id INT NULL;

SET @min_groups_count = (
    SELECT MIN(cnt) FROM (
        (SELECT COUNT(group_id) AS cnt FROM groups WHERE
            group_name LIKE '%gay%'
            OR group_name LIKE '%lesb%'
            OR group_name LIKE '%trans%'
            OR group_name LIKE '%lgbt%'
            OR group_name LIKE '%glbt%'
            OR group_name LIKE '%bisex%'
            OR group_name LIKE '%queer%'
            OR group_name LIKE '%fag%'
            OR group_name REGEXP '\bFTMs?\b'
            OR group_name REGEXP '\bGAM\b'
            OR group_name LIKE '%homo%'
            OR group_name LIKE '%dyke%'
            OR group_name LIKE '\bbi\b'
            OR group_name REGEXP '%bisex%'
            OR group_name REGEXP '\bmtfs?\b'
            OR group_name LIKE '%femme%'
            OR group_name LIKE '%butch%'
            OR group_name REGEXP '\btg\b')
        UNION ALL
        (SELECT COUNT(group_id) AS cnt  FROM groups WHERE
            group_name LIKE '%touris%'
            OR group_name LIKE '%thai%'
            OR group_name LIKE '%russia%'
            OR group_name LIKE '%philippin%'
            OR group_name REGEXP '[[:<:]]cuban?[[:>:]]'
            OR group_name LIKE '%ukrain%'
            OR group_name LIKE '%latvia%'
            OR group_name LIKE '%Lithuan%'
            OR group_name LIKE '%estonia%'
            OR group_name LIKE '%belarus%'
            OR group_name LIKE '%brazil%'
            OR group_name LIKE '%cambodia%'
            OR group_name LIKE '%lao%'
            OR group_name LIKE '%vietnam%'
            OR group_name LIKE '%asian%'
            OR group_name LIKE '%burm%'
            OR group_name LIKE '%chin%'
            OR group_name REGEXP 'Hong\s?Kong'
            OR group_name LIKE '%india%'
            OR group_name LIKE '%indonesia%'
            OR group_name LIKE '%japan%'
            OR group_name LIKE '%Kyrgyzstan%'
            OR group_name LIKE '%Macau%'
            OR group_name LIKE '%Malaysia%'
            OR group_name LIKE '%Mongolia%'
            OR group_name LIKE '%Nepal%'
            OR group_name LIKE '%Korea%'
            OR group_name LIKE '%Pakistan%'
            OR group_name LIKE '%Singapor%'
            OR group_name REGEXP 'Sri\s?Lanka'
            OR group_name LIKE '%Taiwan%'
            OR group_name LIKE '%Tajikistan%'
            OR group_name LIKE '%Dominican%'
            OR group_name LIKE '%Caribb%'
            OR group_name LIKE '%jamaica%'
            OR group_name LIKE '%bali%'
            OR group_name LIKE '%bulgaria%'
            OR group_name LIKE '%egypt%'
            OR group_name LIKE '%turkey%'
            OR group_name LIKE '%racial%'
            OR group_name LIKE '%arab%'
            OR group_name LIKE '%nigg%'
            OR group_name LIKE '%travel%'
            OR group_name LIKE '%africa%'
            OR group_name LIKE '%latin%'
            OR group_name REGEXP 'Costa\s?Rica'
            OR group_name LIKE '%mexic%'
            OR group_name LIKE '%belize%'
            OR group_name LIKE '%guatemal%'
            OR group_name LIKE '%honduras%'
            OR group_name LIKE '%salvador%'
            OR group_name LIKE '%nicaragua%'
            OR group_name LIKE '%panama%'
            OR group_name LIKE '%colombia%'
            OR group_name LIKE '%venezuela%'
            OR group_name LIKE '%ecuador%'
            OR group_name LIKE '%guyana%'
            OR group_name LIKE '%guiana%'
            OR group_name LIKE '%surinam%'
            OR group_name LIKE '%peru%'
            OR group_name LIKE '%bolivia%'
            OR group_name LIKE '%paragua%'
            OR group_name LIKE '%chile%'
            OR group_name LIKE '%urugua%'
            OR group_name LIKE '%argentin%')
        UNION ALL
        (SELECT COUNT(group_id) AS cnt FROM groups WHERE
            group_name LIKE '%touris%'
            OR group_name LIKE '%swing%'
            OR group_name LIKE '%poly%'
            OR group_name LIKE '%hotwi%'
            OR group_name LIKE '%cuckold%'
            OR group_name LIKE '%orgy%'
            OR group_name REGEXP 'gang\s?bang'
            OR group_name LIKE '%voyeur%'
            OR group_name LIKE '%exhibit%'
            OR group_name REGEXP 'casual\s?encounter'
            OR group_name LIKE '%FFM%'
            OR group_name LIKE '%FMM%'
            OR group_name LIKE '%MFF%'
            OR group_name LIKE '%MMF%'
            OR group_name REGEXP 'hook(ing)?\s?up'
            OR group_name LIKE '%MFMF%'
            OR group_name LIKE '%swap%')
    ) x
);

PREPARE statement FROM 'UPDATE groups SET category_id=(SELECT id FROM group_categories WHERE name=''gay'')
WHERE
    (group_name LIKE ''%gay%''
    OR group_name LIKE ''%lesb%''
    OR group_name LIKE ''%trans%''
    OR group_name LIKE ''%lgbt%''
    OR group_name LIKE ''%glbt%''
    OR group_name LIKE ''%bisex%''
    OR group_name LIKE ''%queer%''
    OR group_name LIKE ''%fag%''
    OR group_name REGEXP ''\bFTMs?\b''
    OR group_name REGEXP ''\bGAM\b''
    OR group_name LIKE ''%homo%''
    OR group_name LIKE ''%dyke%''
    OR group_name LIKE ''\bbi\b''
    OR group_name REGEXP ''%bisex%''
    OR group_name REGEXP ''\bmtfs?\b''
    OR group_name LIKE ''%femme%''
    OR group_name LIKE ''%butch%''
    OR group_name REGEXP ''\btg\b'')
    AND category_id IS NULL
LIMIT ?';
EXECUTE statement USING @min_groups_count;
DEALLOCATE PREPARE statement;

PREPARE statement FROM 'UPDATE groups SET category_id=(SELECT id FROM group_categories WHERE name=''sextourism'')
WHERE
    (group_name LIKE ''%touris%''
    OR group_name LIKE ''%thai%''
    OR group_name LIKE ''%russia%''
    OR group_name LIKE ''%philippin%''
    OR group_name REGEXP ''[[:<:]]cuban?[[:>:]]''
    OR group_name LIKE ''%ukrain%''
    OR group_name LIKE ''%latvia%''
    OR group_name LIKE ''%Lithuan%''
    OR group_name LIKE ''%estonia%''
    OR group_name LIKE ''%belarus%''
    OR group_name LIKE ''%brazil%''
    OR group_name LIKE ''%cambodia%''
    OR group_name LIKE ''%lao%''
    OR group_name LIKE ''%vietnam%''
    OR group_name LIKE ''%asian%''
    OR group_name LIKE ''%burm%''
    OR group_name LIKE ''%chin%''
    OR group_name REGEXP ''Hong\s?Kong''
    OR group_name LIKE ''%india%''
    OR group_name LIKE ''%indonesia%''
    OR group_name LIKE ''%japan%''
    OR group_name LIKE ''%Kyrgyzstan%''
    OR group_name LIKE ''%Macau%''
    OR group_name LIKE ''%Malaysia%''
    OR group_name LIKE ''%Mongolia%''
    OR group_name LIKE ''%Nepal%''
    OR group_name LIKE ''%Korea%''
    OR group_name LIKE ''%Pakistan%''
    OR group_name LIKE ''%Singapor%''
    OR group_name REGEXP ''Sri\s?Lanka''
    OR group_name LIKE ''%Taiwan%''
    OR group_name LIKE ''%Tajikistan%''
    OR group_name LIKE ''%Dominican%''
    OR group_name LIKE ''%Caribb%''
    OR group_name LIKE ''%jamaica%''
    OR group_name LIKE ''%bali%''
    OR group_name LIKE ''%bulgaria%''
    OR group_name LIKE ''%egypt%''
    OR group_name LIKE ''%turkey%''
    OR group_name LIKE ''%racial%''
    OR group_name LIKE ''%arab%''
    OR group_name LIKE ''%nigg%''
    OR group_name LIKE ''%travel%''
    OR group_name LIKE ''%africa%''
    OR group_name LIKE ''%latin%''
    OR group_name REGEXP ''Costa\s?Rica''
    OR group_name LIKE ''%mexic%''
    OR group_name LIKE ''%belize%''
    OR group_name LIKE ''%guatemal%''
    OR group_name LIKE ''%honduras%''
    OR group_name LIKE ''%salvador%''
    OR group_name LIKE ''%nicaragua%''
    OR group_name LIKE ''%panama%''
    OR group_name LIKE ''%colombia%''
    OR group_name LIKE ''%venezuela%''
    OR group_name LIKE ''%ecuador%''
    OR group_name LIKE ''%guyana%''
    OR group_name LIKE ''%guiana%''
    OR group_name LIKE ''%surinam%''
    OR group_name LIKE ''%peru%''
    OR group_name LIKE ''%bolivia%''
    OR group_name LIKE ''%paragua%''
    OR group_name LIKE ''%chile%''
    OR group_name LIKE ''%urugua%''
    OR group_name LIKE ''%argentin%'')
    AND category_id IS NULL
LIMIT ?';
EXECUTE statement USING @min_groups_count;
DEALLOCATE PREPARE statement;

PREPARE statement FROM 'UPDATE groups SET category_id=(SELECT id FROM group_categories WHERE name=''swing'')
WHERE
    (group_name LIKE ''%touris%''
    OR group_name LIKE ''%swing%''
    OR group_name LIKE ''%poly%''
    OR group_name LIKE ''%hotwi%''
    OR group_name LIKE ''%cuckold%''
    OR group_name LIKE ''%orgy%''
    OR group_name REGEXP ''gang\s?bang''
    OR group_name LIKE ''%voyeur%''
    OR group_name LIKE ''%exhibit%''
    OR group_name REGEXP ''casual\s?encounter''
    OR group_name LIKE ''%FFM%''
    OR group_name LIKE ''%FMM%''
    OR group_name LIKE ''%MFF%''
    OR group_name LIKE ''%MMF%''
    OR group_name REGEXP ''hook(ing)?\s?up''
    OR group_name LIKE ''%MFMF%''
    OR group_name LIKE ''%swap%'')
    AND category_id IS NULL
LIMIT ?';
EXECUTE statement USING @min_groups_count;
DEALLOCATE PREPARE statement;

PREPARE statement FROM 'UPDATE groups SET category_id=(SELECT id FROM group_categories WHERE name=''fetish/bdsm'')
WHERE category_id IS NULL
LIMIT ?';
EXECUTE statement USING @min_groups_count;
DEALLOCATE PREPARE statement;

COMMIT;
