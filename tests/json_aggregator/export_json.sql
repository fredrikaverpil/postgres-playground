WITH t (url, username) AS (
    SELECT
        photos.url,
        users.username
    FROM photos
        JOIN users on photos.user_id = users.id
    LIMIT %s
)
SELECT json_agg(t)
FROM t
LIMIT %s
