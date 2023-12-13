-- name: search-all-teacher<!
SELECT  *
FROM teacher


-- name: create-new-teacher<!
INSERT INTO teacher (username, phone, homeroom_class_id)
VALUES (:name, :phone, :homeroom_class)
RETURNING
    id, created_at, updated_at;