-- name: search-all-teacher
SELECT c.id, c.username, c.phone, c.address, c.homeroom_class_id, g.class_name
FROM teacher c  
LEFT JOIN "class" g ON c.homeroom_class_id = g.id 
ORDER BY c.id ASC;

-- SELECT c.id, c.class_name, c.grade_id, c.quantity, g.grade_name
-- FROM class c
-- JOIN grades g ON c.grade_id = g.id
-- ORDER BY c.id ASC;

-- name: search_teacher_unassigned
SELECT  id , username
FROM teacher where homeroom_class_id is null
 
--name: get_teacher_by_name<!
SELECT  id , username, phone , address, homeroom_class_id
FROM teacher where username= :username;

--name: check_phone_is_taken<!
SELECT  id , username, phone , address, homeroom_class_id
FROM teacher where phone= :phone ;

-- name: create-new-teacher<!
INSERT INTO teacher (username, phone, address)
VALUES (:name, :phone,  :address)
RETURNING
    id, created_at, updated_at;