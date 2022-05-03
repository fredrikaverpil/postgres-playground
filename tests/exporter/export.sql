WITH t (url, username) AS (
    SELECT photos.url,
        users.username
    FROM photos
        JOIN users on photos.user_id = users.id
)
SELECT json_agg(t)
from t