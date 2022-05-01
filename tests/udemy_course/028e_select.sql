SELECT
    photos.url,
    users.username
FROM photos
INNER JOIN users ON users.id = photos.user_id;
