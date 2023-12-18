-- name: create-new-grade<!
INSERT INTO grades (grade_name)
VALUES (:grade_name)
RETURNING
    id, created_at, updated_at;

-- name: get_grade_by_username
SELECT  grade_name FROM public.grades
where grade_name = :grade_name ;

-- name: get_grades
SELECT id AS "value" , grade_name as "label" FROM public.grades
ORDER BY id ASC ;

-- name: delete_grade_by_name!
DELETE
FROM grades
WHERE grade_name = :grade_name ;

-- name: get_all_class
SELECT c.id, 
       c.class_name As "className", 
       c.grade_id As "gradeId", 
       c.quantity, 
       g.grade_name As  "gradeName",
       t.id AS teacher_id,
       t.username As "homeroomTeacher"
FROM class c
JOIN grades g ON c.grade_id = g.id
LEFT JOIN teacher t ON c.id = t.homeroom_class_id
ORDER BY c.id ASC;

-- name: create-new-class<!
INSERT INTO class (class_name, grade_id, quantity)
VALUES (:class_name, :grade_id, :quantity)
RETURNING
    id, created_at, updated_at;

-- name: get_class_by_name
SELECT  class_name FROM public.class
where class_name = :class_name ;

-- name: delete_class_id
DELETE FROM public.class
where id = :class_id ;

-- name: update_teacher_is_null
UPDATE teacher
SET homeroom_class_id = NULL 
WHERE homeroom_class_id = :class_id;