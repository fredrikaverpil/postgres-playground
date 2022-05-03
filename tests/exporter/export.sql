WITH t (url, user_id) AS (
    SELECT url,
        user_id
    FROM photos
)
SELECT json_agg(t)
from t