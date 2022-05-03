WITH t (url, username, user_id) AS (
    SELECT photos.url,
        users.username,
        photos.user_id
    FROM photos
        JOIN users on photos.user_id = users.id
)
SELECT json_agg(t)
from t