-- name: create-new-student<!
INSERT INTO
    student (
        name,
        phone,
        gender,
        address,
        date_of_birth,
        class_id
    )
VALUES
    (
        :name,
        :phone,
        :gender,
        :address,
        :date_of_birth,
        :class_id
    ) RETURNING id;

-- name: student_update<!
UPDATE
    student
SET
    name = :name,
    phone = :phone,
    gender = :gender,
    address = :address,
    date_of_birth = :date_of_birth,
    class_id = :class_id
WHERE
    id = :id RETURNING id;

-- name: update_quantity
UPDATE
    class
SET
    quantity = quantity + :variable
WHERE
    id = :class_id -- name: update_quantity_change_class
UPDATE
    class
SET
    quantity = quantity + :variable
WHERE
    id = :class_id -- name: get_all_student
SELECT
    s.id,
    s.name,
    s.phone,
    s.address,
    s.gender,
    s.class_id AS "classId",
    TO_CHAR(s.date_of_birth, 'DD/MM/YYYY') AS "dateOfBirth",
    c.class_name AS "className",
    c.grade_id AS "gradeId"
FROM
    student s
    JOIN class c ON s.class_id = c.id;

-- name: get_student_by_id<!
SELECT
    id,
    name,
    phone,
    address,
    gender,
    class_id
FROM
    student
where
    id = :id;

-- name: get_student_by_name<!
SELECT
    id,
    name,
    phone,
    address,
    gender
FROM
    student
where
    name = :name;

-- name: get_student_by_phone<!
SELECT
    id,
    name,
    phone,
    address,
    gender
FROM
    student
where
    phone = :phone;

-- name: delete_student_by_id<!
DELETE FROM
    student
where
    id = :id RETURNING id,
    class_id -- name : insert_new_student_in_attendance
INSERT INTO
    attendance (student_id, status)
VALUES
    (:student_id, 2);

--name : delete_student_in_attendance
DELETE FROM
    attendance
WHERE
    student_id = :student_id