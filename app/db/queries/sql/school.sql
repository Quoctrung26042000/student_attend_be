-- name: create-new-grade<!
INSERT INTO grades (grade_name)
VALUES (:grade_name)
RETURNING
    id, created_at, updated_at;

-- name: get_grade_by_username
SELECT  grade_name FROM public.grades
where grade_name = :grade_name ;

-- name: get_grades
SELECT * FROM public.grades
ORDER BY id ASC ;

-- name: delete_grade_by_name!
DELETE
FROM grades
WHERE grade_name = :grade_name ;

-- name: get_all_class
SELECT * FROM public.class
ORDER BY id ASC ;

-- name: create-new-class<!
INSERT INTO class (class_name, grade_id)
VALUES (:class_name, :grade_id)
RETURNING
    id, created_at, updated_at;

-- name: get_class_by_name
SELECT  class_name FROM public.class
where class_name = :class_name ;